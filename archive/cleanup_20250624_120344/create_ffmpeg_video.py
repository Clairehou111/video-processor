#!/usr/bin/env python3
"""
使用FFmpeg直接烧录字幕的版本 - 更好的QuickTime兼容性
"""

import os
import subprocess

def create_ffmpeg_subtitled_video():
    """使用ffmpeg创建带字幕的视频"""
    
    # 找到原始视频
    video_files = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith('.mp4') and 'final' not in file and 'test' not in file and 'ffmpeg' not in file:
                video_files.append(os.path.join("output", file))
    
    if not video_files:
        print("❌ 未找到原始视频文件")
        return None
    
    video_path = video_files[0]
    srt_path = "chinese_subtitles.srt"
    output_path = "output/ffmpeg_chinese_subtitles.mp4"
    
    if not os.path.exists(srt_path):
        print(f"❌ 字幕文件不存在: {srt_path}")
        return None
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 字幕文件: {srt_path}")
    
    try:
        # 使用ffmpeg命令烧录字幕
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1'",
            '-c:a', 'copy',  # 复制音频，不重新编码
            '-y',  # 覆盖输出文件
            output_path
        ]
        
        print("🔄 使用FFmpeg烧录字幕...")
        print(f"   执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ FFmpeg字幕视频生成成功!")
            print(f"   输出文件: {output_path}")
            
            # 显示文件信息
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024 / 1024
                print(f"   文件大小: {file_size:.2f} MB")
            
            return output_path
        else:
            print(f"❌ FFmpeg处理失败:")
            print(f"   错误输出: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ FFmpeg未安装，请先安装FFmpeg")
        print("   安装命令: brew install ffmpeg")
        return None
    except Exception as e:
        print(f"❌ FFmpeg处理出错: {e}")
        return None

if __name__ == "__main__":
    print("🎬 使用FFmpeg创建带中文字幕的视频")
    print("=" * 50)
    
    result = create_ffmpeg_subtitled_video()
    if result:
        print(f"\n🎉 任务完成!")
        print(f"🎬 FFmpeg版本的中文字幕视频已生成: {result}")
        print(f"\n💡 这个版本应该在QuickTime Player中正常显示字幕")
    else:
        print(f"\n❌ 视频生成失败") 