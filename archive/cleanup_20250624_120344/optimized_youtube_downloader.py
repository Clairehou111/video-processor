#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化的YouTube下载器
统一使用高质量参数：--format "bestvideo[height>=1080]+bestaudio/best[height>=1080]"
支持完整视频和部分切片下载
"""

import os
import sys
import subprocess
import time
import yt_dlp
from pathlib import Path

class OptimizedYouTubeDownloader:
    """优化的YouTube下载器"""
    
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 统一的高质量格式参数
        self.HIGH_QUALITY_FORMAT = "bestvideo[height>=1080]+bestaudio/best[height>=1080]"
        
    def time_to_seconds(self, time_str):
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
    
    def download_full_video(self, url, show_formats=False):
        """下载完整视频 - 使用统一高质量参数"""
        print("🎬 完整视频下载")
        print("=" * 50)
        print(f"🔗 视频URL: {url}")
        print(f"📊 质量参数: {self.HIGH_QUALITY_FORMAT}")
        print()
        
        # 如果需要，先显示所有可用格式
        if show_formats:
            print("📋 查看可用格式...")
            list_opts = {'listformats': True}
            try:
                with yt_dlp.YoutubeDL(list_opts) as ydl:
                    ydl.extract_info(url, download=False)
            except:
                pass
            print("\n" + "="*50)
        
        ydl_opts = {
            'format': self.HIGH_QUALITY_FORMAT,
            'outtmpl': os.path.join(self.output_dir, '%(title)s_HQ.%(ext)s'),
            'writesubtitles': False,
            'writeautomaticsub': False,
            'prefer_ffmpeg': True,
            'merge_output_format': 'mp4',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("🔄 开始下载...")
                info = ydl.extract_info(url, download=True)
                video_title = info['title']
                video_ext = info['ext']
                video_path = os.path.join(self.output_dir, f"{video_title}_HQ.{video_ext}")
                
                print(f"✅ 完整视频下载成功!")
                self._print_video_info(info, video_path)
                return video_path, video_title
                
        except Exception as e:
            print(f"❌ 下载失败: {str(e)}")
            return None, None
    
    def download_video_segment(self, url, start_time, end_time, method="direct"):
        """下载视频片段 - 使用统一高质量参数"""
        print("✂️ 视频片段下载")
        print("=" * 50)
        print(f"🔗 视频URL: {url}")
        print(f"⏰ 时间窗口: {start_time} - {end_time}")
        print(f"📊 质量参数: {self.HIGH_QUALITY_FORMAT}")
        print(f"🛠️ 下载方法: {method}")
        print()
        
        if method == "direct":
            return self._download_segment_direct(url, start_time, end_time)
        elif method == "ffmpeg":
            return self._download_segment_ffmpeg(url, start_time, end_time)
        else:
            print(f"❌ 不支持的方法: {method}")
            return None, None
    
    def _download_segment_direct(self, url, start_time, end_time):
        """直接下载片段 - 使用yt-dlp的时间参数"""
        ydl_opts = {
            'format': self.HIGH_QUALITY_FORMAT,
            'outtmpl': os.path.join(self.output_dir, '%(title)s_segment_HQ.%(ext)s'),
            'writesubtitles': False,
            'writeautomaticsub': False,
            'external_downloader': 'ffmpeg',
            'external_downloader_args': ['-ss', start_time, '-to', end_time],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("🔄 开始直接下载片段...")
                info = ydl.extract_info(url, download=True)
                video_title = info['title']
                video_ext = info['ext']
                video_path = os.path.join(self.output_dir, f"{video_title}_segment_HQ.{video_ext}")
                
                print(f"✅ 片段下载成功!")
                self._print_video_info(info, video_path)
                return video_path, video_title
                
        except Exception as e:
            print(f"❌ 直接下载失败: {str(e)}")
            print("🔄 尝试备用方法...")
            return self._download_segment_ffmpeg(url, start_time, end_time)
    
    def _download_segment_ffmpeg(self, url, start_time, end_time):
        """使用ffmpeg切片方法下载片段"""
        print("🔄 使用ffmpeg切片方法...")
        
        # 第一步：下载完整视频
        temp_path = os.path.join(self.output_dir, "temp_full_video.%(ext)s")
        
        ydl_opts = {
            'format': self.HIGH_QUALITY_FORMAT,
            'outtmpl': temp_path,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'prefer_ffmpeg': True,
            'merge_output_format': 'mp4',
        }
        
        try:
            # 下载完整视频
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("📥 下载完整视频...")
                info = ydl.extract_info(url, download=True)
                video_title = info['title']
                video_ext = info['ext']
                
                downloaded_file = os.path.join(self.output_dir, f"temp_full_video.{video_ext}")
                
            # 使用ffmpeg切片
            print(f"✂️ 切片时间段: {start_time} - {end_time}")
            
            clean_title = video_title.replace('/', '-').replace('\\', '-')
            output_filename = f"{clean_title}_segment_HQ_{start_time.replace(':', '')}-{end_time.replace(':', '')}.mp4"
            output_path = os.path.join(self.output_dir, output_filename)
            
            ffmpeg_cmd = [
                'ffmpeg', '-y',
                '-i', downloaded_file,
                '-ss', start_time,
                '-to', end_time,
                '-c', 'copy',  # 快速复制，保持原质量
                output_path
            ]
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            
            # 清理临时文件
            os.remove(downloaded_file)
            
            print(f"✅ 片段切片成功!")
            self._print_segment_info(output_path, start_time, end_time)
            return output_path, video_title
            
        except subprocess.CalledProcessError as e:
            print(f"❌ ffmpeg切片失败: {e}")
            return None, None
        except Exception as e:
            print(f"❌ 切片过程出错: {str(e)}")
            return None, None
    
    def _print_video_info(self, info, video_path):
        """打印视频信息"""
        print("📊 视频信息:")
        print(f"   📺 分辨率: {info.get('width', 'N/A')}x{info.get('height', 'N/A')}")
        print(f"   🎯 格式ID: {info.get('format_id', 'N/A')}")
        print(f"   📈 视频码率: {info.get('vbr', 'N/A')} kbps")
        print(f"   🔊 音频码率: {info.get('abr', 'N/A')} kbps")
        print(f"   ⚙️ 编码器: {info.get('vcodec', 'N/A')} / {info.get('acodec', 'N/A')}")
        
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / (1024*1024)
            print(f"   📦 文件大小: {file_size:.2f} MB")
        
        print(f"   📁 保存路径: {video_path}")
    
    def _print_segment_info(self, video_path, start_time, end_time):
        """打印片段信息"""
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / (1024*1024)
            print("📊 片段信息:")
            print(f"   ⏰ 时间段: {start_time} - {end_time}")
            print(f"   📦 文件大小: {file_size:.2f} MB")
            print(f"   📁 保存路径: {video_path}")

def main():
    """主函数"""
    print("🎯 优化的YouTube下载器")
    print("=" * 60)
    print("✨ 特点:")
    print("   • 统一使用高质量参数")
    print("   • 支持完整视频和片段下载")
    print("   • 多种下载策略")
    print("   • 详细的质量信息显示")
    print()
    
    downloader = OptimizedYouTubeDownloader()
    
    # 获取用户输入
    youtube_url = input("🔗 请输入YouTube视频URL: ").strip()
    if not youtube_url:
        print("❌ 必须提供视频URL")
        return
    
    # 选择下载类型
    print("\n📋 选择下载类型:")
    print("1. 完整视频下载")
    print("2. 视频片段下载")
    print("3. 查看格式后下载完整视频")
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == "1":
        # 完整视频下载
        video_path, video_title = downloader.download_full_video(youtube_url)
        
    elif choice == "2":
        # 片段下载
        start_time = input("🕐 请输入开始时间 (格式: MM:SS 或 HH:MM:SS): ").strip()
        end_time = input("🕑 请输入结束时间 (格式: MM:SS 或 HH:MM:SS): ").strip()
        
        if not start_time or not end_time:
            print("❌ 必须提供开始和结束时间")
            return
        
        print("\n🛠️ 选择下载方法:")
        print("1. 直接下载 (推荐)")
        print("2. ffmpeg切片")
        
        method_choice = input("请选择方法 (1-2): ").strip()
        method = "direct" if method_choice == "1" else "ffmpeg"
        
        video_path, video_title = downloader.download_video_segment(
            youtube_url, start_time, end_time, method
        )
        
    elif choice == "3":
        # 查看格式后下载
        video_path, video_title = downloader.download_full_video(youtube_url, show_formats=True)
        
    else:
        print("❌ 无效选择")
        return
    
    if video_path:
        print(f"\n🎉 下载完成!")
        print(f"📁 输出目录: {downloader.output_dir}")
    else:
        print(f"\n❌ 下载失败")

if __name__ == "__main__":
    main() 