#!/usr/bin/env python3
"""
自动化视频处理器 - 一键生成B站就绪视频
输入: 视频文件路径
输出: 双语字幕 + 弹幕 + 水印的完整B站版本

使用方法:
python auto_video_processor.py <video_path>
或
python auto_video_processor.py  # 交互式选择文件
"""

import json
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse
import glob

class AutoVideoProcessor:
    def __init__(self):
        self.base_dir = Path("output")
        self.watermark_path = "output/bilibili_hd_watermark.png"
        
    def setup_project_directory(self, video_path: str) -> Path:
        """为视频创建专门的项目目录"""
        video_name = Path(video_path).stem
        # 清理文件名，移除特殊字符
        clean_name = "".join(c for c in video_name if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_name = clean_name.replace(' ', '_')[:50]  # 限制长度
        
        project_dir = self.base_dir / f"{clean_name}_processed"
        project_dir.mkdir(exist_ok=True, parents=True)
        
        # 复制原视频到项目目录
        original_video = project_dir / f"original_{Path(video_path).name}"
        if not original_video.exists():
            shutil.copy2(video_path, original_video)
        
        return project_dir, original_video
    
    def extract_audio(self, video_path: str, output_path: str) -> bool:
        """提取音频用于转录"""
        try:
            cmd = [
                'ffmpeg', '-i', video_path,
                '-vn', '-acodec', 'libmp3lame',
                '-ar', '16000', '-ac', '1',
                '-y', output_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except:
            return False
    
    def find_subtitle_files(self, project_dir: Path, video_name: str) -> Tuple[Optional[str], Optional[str]]:
        """查找英文和中文字幕文件"""
        
        # 常见的字幕文件命名模式
        patterns = [
            f"{video_name}*english*.srt",
            f"{video_name}*English*.srt", 
            f"{video_name}*en*.srt",
            f"{video_name}*sider*chinese*.srt",
            f"{video_name}*Sider*Chinese*.srt",
            f"{video_name}*chinese*.srt",
            f"{video_name}*Chinese*.srt",
            f"{video_name}*zh*.srt"
        ]
        
        # 在整个output目录中查找
        english_srt = None
        chinese_srt = None
        
        for pattern in patterns:
            files = list(self.base_dir.glob(f"**/{pattern}"))
            for file in files:
                if 'english' in file.name.lower() or 'en' in file.name.lower():
                    if english_srt is None:
                        english_srt = str(file)
                elif 'chinese' in file.name.lower() or 'sider' in file.name.lower() or 'zh' in file.name.lower():
                    if chinese_srt is None:
                        chinese_srt = str(file)
        
        # 复制到项目目录
        if english_srt:
            dest = project_dir / "english_subtitles.srt"
            shutil.copy2(english_srt, dest)
            english_srt = str(dest)
        
        if chinese_srt:
            dest = project_dir / "chinese_subtitles.srt"
            shutil.copy2(chinese_srt, dest)
            chinese_srt = str(dest)
            
        return english_srt, chinese_srt
    
    def create_dual_subtitles(self, english_srt: str, chinese_srt: str, output_path: str) -> bool:
        """创建双语字幕"""
        try:
            with open(english_srt, 'r', encoding='utf-8') as f:
                english_lines = f.readlines()
            
            with open(chinese_srt, 'r', encoding='utf-8') as f:
                chinese_lines = f.readlines()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                i = 0
                while i < len(english_lines):
                    line = english_lines[i].strip()
                    
                    if line.isdigit():
                        subtitle_num = line
                        f.write(f"{subtitle_num}\n")
                        
                        # 时间轴
                        i += 1
                        if i < len(english_lines):
                            time_line = english_lines[i].strip()
                            f.write(f"{time_line}\n")
                        
                        # 英文内容
                        i += 1
                        english_content = []
                        while i < len(english_lines) and english_lines[i].strip():
                            english_content.append(english_lines[i].strip())
                            i += 1
                        
                        # 查找对应中文
                        chinese_content = self.find_matching_chinese(subtitle_num, chinese_lines)
                        
                        # 写入双语字幕
                        if english_content:
                            f.write(" ".join(english_content) + "\n")
                        if chinese_content:
                            f.write(chinese_content + "\n")
                        
                        f.write("\n")
                    
                    i += 1
            
            return True
        except Exception as e:
            print(f"创建双语字幕失败: {e}")
            return False
    
    def find_matching_chinese(self, subtitle_num: str, chinese_lines: List[str]) -> str:
        """查找匹配的中文字幕"""
        for i, line in enumerate(chinese_lines):
            if line.strip() == subtitle_num:
                i += 2  # 跳过时间轴
                chinese_content = []
                while i < len(chinese_lines) and chinese_lines[i].strip():
                    chinese_content.append(chinese_lines[i].strip())
                    i += 1
                return " ".join(chinese_content)
        return ""
    
    def generate_smart_danmaku(self, video_path: str, duration: float, output_path: str) -> bool:
        """智能生成弹幕"""
        
        # 政治视频弹幕模板
        political_templates = [
            "重要视频alert",
            "见证历史时刻", 
            "这就是现实政治",
            "关键时刻来了",
            "政治就是这样",
            "历史不会忘记",
            "democracy matters",
            "值得深思",
            "政治智慧体现",
            "这个细节很重要"
        ]
        
        # 根据视频长度生成弹幕
        num_danmaku = min(max(int(duration / 10), 3), 8)  # 3-8条弹幕
        
        danmaku_list = []
        for i in range(num_danmaku):
            time_ms = int((duration * 1000 / (num_danmaku + 1)) * (i + 1))
            
            danmaku = {
                "time": time_ms,
                "type": 1,
                "color": 16777215,  # 白色
                "author": "UP主",
                "text": political_templates[i % len(political_templates)],
                "mode": 1,  # 滚动
                "fontsize": 20
            }
            danmaku_list.append(danmaku)
        
        danmaku_data = {
            "video_title": Path(video_path).stem,
            "duration": duration,
            "danmaku_count": len(danmaku_list),
            "danmaku_list": danmaku_list
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(danmaku_data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def convert_danmaku_to_ass(self, danmaku_json: str, output_path: str) -> bool:
        """转换弹幕为ASS格式"""
        try:
            with open(danmaku_json, 'r', encoding='utf-8') as f:
                danmaku_data = json.load(f)
            
            ass_content = [
                "[Script Info]",
                "Title: Auto Generated Danmaku",
                "ScriptType: v4.00+",
                "",
                "[V4+ Styles]",
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
                "Style: Danmaku,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1",
                "",
                "[Events]",
                "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
            ]
            
            for danmaku in danmaku_data["danmaku_list"]:
                start_ms = danmaku["time"]
                start_time = self.ms_to_ass_time(start_ms)
                end_time = self.ms_to_ass_time(start_ms + 8000)
                
                move_effect = "{\\move(1920,540,0,540)}"
                text = f"{move_effect}{danmaku['text']}"
                
                ass_line = f"Dialogue: 0,{start_time},{end_time},Danmaku,,0,0,0,,{text}"
                ass_content.append(ass_line)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(ass_content))
            
            return True
        except:
            return False
    
    def ms_to_ass_time(self, ms: int) -> str:
        """毫秒转ASS时间格式"""
        total_seconds = ms / 1000
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        centiseconds = int((ms % 1000) / 10)
        return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
    
    def get_video_duration(self, video_path: str) -> float:
        """获取视频时长"""
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', video_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return float(data['format']['duration'])
        except:
            return 60.0  # 默认60秒
    
    def create_final_video(self, original_video: str, dual_srt: str, danmaku_ass: str, 
                          watermark: str, output_path: str, include_danmaku: bool = False) -> bool:
        """创建最终视频"""
        
        if include_danmaku:
            # 包含弹幕的完整版
            filter_complex = (
                f"[0:v]subtitles='{dual_srt}':force_style='FontSize=16,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1'[v1];"
                f"[v1]subtitles='{danmaku_ass}'[v2];"
                "[v2][1:v]overlay=main_w-overlay_w-20:20[v3]"
            )
        else:
            # B站版本（无弹幕）
            filter_complex = (
                f"[0:v]subtitles='{dual_srt}':force_style='FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2'[v1];"
                "[v1][1:v]overlay=main_w-overlay_w-20:20[v2]"
            )
        
        cmd = [
            'ffmpeg',
            '-i', original_video,
            '-i', watermark,
            '-filter_complex', filter_complex,
            '-map', '[v3]' if include_danmaku else '[v2]',
            '-map', '0:a',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-c:v', 'libx264',
            '-crf', '20',
            '-preset', 'medium',
            '-pix_fmt', 'yuv420p',
            '-y', output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except Exception as e:
            print(f"视频生成失败: {e}")
            return False
    
    def process_video(self, video_path: str) -> Optional[Dict]:
        """主处理流程"""
        
        print(f"🎬 开始处理视频: {Path(video_path).name}")
        
        # 1. 设置项目目录
        project_dir, original_video = self.setup_project_directory(video_path)
        video_name = Path(video_path).stem
        
        # 2. 获取视频信息
        duration = self.get_video_duration(str(original_video))
        print(f"⏱️  视频时长: {duration:.1f}秒")
        
        # 3. 查找字幕文件
        print("🔍 查找字幕文件...")
        english_srt, chinese_srt = self.find_subtitle_files(project_dir, video_name)
        
        if not english_srt or not chinese_srt:
            print("❌ 未找到完整的双语字幕文件")
            print(f"英文字幕: {'✅' if english_srt else '❌'}")
            print(f"中文字幕: {'✅' if chinese_srt else '❌'}")
            return None
        
        print(f"✅ 字幕文件已找到")
        
        # 4. 创建双语字幕
        print("📝 生成双语字幕...")
        dual_srt = project_dir / "dual_subtitles.srt"
        if not self.create_dual_subtitles(english_srt, chinese_srt, str(dual_srt)):
            print("❌ 双语字幕生成失败")
            return None
        
        # 5. 生成智能弹幕
        print("🎭 生成智能弹幕...")
        danmaku_json = project_dir / "danmaku.json"
        danmaku_ass = project_dir / "danmaku.ass"
        
        if not self.generate_smart_danmaku(str(original_video), duration, str(danmaku_json)):
            print("❌ 弹幕生成失败")
            return None
        
        if not self.convert_danmaku_to_ass(str(danmaku_json), str(danmaku_ass)):
            print("❌ 弹幕转换失败")
            return None
        
        # 6. 检查水印
        if not os.path.exists(self.watermark_path):
            print("❌ 未找到水印文件")
            return None
        
        # 7. 生成最终视频
        print("🎬 生成B站版本...")
        bilibili_video = project_dir / f"{video_name}_bilibili_ready.mp4"
        
        if not self.create_final_video(
            str(original_video), str(dual_srt), str(danmaku_ass),
            self.watermark_path, str(bilibili_video), include_danmaku=False
        ):
            print("❌ B站版本生成失败")
            return None
        
        # 8. 生成完整版本（可选）
        print("🎬 生成完整版本...")
        complete_video = project_dir / f"{video_name}_complete.mp4"
        
        self.create_final_video(
            str(original_video), str(dual_srt), str(danmaku_ass),
            self.watermark_path, str(complete_video), include_danmaku=True
        )
        
        # 9. 生成结果摘要
        file_size_mb = bilibili_video.stat().st_size / (1024 * 1024)
        
        result = {
            "project_dir": str(project_dir),
            "bilibili_video": str(bilibili_video),
            "complete_video": str(complete_video),
            "dual_subtitles": str(dual_srt),
            "danmaku_json": str(danmaku_json),
            "file_size_mb": round(file_size_mb, 1),
            "duration": duration
        }
        
        print("\n🎉 处理完成！")
        print(f"📁 项目目录: {project_dir}")
        print(f"📺 B站版本: {bilibili_video.name} ({file_size_mb:.1f}MB)")
        print(f"🎬 完整版本: {complete_video.name}")
        
        return result


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='自动化视频处理器')
    parser.add_argument('video_path', nargs='?', help='视频文件路径')
    parser.add_argument('--batch', action='store_true', help='批量处理模式')
    
    args = parser.parse_args()
    
    processor = AutoVideoProcessor()
    
    if args.batch:
        # 批量处理模式
        video_files = []
        for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv']:
            video_files.extend(glob.glob(f"output/**/{ext}", recursive=True))
        
        print(f"发现 {len(video_files)} 个视频文件")
        for video in video_files:
            if 'processed' not in video and 'bilibili' not in video:
                result = processor.process_video(video)
                if result:
                    print(f"✅ {Path(video).name} 处理完成")
                else:
                    print(f"❌ {Path(video).name} 处理失败")
                print("-" * 50)
    
    elif args.video_path:
        # 单文件处理
        if not os.path.exists(args.video_path):
            print(f"❌ 文件不存在: {args.video_path}")
            sys.exit(1)
        
        result = processor.process_video(args.video_path)
        if not result:
            sys.exit(1)
    
    else:
        # 交互式选择
        video_files = []
        for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv']:
            video_files.extend(glob.glob(f"output/**/{ext}", recursive=True))
        
        # 过滤掉已处理的文件
        video_files = [v for v in video_files if 'processed' not in v and 'bilibili' not in v]
        
        if not video_files:
            print("❌ 未找到可处理的视频文件")
            sys.exit(1)
        
        print("📹 发现以下视频文件:")
        for i, video in enumerate(video_files, 1):
            print(f"{i}. {Path(video).name}")
        
        try:
            choice = int(input("\n请选择要处理的视频 (序号): ")) - 1
            if 0 <= choice < len(video_files):
                result = processor.process_video(video_files[choice])
                if not result:
                    sys.exit(1)
            else:
                print("❌ 无效选择")
                sys.exit(1)
        except (ValueError, KeyboardInterrupt):
            print("\n❌ 操作取消")
            sys.exit(1)


if __name__ == "__main__":
    main() 