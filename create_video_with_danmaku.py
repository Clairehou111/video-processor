#!/usr/bin/env python3
"""
直接生成带弹幕的视频
使用FFmpeg实现，无需手动操作剪映
"""

import json
import os
import subprocess
import tempfile
from typing import List, Dict

class VideoDanmakuProcessor:
    def __init__(self):
        self.temp_files = []
    
    def create_ass_subtitle(self, danmaku_data: Dict, video_duration: float, 
                          output_path: str) -> str:
        """将弹幕数据转换为ASS字幕格式"""
        
        # ASS文件头部
        ass_header = """[Script Info]
Title: Danmaku Subtitle
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Danmaku,Microsoft YaHei,25,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        
        ass_content = ass_header
        
        for danmaku in danmaku_data["danmaku_list"]:
            # 转换时间格式
            start_time = danmaku["time"] / 1000.0  # 毫秒转秒
            end_time = start_time + 3.0  # 弹幕显示3秒
            
            # 转换为ASS时间格式 (h:mm:ss.cc)
            start_ass = self._seconds_to_ass_time(start_time)
            end_ass = self._seconds_to_ass_time(end_time)
            
            # 根据弹幕模式设置效果
            effect = ""
            alignment = "2"  # 默认居中
            
            if danmaku["mode"] == 1:  # 滚动弹幕
                effect = "{\\move(1920,540,0,540)}"  # 从右到左滚动
            elif danmaku["mode"] == 5:  # 顶部弹幕
                alignment = "8"
                effect = "{\\pos(960,100)}"
            elif danmaku["mode"] == 4:  # 底部弹幕
                alignment = "2"
                effect = "{\\pos(960,980)}"
            
            # 颜色转换
            color = danmaku["color"]
            if isinstance(color, str):
                color = int(color)
            
            # 转换为ASS颜色格式 (BGR)
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            ass_color = f"&H00{b:02X}{g:02X}{r:02X}"
            
            # 文本内容
            text = danmaku["text"].replace('\n', '\\N')
            
            # 添加弹幕行
            ass_line = f"Dialogue: 0,{start_ass},{end_ass},Danmaku,,0,0,0,{effect}{{\\c{ass_color}\\fs{danmaku['fontsize']}}}{text}\n"
            ass_content += ass_line
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ass_content)
        
        return output_path
    
    def _seconds_to_ass_time(self, seconds: float) -> str:
        """将秒数转换为ASS时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}:{minutes:02d}:{secs:05.2f}"
    
    def create_video_with_danmaku(self, video_path: str, danmaku_file: str, 
                                output_path: str) -> str:
        """使用FFmpeg创建带弹幕的视频"""
        
        # 读取弹幕数据
        with open(danmaku_file, 'r', encoding='utf-8') as f:
            danmaku_data = json.load(f)
        
        # 获取视频时长
        import cv2
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 60
        cap.release()
        
        # 创建临时ASS字幕文件
        temp_ass = tempfile.NamedTemporaryFile(suffix='.ass', delete=False, mode='w', encoding='utf-8')
        temp_ass_path = temp_ass.name
        temp_ass.close()
        self.temp_files.append(temp_ass_path)
        
        self.create_ass_subtitle(danmaku_data, duration, temp_ass_path)
        
        # 构建FFmpeg命令
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"ass='{temp_ass_path}'",
            '-c:a', 'copy',
            '-c:v', 'libx264',
            '-crf', '23',
            '-preset', 'medium',
            '-y',  # 覆盖输出文件
            output_path
        ]
        
        print(f"🎬 正在生成带弹幕的视频...")
        print(f"📥 输入视频: {os.path.basename(video_path)}")
        print(f"💬 弹幕数量: {len(danmaku_data['danmaku_list'])}")
        print(f"📤 输出视频: {output_path}")
        
        try:
            # 执行FFmpeg命令
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print("✅ 视频生成成功!")
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"❌ FFmpeg错误: {e}")
            print(f"错误输出: {e.stderr}")
            return None
        
        except FileNotFoundError:
            print("❌ 未找到FFmpeg，请确保已安装FFmpeg")
            print("安装方法: brew install ffmpeg")
            return None
    
    def create_enhanced_video(self, video_path: str, danmaku_file: str, 
                            output_path: str, add_watermark: bool = True) -> str:
        """创建增强版视频（带弹幕、水印等）"""
        
        # 读取弹幕数据
        with open(danmaku_file, 'r', encoding='utf-8') as f:
            danmaku_data = json.load(f)
        
        # 创建ASS字幕文件
        temp_ass = tempfile.NamedTemporaryFile(suffix='.ass', delete=False, mode='w', encoding='utf-8')
        temp_ass_path = temp_ass.name
        temp_ass.close()
        self.temp_files.append(temp_ass_path)
        
        # 获取视频时长
        import cv2
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 60
        cap.release()
        
        self.create_ass_subtitle(danmaku_data, duration, temp_ass_path)
        
        # 构建复杂的FFmpeg滤镜链
        video_filters = []
        
        # 添加弹幕
        video_filters.append(f"ass='{temp_ass_path}'")
        
        # 添加水印（如果需要）
        if add_watermark:
            watermark_text = "Political Comedy • 政治喜剧"
            video_filters.append(
                f"drawtext=text='{watermark_text}':fontsize=20:fontcolor=white@0.7"
                ":x=w-tw-10:y=h-th-10:fontfile=/System/Library/Fonts/Arial.ttf"
            )
        
        # 组合滤镜
        filter_complex = ",".join(video_filters)
        
        # FFmpeg命令
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', filter_complex,
            '-c:a', 'copy',
            '-c:v', 'libx264',
            '-crf', '20',  # 高质量
            '-preset', 'medium',
            '-movflags', '+faststart',  # 优化流播放
            '-y',
            output_path
        ]
        
        print(f"🎨 正在生成增强版视频...")
        print(f"💬 弹幕数量: {len(danmaku_data['danmaku_list'])}")
        print(f"🏷️ 水印: {'启用' if add_watermark else '禁用'}")
        
        try:
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print("✅ 增强版视频生成成功!")
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 生成失败: {e}")
            if e.stderr:
                print(f"错误详情: {e.stderr}")
            return None
    
    def cleanup(self):
        """清理临时文件"""
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        self.temp_files.clear()
    
    def __del__(self):
        self.cleanup()


