#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的YouTube视频时间段下载器
使用yt-dlp的内置时间段下载功能
"""

import os
import subprocess

def download_video_segment_simple(url, start_time, end_time, quality="720p"):
    """使用yt-dlp直接下载指定时间段的视频"""
    print("=" * 60)
    print("🎬 YouTube视频时间段下载器 (yt-dlp内置功能)")
    print("=" * 60)
    print(f"🔗 视频URL: {url}")
    print(f"⏰ 时间窗口: {start_time} - {end_time}")
    print(f"📺 视频质量: {quality}")
    print()
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 选择视频质量
    if quality == "best":
        format_selector = 'best'
    elif quality == "1080p":
        format_selector = 'best[height<=1080]'
    elif quality == "720p":
        format_selector = 'best[height<=720]'
    elif quality == "480p":
        format_selector = 'best[height<=480]'
    else:
        format_selector = 'best[height<=720]'
    
    # 使用yt-dlp的download-sections功能
    cmd = [
        "yt-dlp",
        "--download-sections", f"*{start_time}-{end_time}",
        "--format", format_selector,
        "--output", f"{output_dir}/%(title)s_segment_{start_time.replace(':', '')}-{end_time.replace(':', '')}.%(ext)s",
        url
    ]
    
    print("🔄 开始下载视频片段...")
    print(f"执行命令: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ 视频片段下载成功！")
        print("输出信息:")
        print(result.stdout)
        
        # 查找下载的文件
        for file in os.listdir(output_dir):
            if "segment" in file:
                print(f"📁 下载文件: {os.path.join(output_dir, file)}")
                return os.path.join(output_dir, file)
        
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 下载失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None

def main():
    """主函数"""
    # 你指定的视频参数
    youtube_url = "https://www.youtube.com/watch?v=smemFVe0l5E&t=3424s"
    start_time = "50:00"  # 50分0秒
    end_time = "50:35"    # 50分35秒
    quality = "720p"      # 视频质量
    
    result = download_video_segment_simple(
        url=youtube_url,
        start_time=start_time,
        end_time=end_time,
        quality=quality
    )
    
    if result:
        print(f"\n🎉 视频段下载完成: {result}")
    else:
        print(f"\n💥 下载失败")

if __name__ == "__main__":
    main() 