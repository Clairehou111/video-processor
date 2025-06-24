#!/usr/bin/env python3
"""
创建同时显示英文和中文字幕的视频
英文字幕在上方，中文字幕在下方
"""

import os
import subprocess

def create_dual_subtitles_video():
    """使用ffmpeg创建双语字幕视频"""
    
    # 找到原始视频
    video_files = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith('.mp4') and 'final' not in file and 'test' not in file and 'ffmpeg' not in file and 'dual' not in file:
                video_files.append(os.path.join("output", file))
    
    if not video_files:
        print("❌ 未找到原始视频文件")
        return None
    
    video_path = video_files[0]
    english_srt = None
    chinese_srt = "chinese_subtitles.srt"
    
    # 查找英文字幕文件
    for file in os.listdir("output"):
        if file.endswith("_english.srt"):
            english_srt = os.path.join("output", file)
            break
    
    if not english_srt or not os.path.exists(english_srt):
        print("❌ 未找到英文字幕文件")
        return None
    
    if not os.path.exists(chinese_srt):
        print(f"❌ 中文字幕文件不存在: {chinese_srt}")
        return None
    
    output_path = "output/dual_subtitles_video.mp4"
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 英文字幕: {english_srt}")
    print(f"📝 中文字幕: {chinese_srt}")
    
    try:
        # 使用ffmpeg命令烧录双语字幕
        # 英文字幕在上方 (MarginV=100)，中文字幕在下方 (MarginV=10)
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', 
            f"subtitles={english_srt}:force_style='FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=100,Alignment=2',"
            f"subtitles={chinese_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=10,Alignment=2'",
            '-c:a', 'copy',  # 复制音频，不重新编码
            '-y',  # 覆盖输出文件
            output_path
        ]
        
        print("🔄 使用FFmpeg烧录双语字幕...")
        print("   英文字幕: 白色，位置较高")
        print("   中文字幕: 黄色，位置较低")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 双语字幕视频生成成功!")
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
        return None
    except Exception as e:
        print(f"❌ FFmpeg处理出错: {e}")
        return None

def create_options_menu():
    """创建选项菜单"""
    print("🎬 字幕视频生成选项")
    print("=" * 40)
    print("1. 只显示中文字幕 (已生成)")
    print("2. 只显示英文字幕")
    print("3. 显示双语字幕 (英文上方，中文下方)")
    print("4. 退出")
    
    choice = input("\n请选择 (1-4): ").strip()
    return choice

def create_english_only_video():
    """创建只有英文字幕的视频"""
    
    # 找到原始视频
    video_files = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith('.mp4') and 'final' not in file and 'test' not in file and 'ffmpeg' not in file and 'dual' not in file and 'english' not in file:
                video_files.append(os.path.join("output", file))
    
    if not video_files:
        print("❌ 未找到原始视频文件")
        return None
    
    video_path = video_files[0]
    english_srt = None
    
    # 查找英文字幕文件
    for file in os.listdir("output"):
        if file.endswith("_english.srt"):
            english_srt = os.path.join("output", file)
            break
    
    if not english_srt or not os.path.exists(english_srt):
        print("❌ 未找到英文字幕文件")
        return None
    
    output_path = "output/english_subtitles_video.mp4"
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 英文字幕: {english_srt}")
    
    try:
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"subtitles={english_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1'",
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        print("🔄 使用FFmpeg烧录英文字幕...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 英文字幕视频生成成功!")
            print(f"   输出文件: {output_path}")
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024 / 1024
                print(f"   文件大小: {file_size:.2f} MB")
            
            return output_path
        else:
            print(f"❌ FFmpeg处理失败: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 处理出错: {e}")
        return None

if __name__ == "__main__":
    while True:
        choice = create_options_menu()
        
        if choice == '1':
            print("✅ 中文字幕视频已经生成: output/ffmpeg_chinese_subtitles.mp4")
            break
        elif choice == '2':
            result = create_english_only_video()
            if result:
                print(f"🎉 英文字幕视频生成完成: {result}")
            break
        elif choice == '3':
            result = create_dual_subtitles_video()
            if result:
                print(f"🎉 双语字幕视频生成完成: {result}")
            break
        elif choice == '4':
            print("👋 退出")
            break
        else:
            print("❌ 无效选择，请重新输入") 