def main():
    """主函数"""
    processor = VideoDanmakuProcessor()
    
    # 输入文件
    video_path = "/Users/admin/IdeaProjects/video-processor/output/_jOTww0E0b4_Trump_seen_in_new_clip_released_by_filmmaker_following_Jan_6_committee_subpoena/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena.mp4"
    danmaku_file = "output/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena_jan6_special_danmaku.json"
    
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}")
        return
    
    if not os.path.exists(danmaku_file):
        print(f"❌ 弹幕文件不存在: {danmaku_file}")
        return
    
    # 输出文件
    output_basic = "output/trump_jan6_with_danmaku.mp4"
    output_enhanced = "output/trump_jan6_enhanced_with_danmaku.mp4"
    
    print("🎬 开始处理视频...")
    
    # 生成基础版本
    result1 = processor.create_video_with_danmaku(video_path, danmaku_file, output_basic)
    
    if result1:
        print(f"✅ 基础版本已保存: {output_basic}")
    
    # 生成增强版本
    result2 = processor.create_enhanced_video(video_path, danmaku_file, output_enhanced, add_watermark=True)
    
    if result2:
        print(f"✅ 增强版本已保存: {output_enhanced}")
    
    # 清理临时文件
    processor.cleanup()
    
    if result1 or result2:
        print("\n🎉 视频处理完成!")
        print("📋 生成的文件:")
        if result1:
            print(f"  - 基础版: {output_basic}")
        if result2:
            print(f"  - 增强版: {output_enhanced}")
        print("\n💡 你现在有了完整的带弹幕视频，可以直接上传到B站!")
    else:
        print("❌ 视频生成失败")


if __name__ == "__main__":
    main() 