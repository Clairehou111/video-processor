#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube视频时间段下载器
先下载完整视频，然后切片指定时间段
"""

import os
import subprocess
import time
import yt_dlp

def time_to_seconds(time_str):
    """将时间格式 (MM:SS 或 HH:MM:SS) 转换为秒数"""
    parts = time_str.split(':')
    if len(parts) == 2:  # MM:SS
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"无效的时间格式: {time_str}")

def download_and_clip_video(url, start_time, end_time, quality="720p"):
    """下载视频并切片指定时间段"""
    print("=" * 60)
    print("🎬 YouTube视频时间段下载器")
    print("=" * 60)
    print(f"🔗 视频URL: {url}")
    print(f"⏰ 时间窗口: {start_time} - {end_time}")
    print(f"📺 视频质量: {quality}")
    print()
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 第一步：下载完整视频
    print("📥 第一步：下载完整视频...")
    
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
    
    temp_video_path = os.path.join(output_dir, "temp_full_video.%(ext)s")
    
    ydl_opts = {
        'format': format_selector,
        'outtmpl': temp_video_path,
        'writesubtitles': False,
        'writeautomaticsub': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info['title']
            video_ext = info['ext']
            
            # 找到下载的文件
            downloaded_file = os.path.join(output_dir, f"temp_full_video.{video_ext}")
            
            print(f"✅ 视频下载完成: {downloaded_file}")
            print(f"📝 视频标题: {video_title}")
            
    except Exception as e:
        print(f"❌ 视频下载失败: {str(e)}")
        return None
    
    # 第二步：使用ffmpeg切片
    print(f"\n✂️ 第二步：切片视频 ({start_time} - {end_time})...")
    
    # 计算时长
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)
    duration = end_seconds - start_seconds
    
    # 创建输出文件名
    clean_title = video_title.replace('/', '-').replace('\\', '-')
    output_filename = f"{clean_title}_segment_{start_time.replace(':', '')}_{end_time.replace(':', '')}.mp4"
    output_path = os.path.join(output_dir, output_filename)
    
    # 使用ffmpeg切片
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', downloaded_file,
        '-ss', str(start_seconds),
        '-t', str(duration),
        '-c', 'copy',  # 快速复制，不重新编码
        output_path
    ]
    
    try:
        print(f"🔄 正在切片 {duration} 秒片段...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        print(f"✅ 视频切片完成: {output_path}")
        
        # 清理临时文件
        os.remove(downloaded_file)
        print("🗑️ 清理临时文件")
        
        return output_path, video_title
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 视频切片失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None, None
    except Exception as e:
        print(f"❌ 切片过程中出错: {str(e)}")
        return None, None

def main():
    """主函数"""
    # 你指定的视频参数
    youtube_url = "https://www.youtube.com/watch?v=smemFVe0l5E&t=3424s"
    start_time = "50:00"  # 50分0秒
    end_time = "50:35"    # 50分35秒
    quality = "720p"      # 视频质量
    
    result = download_and_clip_video(
        url=youtube_url,
        start_time=start_time,
        end_time=end_time,
        quality=quality
    )
    
    if result and result[0]:
        print(f"\n🎉 视频段下载完成: {result[0]}")
        print(f"📝 视频标题: {result[1]}")
    else:
        print(f"\n💥 下载失败")

if __name__ == "__main__":
    main() 