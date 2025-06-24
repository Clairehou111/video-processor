#!/usr/bin/env python3
"""
简单的双语字幕视频生成器
不需要ASS文件，直接使用SRT字幕文件 + FFmpeg force_style参数
"""

import subprocess
import sys
import os

def create_bilingual_video_simple(input_video, chinese_srt, english_srt, output_video):
    """
    使用两个独立的SRT文件创建双语视频
    中文字幕在上面（较大字体），英文字幕在下面（较小字体）
    考虑长字幕换行时的垂直空间需求
    """
    
    # 检查输入文件
    if not os.path.exists(input_video):
        print(f"错误: 输入视频不存在: {input_video}")
        return False
    if not os.path.exists(chinese_srt):
        print(f"错误: 中文字幕不存在: {chinese_srt}")
        return False
    if not os.path.exists(english_srt):
        print(f"错误: 英文字幕不存在: {english_srt}")
        return False
    
    # 水印和字体设置
    watermark_text = "董卓主演脱口秀"
    font_path = "/System/Library/Fonts/PingFang.ttc"
    
    # FFmpeg命令：使用两个字幕轨道，分别设置不同的样式
    cmd = [
        'ffmpeg', '-y',
        '-i', input_video,
        '-vf', (
            f"drawbox=x=10:y=10:w=320:h=100:color=black@0.8:t=fill,"
            f"drawbox=x=10:y=h-120:w=280:h=80:color=black@0.8:t=fill,"
            f"drawtext=text='{watermark_text}':fontfile={font_path}:fontsize=32:fontcolor=white:x=w-tw-30:y=30:alpha=0.9,"
            f"subtitles={chinese_srt}:force_style='FontSize=22,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=70,Alignment=2',"
            f"subtitles={english_srt}:force_style='FontSize=18,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=25,Alignment=2'"
        ),
        '-c:a', 'copy',
        output_video
    ]
    
    print(f"生成双语视频: {output_video}")
    print("中文字幕: 22px, MarginV=70 (考虑换行空间)")
    print("英文字幕: 18px, MarginV=25") 
    print("安全间距，避免长字幕重叠")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ 成功生成: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败: {e}")
        return False
    
    return True

def create_chinese_only_video(input_video, chinese_srt, output_video):
    """
    创建纯中文字幕视频
    """
    cmd = [
        'ffmpeg', '-y',
        '-i', input_video,
        '-vf', f"""
        drawbox=x=10:y=10:w=320:h=100:color=black@0.8:t=fill,
        drawbox=x=10:y=h-120:w=280:h=80:color=black@0.8:t=fill,
        drawtext=text='董卓主演脱口秀':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=32:fontcolor=white:x=w-tw-30:y=30:alpha=0.9,
        subtitles={chinese_srt}:force_style='FontSize=26,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=20,Alignment=2'
        """.replace('\n        ', ''),
        '-c:a', 'copy',
        output_video
    ]
    
    print(f"生成中文字幕视频: {output_video}")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ 成功生成: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # 输入文件
    input_video = "output/clean_segment_2m36s-5m59s.mp4"
    chinese_srt = "output/VP9_segment_2m36s-5m59s_chinese.srt"
    english_srt = "output/VP9_segment_2m36s-5m59s_english.srt"
    
    # 输出文件
    bilingual_output = "output/simple_bilingual_video.mp4"
    chinese_output = "output/simple_chinese_video.mp4"
    
    print("=== 简单双语字幕视频生成器 ===")
    print("优势：")
    print("✅ 不需要生成ASS文件")
    print("✅ 直接使用现有的SRT字幕文件")
    print("✅ 通过FFmpeg参数控制字体大小和位置")
    print("✅ 中文22px在上，英文18px在下")
    print("✅ 自动遮盖Daily Show标记")
    print()
    
    # 生成双语版本
    print("1. 生成双语版本...")
    create_bilingual_video_simple(input_video, chinese_srt, english_srt, bilingual_output)
    print()
    
    # 生成纯中文版本
    print("2. 生成纯中文版本...")
    create_chinese_only_video(input_video, chinese_srt, chinese_output)
    print()
    
    print("=== 完成！===")
    print(f"双语版本: {bilingual_output}")
    print(f"中文版本: {chinese_output}") 