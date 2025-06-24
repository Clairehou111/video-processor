#!/usr/bin/env python3
"""
Trump Jan 6 完整视频生成器
包含双语字幕、弹幕和HD水印的最终版本
"""

import json
import os
import subprocess
import tempfile
from typing import List, Dict

class TrumpJan6VideoProcessor:
    def __init__(self):
        self.project_dir = "output/trump_jan6_complete_project"
        self.original_video = f"{self.project_dir}/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena.mp4"
        self.english_srt = f"{self.project_dir}/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena_english.srt"
        self.chinese_srt = f"{self.project_dir}/Trump_Sider_Chinese_Subtitles.srt"
        self.danmaku_json = f"{self.project_dir}/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena_jan6_special_danmaku.json"
        self.watermark = f"{self.project_dir}/bilibili_hd_watermark.png"
        
    def create_dual_subtitles(self) -> str:
        """创建双语字幕文件"""
        
        print("📝 创建双语字幕文件...")
        
        # 读取英文字幕
        with open(self.english_srt, 'r', encoding='utf-8') as f:
            english_lines = f.readlines()
        
        # 读取中文字幕  
        with open(self.chinese_srt, 'r', encoding='utf-8') as f:
            chinese_lines = f.readlines()
        
        dual_srt_path = f"{self.project_dir}/trump_jan6_dual_subtitles.srt"
        
        with open(dual_srt_path, 'w', encoding='utf-8') as f:
            english_subtitle = ""
            chinese_subtitle = ""
            
            i = 0
            while i < len(english_lines):
                line = english_lines[i].strip()
                
                # 字幕序号
                if line.isdigit():
                    subtitle_num = line
                    f.write(f"{subtitle_num}\n")
                    
                    # 时间轴
                    i += 1
                    if i < len(english_lines):
                        time_line = english_lines[i].strip()
                        f.write(f"{time_line}\n")
                    
                    # 英文字幕内容
                    i += 1
                    english_content = []
                    while i < len(english_lines) and english_lines[i].strip():
                        english_content.append(english_lines[i].strip())
                        i += 1
                    
                    # 查找对应的中文字幕
                    chinese_content = self.find_matching_chinese_subtitle(subtitle_num, chinese_lines)
                    
                    # 写入双语字幕
                    if english_content:
                        # 英文在上
                        f.write(" ".join(english_content) + "\n")
                    if chinese_content:
                        # 中文在下  
                        f.write(chinese_content + "\n")
                    
                    f.write("\n")
                
                i += 1
        
        print(f"✅ 双语字幕已创建: {dual_srt_path}")
        return dual_srt_path
    
    def find_matching_chinese_subtitle(self, subtitle_num: str, chinese_lines: List[str]) -> str:
        """查找匹配的中文字幕"""
        
        for i, line in enumerate(chinese_lines):
            if line.strip() == subtitle_num:
                # 跳过时间轴行
                i += 2
                chinese_content = []
                while i < len(chinese_lines) and chinese_lines[i].strip():
                    chinese_content.append(chinese_lines[i].strip())
                    i += 1
                return " ".join(chinese_content)
        
        return ""
    
    def convert_danmaku_to_ass(self) -> str:
        """将弹幕JSON转换为ASS字幕格式"""
        
        print("🎭 转换弹幕为ASS格式...")
        
        with open(self.danmaku_json, 'r', encoding='utf-8') as f:
            danmaku_data = json.load(f)
        
        ass_content = [
            "[Script Info]",
            "Title: Trump Jan 6 Danmaku",
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
            end_time = self.ms_to_ass_time(start_ms + 8000)  # 显示8秒
            
            # 弹幕移动效果
            move_effect = "{\\move(1920,540,0,540)}"
            text = f"{move_effect}{danmaku['text']}"
            
            ass_line = f"Dialogue: 0,{start_time},{end_time},Danmaku,,0,0,0,,{text}"
            ass_content.append(ass_line)
        
        ass_path = f"{self.project_dir}/trump_jan6_danmaku.ass"
        with open(ass_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ass_content))
        
        print(f"✅ ASS弹幕文件已创建: {ass_path}")
        return ass_path
    
    def ms_to_ass_time(self, ms: int) -> str:
        """毫秒转ASS时间格式"""
        total_seconds = ms / 1000
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        centiseconds = int((ms % 1000) / 10)
        return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
    
    def create_final_video(self, dual_srt_path: str, danmaku_ass_path: str) -> str:
        """创建最终视频：原视频 + 双语字幕 + 弹幕 + 水印"""
        
        print("🎬 生成最终视频...")
        
        output_video = f"{self.project_dir}/trump_jan6_final_complete.mp4"
        
        # FFmpeg命令：添加双语字幕、弹幕和水印
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', self.original_video,
            '-i', self.watermark,
            '-filter_complex',
            (
                # 添加双语字幕
                f"[0:v]subtitles='{dual_srt_path}':force_style='FontSize=16,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1'[v1];"
                # 添加弹幕
                f"[v1]subtitles='{danmaku_ass_path}'[v2];"
                # 添加水印到右上角
                "[v2][1:v]overlay=main_w-overlay_w-20:20[v3]"
            ),
            '-map', '[v3]',
            '-map', '0:a',
            '-c:a', 'copy',
            '-c:v', 'libx264',
            '-crf', '23',
            '-preset', 'medium',
            '-y',
            output_video
        ]
        
        try:
            print("⏳ 正在处理视频，请稍候...")
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print(f"✅ 最终视频已生成: {output_video}")
            
            # 显示文件信息
            file_size = os.path.getsize(output_video) / (1024 * 1024)
            print(f"📊 文件大小: {file_size:.1f}MB")
            
            return output_video
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 视频生成失败:")
            print(f"错误: {e.stderr}")
            return None
        except FileNotFoundError:
            print("❌ 未找到FFmpeg，请确保已安装")
            return None
    
    def create_bilibili_ready_video(self, dual_srt_path: str, danmaku_ass_path: str) -> str:
        """创建B站优化版本（不包含弹幕，只有字幕和水印）"""
        
        print("📺 生成B站优化版本...")
        
        output_video = f"{self.project_dir}/trump_jan6_bilibili_ready.mp4"
        
        # FFmpeg命令：只添加双语字幕和水印，不添加弹幕
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', self.original_video,
            '-i', self.watermark,
            '-filter_complex',
            (
                # 添加双语字幕
                f"[0:v]subtitles='{dual_srt_path}':force_style='FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2'[v1];"
                # 添加水印到右上角
                "[v1][1:v]overlay=main_w-overlay_w-20:20[v2]"
            ),
            '-map', '[v2]',
            '-map', '0:a',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-c:v', 'libx264',
            '-crf', '20',  # 更高质量
            '-preset', 'medium',
            '-pix_fmt', 'yuv420p',
            '-y',
            output_video
        ]
        
        try:
            print("⏳ 正在生成B站版本，请稍候...")
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print(f"✅ B站版本已生成: {output_video}")
            
            # 显示文件信息
            file_size = os.path.getsize(output_video) / (1024 * 1024)
            print(f"📊 文件大小: {file_size:.1f}MB")
            
            return output_video
            
        except subprocess.CalledProcessError as e:
            print(f"❌ B站版本生成失败:")
            print(f"错误: {e.stderr}")
            return None
    
    def process_complete_video(self):
        """处理完整视频的主流程"""
        
        print("🎯 Trump Jan 6 完整视频处理开始")
        print("=" * 50)
        
        # 检查必需文件
        required_files = [
            self.original_video,
            self.english_srt,
            self.chinese_srt,
            self.danmaku_json,
            self.watermark
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                print(f"❌ 缺少必需文件: {file_path}")
                return
        
        print("✅ 所有必需文件检查完成")
        
        # 1. 创建双语字幕
        dual_srt_path = self.create_dual_subtitles()
        
        # 2. 转换弹幕为ASS格式
        danmaku_ass_path = self.convert_danmaku_to_ass()
        
        # 3. 生成完整版（含弹幕）
        final_video = self.create_final_video(dual_srt_path, danmaku_ass_path)
        
        # 4. 生成B站版（无弹幕）
        bilibili_video = self.create_bilibili_ready_video(dual_srt_path, danmaku_ass_path)
        
        print("\n🎉 视频处理完成！")
        print("=" * 30)
        print(f"📹 完整版（含弹幕）: {final_video}")
        print(f"📺 B站版（无弹幕）: {bilibili_video}")
        print(f"📝 双语字幕: {dual_srt_path}")
        print(f"🎭 弹幕ASS: {danmaku_ass_path}")
        
        return final_video, bilibili_video


def main():
    """主函数"""
    processor = TrumpJan6VideoProcessor()
    processor.process_complete_video()


if __name__ == "__main__":
    main() 