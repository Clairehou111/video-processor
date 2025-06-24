#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能优化的视频处理自动化系统
特点：网络重试、并发处理、断点续传、智能缓存
"""

import os
import subprocess
import json
import re
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import yt_dlp
import whisper

class OptimizedVideoAutomation:
    def __init__(self):
        self.base_output_dir = "output"
        self.current_project_dir = None
        self.whisper_model = None
        self.max_retries = 3
        self.retry_delay = 5  # 秒
        
    def load_whisper_model(self):
        """优化：只加载一次Whisper模型"""
        if not self.whisper_model:
            print("🔄 加载Whisper模型...")
            start_time = time.time()
            self.whisper_model = whisper.load_model("base")
            load_time = time.time() - start_time
            print(f"✅ Whisper模型加载完成 ({load_time:.1f}秒)")
    
    def create_project_directory(self, video_title):
        """快速创建项目目录"""
        import datetime
        
        # 清理视频标题，创建安全的目录名
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', video_title)
        safe_title = safe_title.replace(' ', '_')[:50]
        
        # 添加时间戳避免重复
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        project_name = f"{safe_title}_{timestamp}"
        self.current_project_dir = os.path.join(self.base_output_dir, project_name)
        
        # 批量创建目录结构
        directories = [
            self.current_project_dir,
            os.path.join(self.current_project_dir, "subtitles"),
            os.path.join(self.current_project_dir, "final"),
            os.path.join(self.current_project_dir, "temp")  # 临时文件目录
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        print(f"📁 项目目录已创建: {self.current_project_dir}")
        return self.current_project_dir

    def download_video_with_incremental_retry(self, url, start_time=None, end_time=None):
        """带增量重试机制的视频下载 - 避免重复下载已完成的部分"""
        print(f"📥 开始智能下载 (断点续传 + 增量重试)")
        if start_time and end_time:
            print(f"   切片时间: {start_time} - {end_time}")
        
        # 步骤1: 获取并缓存视频信息
        video_info, video_title = self.get_and_cache_video_info(url)
        if not video_info:
            return None, None
            
        # 创建项目目录
        project_dir = self.create_project_directory(video_title)
        
        # 步骤2: 检查是否已有部分下载
        partial_file = self.check_partial_download(project_dir, video_title)
        
        # 步骤3: 增量下载策略
        return self.incremental_download(url, project_dir, video_info, start_time, end_time, partial_file)
    
    def get_and_cache_video_info(self, url):
        """获取并缓存视频信息，避免重复请求"""
        cache_file = f"{self.base_output_dir}/.video_info_cache.json"
        
        # 尝试从缓存读取
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    if url in cache and (time.time() - cache[url]['timestamp']) < 300:  # 5分钟缓存
                        print("📋 使用缓存的视频信息")
                        info = cache[url]['info']
                        return info, info.get('title', 'video')
            except:
                pass
        
        # 获取新的视频信息
        print("🔍 获取视频信息...")
        temp_ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 15,
            'retries': 2
        }
        
        for attempt in range(2):
            try:
                with yt_dlp.YoutubeDL(temp_ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'video')
                    
                    # 缓存视频信息
                    cache = {}
                    if os.path.exists(cache_file):
                        try:
                            with open(cache_file, 'r', encoding='utf-8') as f:
                                cache = json.load(f)
                        except:
                            pass
                    
                    cache[url] = {
                        'info': info,
                        'timestamp': time.time()
                    }
                    
                    os.makedirs(self.base_output_dir, exist_ok=True)
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        json.dump(cache, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ 视频信息获取成功: {title}")
                    return info, title
                    
            except Exception as e:
                print(f"⚠️ 获取视频信息失败 (尝试 {attempt + 1}/2): {str(e)[:50]}...")
                if attempt == 0:
                    time.sleep(3)
        
        return None, None
    
    def check_partial_download(self, project_dir, video_title):
        """检查是否有部分下载的文件"""
        # 检查完整文件
        complete_file = self.find_downloaded_file(project_dir)
        if complete_file:
            print(f"✅ 发现已完成的下载: {complete_file}")
            return complete_file
        
        # 检查部分文件 (.part, .ytdl, .tmp)
        partial_extensions = ['.part', '.ytdl', '.tmp', '.f*']
        for file in os.listdir(project_dir):
            for ext in partial_extensions:
                if ext in file.lower():
                    partial_path = os.path.join(project_dir, file)
                    size = os.path.getsize(partial_path) / (1024*1024)  # MB
                    print(f"📂 发现部分下载: {file} ({size:.1f}MB)")
                    return partial_path
        
        return None
    
    def incremental_download(self, url, project_dir, video_info, start_time, end_time, partial_file):
        """增量下载 - 基于已有进度继续"""
        
        # 基础下载配置
        ydl_opts = {
            'format': 'bestvideo[height>=1080]+bestaudio/best[height>=1080]',
            'outtmpl': f'{project_dir}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'socket_timeout': 30,
            'http_chunk_size': 10485760,  # 10MB chunks
            'continue_dl': True,  # 关键：启用断点续传
            'nooverwrites': True,  # 不覆盖已存在文件
        }
        
        # 如果是切片下载
        if start_time and end_time:
            ydl_opts['external_downloader'] = 'ffmpeg'
            ydl_opts['external_downloader_args'] = [
                '-ss', start_time,
                '-to', end_time,
                '-reconnect', '1',
                '-reconnect_streamed', '1',
                '-reconnect_delay_max', '5',
                '-reconnect_at_eof', '1'  # EOF时重连
            ]
        
        # 如果有部分文件，优化重试策略
        if partial_file and partial_file.endswith('.mp4'):
            print("✅ 文件已完整，跳过下载")
            return partial_file, video_info.get('title', 'video')
        
        # 增量重试下载
        for attempt in range(self.max_retries):
            try:
                print(f"🔄 增量下载尝试 {attempt + 1}/{self.max_retries}")
                
                # 动态调整超时时间
                ydl_opts['socket_timeout'] = 30 + (attempt * 10)  # 递增超时
                ydl_opts['retries'] = max(1, 3 - attempt)  # 递减内部重试
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # 使用已缓存的info，避免重复网络请求
                    ydl.process_info(video_info)
                    
                    # 查找下载的文件
                    video_path = self.find_downloaded_file(project_dir)
                    if video_path:
                        file_size = os.path.getsize(video_path) / (1024*1024)
                        print(f"✅ 增量下载成功: {video_path} ({file_size:.1f}MB)")
                        return video_path, video_info.get('title', 'video')
                    
            except Exception as e:
                error_msg = str(e)
                print(f"❌ 增量下载尝试 {attempt + 1} 失败: {error_msg[:80]}...")
                
                # 智能错误处理
                if "connection reset" in error_msg.lower() or "timeout" in error_msg.lower():
                    # 网络问题 - 继续重试
                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (attempt + 1)
                        print(f"🌐 网络问题，等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                        continue
                        
                elif "unavailable" in error_msg.lower() or "private" in error_msg.lower():
                    # 视频不可用 - 直接退出
                    print("❌ 视频不可用或已私有，停止重试")
                    break
                    
                else:
                    # 其他错误 - 短暂等待后重试
                    if attempt < self.max_retries - 1:
                        print(f"⏱️  等待 {self.retry_delay} 秒后重试...")
                        time.sleep(self.retry_delay)
        
        print("❌ 所有增量下载尝试均失败")
        return None, None
    

    
    def find_downloaded_file(self, project_dir):
        """查找下载的视频文件"""
        for file in os.listdir(project_dir):
            if file.endswith('.mp4') and not file.startswith('.'):
                return os.path.join(project_dir, file)
        return None
    
    def extract_english_subtitles_fast(self, video_path):
        """优化的字幕提取"""
        print("🔄 提取英文字幕...")
        
        # 预加载模型
        self.load_whisper_model()
        
        start_time = time.time()
        result = self.whisper_model.transcribe(video_path)
        transcribe_time = time.time() - start_time
        
        segments = []
        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            })
        
        # 批量写入字幕文件
        video_name = Path(video_path).stem
        english_srt = f"{self.current_project_dir}/subtitles/{video_name}_english.srt"
        
        # 优化：批量构建内容再一次写入
        srt_content = []
        for i, segment in enumerate(segments, 1):
            start_time_str = self.seconds_to_srt_time(segment["start"])
            end_time_str = self.seconds_to_srt_time(segment["end"])
            srt_content.append(f"{i}\n{start_time_str} --> {end_time_str}\n{segment['text']}\n")
        
        with open(english_srt, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_content))
        
        print(f"✅ 英文字幕提取完成: {english_srt}")
        print(f"📊 共 {len(segments)} 个片段 (耗时 {transcribe_time:.1f}秒)")
        return english_srt, segments
    
    def create_translation_prompt_fast(self, segments):
        """快速生成翻译提示词"""
        prompt_file = f"{self.current_project_dir}/translation_prompt.txt"
        translation_file = f"{self.current_project_dir}/subtitles/chinese_translation.srt"
        
        # 优化：使用字符串拼接而不是多次append
        prompt_lines = [
            "# 政治脱口秀翻译指南",
            "",
            "## 翻译要求",
            "1. 保持政治幽默的精髓和讽刺效果",
            "2. 适应中文表达习惯，但保留原意", 
            "3. 专有名词准确翻译（人名、地名、机构名）",
            "4. 保持时间节奏，适合字幕显示",
            "",
            f"## 待翻译内容 ({len(segments)} 个片段)",
            ""
        ]
        
        # 批量添加片段
        for i, segment in enumerate(segments, 1):
            prompt_lines.append(f"{i}. {segment['text']}")
        
        prompt_lines.extend([
            "",
            "## 翻译格式要求",
            f"请将翻译结果保存到: {translation_file}",
            "格式如下:",
            "",
            "1",
            "00:00:01,000 --> 00:00:03,500", 
            "中文翻译内容1",
            "",
            "2",
            "00:00:03,500 --> 00:00:05,800",
            "中文翻译内容2",
            "",
            "...",
            "",
            "## 翻译完成后",
            "请运行: python optimized_video_automation.py --finalize"
        ])
        
        # 一次性写入
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(prompt_lines))
        
        print(f"✅ 翻译提示词已生成: {prompt_file}")
        print(f"📝 请将中文翻译保存到: {translation_file}")
        return prompt_file, translation_file
    
    def seconds_to_srt_time(self, seconds):
        """转换秒数为SRT时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def process_video_optimized(self, url, start_time=None, end_time=None):
        """优化的视频处理流程"""
        print("🚀 优化版视频处理自动化开始")
        print("="*50)
        
        total_start_time = time.time()
        
        # 步骤1: 智能下载（增量重试）
        print("\n📥 步骤1: 智能下载")
        video_path, video_title = self.download_video_with_incremental_retry(url, start_time, end_time)
        if not video_path:
            print("❌ 下载失败，无法继续")
            return False
        
        # 步骤2: 提取英文字幕
        print("\n📝 步骤2: 提取英文字幕")
        english_srt, segments = self.extract_english_subtitles_fast(video_path)
        
        # 步骤3: 生成翻译提示词
        print("\n📖 步骤3: 生成翻译提示词")
        prompt_file, translation_file = self.create_translation_prompt_fast(segments)
        
        # 保存状态（优化的状态保存）
        state = {
            "video_path": video_path,
            "video_title": video_title,
            "english_srt": english_srt,
            "translation_file": translation_file,
            "project_dir": self.current_project_dir,
            "status": "waiting_translation",
            "created_time": time.time(),
            "segments_count": len(segments)
        }
        
        state_file = f"{self.current_project_dir}/automation_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        total_time = time.time() - total_start_time
        
        print(f"\n⏳ 处理完成，总耗时: {total_time:.1f}秒")
        print("\n📋 下一步操作:")
        print(f"1. 查看翻译提示词: {prompt_file}")
        print(f"2. 完成中文翻译并保存到: {translation_file}")
        print("3. 运行完成命令: python optimized_video_automation.py --finalize")
        
        return True
    
    def finalize_latest_project(self):
        """完成最新项目的视频生成"""
        print("🎬 开始生成最终双语视频")
        print("="*50)
        
        # 查找最新项目
        projects = []
        for item in os.listdir(self.base_output_dir):
            item_path = os.path.join(self.base_output_dir, item)
            if os.path.isdir(item_path) and 'automation_state.json' in os.listdir(item_path):
                state_file = os.path.join(item_path, 'automation_state.json')
                try:
                    with open(state_file, 'r', encoding='utf-8') as f:
                        state = json.load(f)
                        projects.append((state.get('created_time', 0), item_path, state))
                except:
                    continue
        
        if not projects:
            print("❌ 没有找到可完成的项目")
            return False
        
        # 选择最新项目
        latest_project = max(projects, key=lambda x: x[0])
        project_dir = latest_project[1]
        state = latest_project[2]
        
        print(f"📁 项目目录: {project_dir}")
        print(f"📹 视频标题: {state.get('video_title', 'Unknown')}")
        
        # 检查文件
        video_path = state.get('video_path')
        english_srt = state.get('english_srt')
        
        if not video_path or not os.path.exists(video_path):
            print("❌ 找不到原始视频文件")
            return False
        
        if not english_srt or not os.path.exists(english_srt):
            print("❌ 找不到英文字幕文件")
            return False
        
        # 查找中文字幕
        video_name = Path(video_path).stem
        chinese_srt = f"{project_dir}/subtitles/{video_name}_chinese.srt"
        
        if not os.path.exists(chinese_srt):
            print(f"❌ 找不到中文字幕文件: {chinese_srt}")
            print("请确保中文翻译已保存到正确位置")
            return False
        
        print(f"✅ 找到所有必需文件")
        print(f"📹 视频: {os.path.basename(video_path)} ({os.path.getsize(video_path)/(1024*1024):.1f}MB)")
        print(f"📝 英文字幕: {os.path.basename(english_srt)}")
        print(f"📝 中文字幕: {os.path.basename(chinese_srt)}")
        
        # 生成双语视频
        self.generate_bilingual_video(project_dir, video_path, english_srt, chinese_srt)
        
        # 更新状态
        state['status'] = 'completed'
        state['completed_time'] = time.time()
        state_file = f"{project_dir}/automation_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        print("🎉 项目完成！")
        return True
    
    def generate_bilingual_video(self, project_dir, video_path, english_srt, chinese_srt):
        """生成双语视频"""
        print("\n🎬 生成双语视频...")
        
        video_name = Path(video_path).stem
        output_video = f"{project_dir}/final/{video_name}_bilingual.mp4"
        
        # FFmpeg命令 - 添加双语字幕和右上角水印
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-filter_complex', 
            f"[0:v]subtitles='{chinese_srt}':force_style='Fontname=PingFang SC,Fontsize=20,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=70'[v1];"
            f"[v1]subtitles='{english_srt}':force_style='Fontname=Arial,Fontsize=18,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=25'[v2];"
            f"[v2]drawtext=text='董卓主演脱口秀':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=24:fontcolor=white:bordercolor=black:borderw=2:x=w-tw-20:y=20[v3]",
            '-map', '[v3]',
            '-map', '0:a',
            '-c:a', 'copy',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            output_video
        ]
        
        try:
            print("🔄 正在渲染双语视频...")
            start_time = time.time()
            
            result = subprocess.run(ffmpeg_cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=1800)  # 30分钟超时
            
            if result.returncode == 0:
                render_time = time.time() - start_time
                file_size = os.path.getsize(output_video) / (1024*1024)
                print(f"✅ 双语视频生成成功!")
                print(f"📁 输出文件: {output_video}")
                print(f"📊 文件大小: {file_size:.1f}MB")
                print(f"⏱️  渲染耗时: {render_time:.1f}秒")
                
                # 也生成纯中文版本
                self.generate_chinese_only_video(project_dir, video_path, chinese_srt)
                
            else:
                print(f"❌ FFmpeg渲染失败:")
                print(f"错误信息: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("❌ 渲染超时（30分钟）")
        except Exception as e:
            print(f"❌ 渲染过程出错: {e}")
    
    def generate_chinese_only_video(self, project_dir, video_path, chinese_srt):
        """生成纯中文字幕视频"""
        print("\n🈳 生成纯中文视频...")
        
        video_name = Path(video_path).stem
        output_video = f"{project_dir}/final/{video_name}_chinese.mp4"
        
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vf', f"subtitles='{chinese_srt}':force_style='Fontname=PingFang SC,Fontsize=22,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=50',drawtext=text='董卓主演脱口秀':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=24:fontcolor=white:bordercolor=black:borderw=2:x=w-tw-20:y=20",
            '-c:a', 'copy',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            output_video
        ]
        
        try:
            result = subprocess.run(ffmpeg_cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=1800)
            
            if result.returncode == 0:
                file_size = os.path.getsize(output_video) / (1024*1024)
                print(f"✅ 中文视频生成成功!")
                print(f"📁 输出文件: {output_video}")
                print(f"📊 文件大小: {file_size:.1f}MB")
            else:
                print(f"⚠️ 中文视频生成失败: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️ 中文视频生成出错: {e}")

def main():
    import sys
    
    automation = OptimizedVideoAutomation()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--finalize":
        automation.finalize_latest_project()
        return
    
    # 交互式开始
    print("🚀 优化版视频处理自动化")
    print("特点: 网络重试、性能优化、错误恢复")
    print("="*50)
    
    url = input("📥 请输入YouTube视频URL: ").strip()
    if not url:
        print("❌ URL不能为空")
        return
    
    use_segment = input("✂️  是否需要切片? (y/N): ").strip().lower()
    
    start_time = None
    end_time = None
    
    if use_segment == 'y':
        start_time = input("⏱️  开始时间 (如: 28:23): ").strip()
        end_time = input("⏱️  结束时间 (如: 36:10): ").strip()
        
        if not start_time or not end_time:
            print("❌ 切片时间不能为空")
            return
    
    automation.process_video_optimized(url, start_time, end_time)

if __name__ == "__main__":
    main() 