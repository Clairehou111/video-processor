#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接YouTube视频时间段下载器
分步骤：下载 -> 切片
"""

import os
import sys

def main():
    """主函数"""
    print("=" * 60)
    print("🎬 YouTube视频时间段下载器")
    print("=" * 60)
    
    # 视频参数
    youtube_url = "https://www.youtube.com/watch?v=smemFVe0l5E"
    start_time = "50:00"  # 50分0秒
    end_time = "50:35"    # 50分35秒
    
    print(f"🔗 视频URL: {youtube_url}")
    print(f"⏰ 时间窗口: {start_time} - {end_time}")
    print()
    
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    print("方法1: 使用yt-dlp的时间段下载功能")
    print("执行以下命令:")
    print()
    
    cmd1 = f'''yt-dlp --download-sections "*{start_time}-{end_time}" --format "best[height<=720]" --output "output/%(title)s_segment_{start_time.replace(':', '')}-{end_time.replace(':', '')}.%(ext)s" "{youtube_url}"'''
    
    print(f"命令: {cmd1}")
    print()
    
    print("=" * 60)
    print("方法2: 分步骤下载和切片")
    print("=" * 60)
    print()
    
    print("步骤1: 下载完整视频")
    cmd2 = f'''yt-dlp --format "best[height<=720]" --output "output/temp_full_video.%(ext)s" "{youtube_url}"'''
    print(f"命令: {cmd2}")
    print()
    
    print("步骤2: 使用ffmpeg切片")
    cmd3 = f'''ffmpeg -i output/temp_full_video.mp4 -ss {start_time} -to {end_time} -c copy output/video_segment_{start_time.replace(':', '')}-{end_time.replace(':', '')}.mp4'''
    print(f"命令: {cmd3}")
    print()
    
    print("步骤3: 清理临时文件")
    cmd4 = "rm output/temp_full_video.mp4"
    print(f"命令: {cmd4}")
    print()
    
    print("=" * 60)
    print("方法3: 直接使用ffmpeg和yt-dlp流")
    print("=" * 60)
    print()
    
    cmd5 = f'''yt-dlp -f "best[height<=720]" -o - "{youtube_url}" | ffmpeg -i pipe: -ss {start_time} -to {end_time} -c copy output/piped_segment_{start_time.replace(':', '')}-{end_time.replace(':', '')}.mp4'''
    print(f"命令: {cmd5}")
    print()
    
    print("选择一种方法执行即可。推荐使用方法1或方法2。")
    print("如果网络不稳定，可以试试方法2，分步骤进行。")

if __name__ == "__main__":
    main() 