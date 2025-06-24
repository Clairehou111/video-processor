#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版视频处理工具：
1. 每个源视频创建独立的输出文件夹
2. 生成视频前先确认双语字幕
"""

import os
import sys
import subprocess
import whisper
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, ImageClip
import yt_dlp
from PIL import Image, ImageDraw, ImageFont
import tempfile
import json
import requests
import time
from pathlib import Path
import re
from urllib.parse import urlparse, parse_qs

class ImprovedVideoProcessor:
    def __init__(self):
        self.whisper_model = None
        self.base_output_dir = "output"
        self.current_video_dir = None
        os.makedirs(self.base_output_dir, exist_ok=True)
    
    def extract_video_id_from_url(self, url):
        """从YouTube URL提取视频ID"""
        if "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        elif "youtube.com/watch" in url:
            parsed_url = urlparse(url)
            return parse_qs(parsed_url.query)['v'][0]
        else:
            # 如果无法提取，使用时间戳
            return f"video_{int(time.time())}"
    
    def create_video_output_dir(self, youtube_url, video_title=None):
        """为每个视频创建独立的输出目录"""
        # 提取视频ID
        video_id = self.extract_video_id_from_url(youtube_url)
        
        # 清理视频标题作为文件夹名
        if video_title:
            # 移除特殊字符，保留中英文、数字、空格、短横线
            clean_title = re.sub(r'[^\w\s\-\u4e00-\u9fff]', '', video_title)
            clean_title = re.sub(r'\s+', '_', clean_title.strip())
            folder_name = f"{video_id}_{clean_title}"
        else:
            folder_name = video_id
        
        # 限制文件夹名长度
        if len(folder_name) > 100:
            folder_name = folder_name[:100]
        
        self.current_video_dir = os.path.join(self.base_output_dir, folder_name)
        os.makedirs(self.current_video_dir, exist_ok=True)
        
        print(f"📁 视频输出目录: {self.current_video_dir}")
        return self.current_video_dir
    
    def load_whisper_model(self, model_size="base"):
        """加载Whisper模型用于语音识别"""
        print(f"正在加载Whisper模型: {model_size}")
        self.whisper_model = whisper.load_model(model_size)
        print("Whisper模型加载完成")
    
    def download_youtube_video(self, url, quality="1080p"):
        """下载YouTube视频到专用文件夹 - 统一使用高质量参数"""
        print(f"正在下载视频: {url} (质量: {quality})")
        
        # 统一使用高质量格式参数
        format_selector = 'bestvideo[height>=1080]+bestaudio/best[height>=1080]'
        print(f"📊 使用高质量参数: {format_selector}")
        
        # 先获取视频信息来创建目录
        ydl_opts_info = {
            'quiet': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info['title']
                
            # 创建视频专用目录
            self.create_video_output_dir(url, video_title)
            
            # 下载视频到专用目录
            ydl_opts = {
                'format': format_selector,
                'outtmpl': os.path.join(self.current_video_dir, '%(title)s.%(ext)s'),
                'writesubtitles': False,
                'writeautomaticsub': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = info['title']
                video_ext = info['ext']
                video_path = os.path.join(self.current_video_dir, f"{video_title}.{video_ext}")
                
                print(f"✅ 视频下载完成: {video_path}")
                print(f"📊 视频信息: {info.get('width', 'N/A')}x{info.get('height', 'N/A')}")
                return video_path, video_title
                
        except Exception as e:
            print(f"❌ 下载视频时出错: {str(e)}")
            return None, None
    
    def extract_audio_and_transcribe(self, video_path):
        """提取音频并进行语音识别"""
        if not self.whisper_model:
            self.load_whisper_model()
        
        print("🔄 正在提取音频并进行语音识别...")
        
        result = self.whisper_model.transcribe(video_path)
        
        segments = []
        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            })
        
        print(f"✅ 语音识别完成，共识别出 {len(segments)} 个片段")
        return segments
    
    def translate_to_chinese_simple(self, text):
        """简单的英文到中文翻译"""
        # 这里使用之前的翻译词典
        common_translations = {
            # 基础词汇
            "hello": "你好", "world": "世界", "video": "视频", "music": "音乐",
            "the": "", "and": "和", "is": "是", "are": "是", "was": "是", "were": "是",
            "this": "这个", "that": "那个", "these": "这些", "those": "那些",
            "with": "与", "for": "为了", "to": "到", "in": "在", "on": "在", "at": "在",
            
            # 常用表达
            "donald": "唐纳德", "trump": "特朗普", "charlie": "查理", "sheen": "辛",
            "watch": "手表", "dinner": "晚餐", "wedding": "婚礼", "wife": "妻子",
            "i have to say": "我必须说", "you know": "你知道",
            "listen i'm sorry": "听着，我很抱歉",
        }
        
        # 转换为小写进行匹配
        text_lower = text.lower().strip()
        
        # 首先检查完整短语
        for eng, chi in common_translations.items():
            if eng in text_lower:
                text_lower = text_lower.replace(eng, chi)
        
        # 如果翻译后主要还是英文，添加标识
        if len([c for c in text_lower if ord(c) > 127]) < len(text_lower) * 0.3:
            return f"[英] {text.strip()}"
        
        return text_lower.strip()
    
    def generate_chinese_subtitles(self, segments):
        """生成中文字幕"""
        print("🔄 正在生成中文字幕...")
        chinese_subtitles = []
        
        for i, segment in enumerate(segments):
            chinese_text = self.translate_to_chinese_simple(segment["text"])
            chinese_subtitles.append({
                "start": segment["start"],
                "end": segment["end"],
                "english": segment["text"],
                "chinese": chinese_text
            })
            
            if (i + 1) % 5 == 0:
                print(f"   已处理 {i + 1}/{len(segments)} 个片段")
        
        print(f"✅ 中文字幕生成完成，共 {len(chinese_subtitles)} 条")
        return chinese_subtitles
    
    def save_dual_subtitles_for_review(self, subtitles, base_filename):
        """保存双语字幕文件供用户审查"""
        english_path = os.path.join(self.current_video_dir, f"{base_filename}_english.srt")
        chinese_path = os.path.join(self.current_video_dir, f"{base_filename}_chinese.srt")
        dual_path = os.path.join(self.current_video_dir, f"{base_filename}_dual_review.txt")
        
        # 保存英文字幕
        with open(english_path, 'w', encoding='utf-8') as f:
            for i, subtitle in enumerate(subtitles, 1):
                start_time = self.seconds_to_srt_time(subtitle["start"])
                end_time = self.seconds_to_srt_time(subtitle["end"])
                f.write(f"{i}\n{start_time} --> {end_time}\n{subtitle['english']}\n\n")
        
        # 保存中文字幕
        with open(chinese_path, 'w', encoding='utf-8') as f:
            for i, subtitle in enumerate(subtitles, 1):
                start_time = self.seconds_to_srt_time(subtitle["start"])
                end_time = self.seconds_to_srt_time(subtitle["end"])
                f.write(f"{i}\n{start_time} --> {end_time}\n{subtitle['chinese']}\n\n")
        
        # 保存双语对照文件供审查
        with open(dual_path, 'w', encoding='utf-8') as f:
            f.write("双语字幕对照 - 请检查翻译质量\n")
            f.write("=" * 50 + "\n\n")
            
            for i, subtitle in enumerate(subtitles, 1):
                start_time = self.seconds_to_srt_time(subtitle["start"])
                end_time = self.seconds_to_srt_time(subtitle["end"])
                f.write(f"片段 {i}: {start_time} --> {end_time}\n")
                f.write(f"英文: {subtitle['english']}\n")
                f.write(f"中文: {subtitle['chinese']}\n")
                f.write("-" * 30 + "\n")
        
        print(f"📝 字幕文件已保存:")
        print(f"   英文: {english_path}")
        print(f"   中文: {chinese_path}")
        print(f"   对照: {dual_path}")
        
        return english_path, chinese_path, dual_path
    
    def display_subtitle_preview(self, subtitles, num_samples=5):
        """显示字幕预览"""
        print("\n📋 双语字幕预览 (前{}条):".format(min(num_samples, len(subtitles))))
        print("=" * 60)
        
        for i, subtitle in enumerate(subtitles[:num_samples]):
            start_time = self.seconds_to_srt_time(subtitle["start"])
            end_time = self.seconds_to_srt_time(subtitle["end"])
            print(f"\n片段 {i+1}: {start_time} --> {end_time}")
            print(f"🇺🇸 英文: {subtitle['english']}")
            print(f"🇨🇳 中文: {subtitle['chinese']}")
            print("-" * 40)
        
        if len(subtitles) > num_samples:
            print(f"\n... 还有 {len(subtitles) - num_samples} 条字幕")
        
        print(f"\n总计: {len(subtitles)} 条双语字幕")
    
    def confirm_subtitles(self, subtitles, base_filename):
        """让用户确认字幕质量"""
        # 保存字幕文件
        english_path, chinese_path, dual_path = self.save_dual_subtitles_for_review(subtitles, base_filename)
        
        # 显示预览
        self.display_subtitle_preview(subtitles)
        
        print(f"\n📁 完整字幕文件已保存到: {self.current_video_dir}")
        print("   可以打开对照文件查看完整翻译: {}".format(os.path.basename(dual_path)))
        
        while True:
            print("\n🤔 请确认字幕质量:")
            print("1. ✅ 字幕质量满意，继续生成视频")
            print("2. ✏️  手动编辑字幕文件后继续")
            print("3. 🔄 重新生成字幕")
            print("4. ❌ 取消处理")
            
            choice = input("请选择 (1-4): ").strip()
            
            if choice == "1":
                print("✅ 继续生成视频...")
                return subtitles, True
            elif choice == "2":
                print(f"📝 请编辑以下文件后按回车继续:")
                print(f"   英文字幕: {english_path}")
                print(f"   中文字幕: {chinese_path}")
                input("编辑完成后按回车继续...")
                
                # 重新读取编辑后的字幕
                try:
                    updated_subtitles = self.load_edited_subtitles(english_path, chinese_path)
                    print("✅ 字幕文件已重新加载")
                    return updated_subtitles, True
                except Exception as e:
                    print(f"❌ 读取编辑后的字幕失败: {e}")
                    continue
            elif choice == "3":
                print("🔄 重新生成字幕...")
                return subtitles, False
            elif choice == "4":
                print("❌ 用户取消处理")
                return None, False
            else:
                print("❌ 无效选择，请重新输入")
    
    def load_edited_subtitles(self, english_path, chinese_path):
        """加载用户编辑后的字幕文件"""
        subtitles = []
        
        # 读取英文字幕
        with open(english_path, 'r', encoding='utf-8') as f:
            english_content = f.read()
        
        # 读取中文字幕
        with open(chinese_path, 'r', encoding='utf-8') as f:
            chinese_content = f.read()
        
        # 解析SRT格式
        english_blocks = [block.strip() for block in english_content.split('\n\n') if block.strip()]
        chinese_blocks = [block.strip() for block in chinese_content.split('\n\n') if block.strip()]
        
        for eng_block, chi_block in zip(english_blocks, chinese_blocks):
            eng_lines = eng_block.split('\n')
            chi_lines = chi_block.split('\n')
            
            if len(eng_lines) >= 3 and len(chi_lines) >= 3:
                # 解析时间
                time_line = eng_lines[1]
                times = time_line.split(' --> ')
                start_time = self.srt_time_to_seconds(times[0])
                end_time = self.srt_time_to_seconds(times[1])
                
                # 获取文本
                english_text = '\n'.join(eng_lines[2:])
                chinese_text = '\n'.join(chi_lines[2:])
                
                subtitles.append({
                    "start": start_time,
                    "end": end_time,
                    "english": english_text,
                    "chinese": chinese_text
                })
        
        return subtitles
    
    def seconds_to_srt_time(self, seconds):
        """将秒数转换为SRT时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
    def srt_time_to_seconds(self, time_str):
        """将SRT时间格式转换为秒数"""
        time_str = time_str.replace(',', '.')
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    
    def create_watermark_image(self, text="水印", size=(200, 50)):
        """创建水印图片"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.rectangle([0, 0, size[0], size[1]], fill=(0, 0, 0, 100))
        draw.text((x, y), text, fill=(255, 255, 255, 200), font=font)
        
        watermark_path = os.path.join(self.current_video_dir, "watermark.png")
        img.save(watermark_path)
        
        return watermark_path
    
    def process_video_with_confirmation(self, youtube_url, watermark_text="我的视频", quality="1080p"):
        """带确认功能的完整视频处理流程"""
        print("🎬 开始改进版视频处理流程...")
        
        # 1. 下载YouTube视频
        video_path, video_title = self.download_youtube_video(youtube_url, quality)
        if not video_path:
            print("❌ 视频下载失败")
            return None
        
        # 2. 语音识别
        segments = self.extract_audio_and_transcribe(video_path)
        
        # 3. 生成双语字幕
        while True:
            chinese_subtitles = self.generate_chinese_subtitles(segments)
            
            # 4. 让用户确认字幕
            confirmed_subtitles, should_continue = self.confirm_subtitles(chinese_subtitles, video_title)
            
            if confirmed_subtitles and should_continue:
                break
            elif not should_continue and confirmed_subtitles is None:
                print("❌ 用户取消处理")
                return None
            # 如果should_continue为False但confirmed_subtitles不为None，则重新生成
        
        print("✅ 字幕确认完成，视频文件已准备好生成B站版本!")
        print(f"📁 所有文件保存在: {self.current_video_dir}")
        
        # 返回处理后的信息
        return {
            "video_path": video_path,
            "video_title": video_title,
            "subtitles": confirmed_subtitles,
            "output_dir": self.current_video_dir,
            "english_srt": os.path.join(self.current_video_dir, f"{video_title}_english.srt"),
            "chinese_srt": os.path.join(self.current_video_dir, f"{video_title}_chinese.srt")
        }

def main():
    """主函数"""
    print("🎬 改进版YouTube视频处理工具")
    print("=" * 40)
    print("新功能:")
    print("✅ 每个视频独立文件夹")
    print("✅ 字幕确认机制")
    print("✅ 支持手动编辑字幕")
    print("=" * 40)
    
    # 获取用户输入
    youtube_url = input("请输入YouTube视频URL: ").strip()
    if not youtube_url:
        print("❌ 请提供有效的YouTube URL")
        return
    
    watermark_text = input("请输入水印文字 (默认: 董卓主演脱口秀): ").strip()
    if not watermark_text:
        watermark_text = "董卓主演脱口秀"
    
    # 创建处理器并执行
    processor = ImprovedVideoProcessor()
    
    try:
        result = processor.process_video_with_confirmation(youtube_url, watermark_text)
        if result:
            print(f"\n🎉 处理成功！")
            print(f"📁 输出目录: {result['output_dir']}")
            print(f"📹 视频文件: {os.path.basename(result['video_path'])}")
            print(f"📝 英文字幕: {os.path.basename(result['english_srt'])}")
            print(f"📝 中文字幕: {os.path.basename(result['chinese_srt'])}")
            print(f"\n💡 接下来可以运行B站版本生成脚本!")
        else:
            print("\n❌ 处理失败或被取消")
    except Exception as e:
        print(f"\n❌ 处理过程中出错: {str(e)}")

if __name__ == "__main__":
    main() 