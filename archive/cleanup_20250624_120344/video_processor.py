#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频处理工具：下载YouTube视频，生成中文字幕，添加水印
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

class VideoProcessor:
    def __init__(self):
        self.whisper_model = None
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_whisper_model(self, model_size="base"):
        """加载Whisper模型用于语音识别"""
        print(f"正在加载Whisper模型: {model_size}")
        self.whisper_model = whisper.load_model(model_size)
        print("Whisper模型加载完成")
    
    def download_youtube_video(self, url, quality="1080p"):
        """下载YouTube视频 - 统一使用高质量参数"""
        print(f"正在下载视频: {url} (质量: {quality})")
        
        # 统一使用高质量格式参数
        format_selector = 'bestvideo[height>=1080]+bestaudio/best[height>=1080]'
        print(f"📊 使用高质量参数: {format_selector}")
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'writesubtitles': False,
            'writeautomaticsub': False,
            # 添加质量优化选项
            'prefer_ffmpeg': True,  # 优先使用ffmpeg进行格式合并
            'merge_output_format': 'mp4',  # 确保输出为mp4格式
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = info['title']
                video_ext = info['ext']
                video_path = os.path.join(self.output_dir, f"{video_title}.{video_ext}")
                
                print(f"视频下载完成: {video_path}")
                print(f"视频信息: {info.get('width', 'N/A')}x{info.get('height', 'N/A')}")
                print(f"视频格式: {info.get('format_id', 'N/A')}")
                print(f"视频码率: {info.get('vbr', 'N/A')} kbps")
                print(f"音频码率: {info.get('abr', 'N/A')} kbps")
                return video_path, video_title
                
        except Exception as e:
            print(f"下载视频时出错: {str(e)}")
            return None, None
    
    def download_youtube_video_segment(self, url, start_time=None, end_time=None, quality="1080p"):
        """下载YouTube视频的指定时间段 - 统一使用高质量参数"""
        print(f"正在下载视频片段: {url}")
        if start_time and end_time:
            print(f"时间窗口: {start_time} - {end_time}")
        elif start_time:
            print(f"从 {start_time} 开始下载")
        
        # 统一使用高质量格式参数
        format_selector = 'bestvideo[height>=1080]+bestaudio/best[height>=1080]'
        print(f"📊 使用高质量参数: {format_selector}")
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': os.path.join(self.output_dir, '%(title)s_segment.%(ext)s'),
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
        
        # 如果指定了时间参数，使用external_downloader
        if start_time or end_time:
            # 使用ffmpeg作为外部下载器来处理时间切片
            ydl_opts['external_downloader'] = 'ffmpeg'
            external_downloader_args = []
            
            if start_time:
                external_downloader_args.extend(['-ss', start_time])
            if end_time:
                # 计算持续时间
                if start_time:
                    start_seconds = self.time_to_seconds(start_time)
                    end_seconds = self.time_to_seconds(end_time)
                    duration = end_seconds - start_seconds
                    external_downloader_args.extend(['-t', str(duration)])
                else:
                    external_downloader_args.extend(['-to', end_time])
            
            ydl_opts['external_downloader_args'] = external_downloader_args
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = info['title']
                video_ext = info['ext']
                video_path = os.path.join(self.output_dir, f"{video_title}_segment.{video_ext}")
                
                print(f"视频片段下载完成: {video_path}")
                print(f"视频信息: {info.get('width', 'N/A')}x{info.get('height', 'N/A')}")
                return video_path, video_title
                
        except Exception as e:
            print(f"下载视频片段时出错: {str(e)}")
            return None, None
    
    def extract_audio_and_transcribe(self, video_path):
        """提取音频并进行语音识别"""
        if not self.whisper_model:
            self.load_whisper_model()
        
        print("正在提取音频并进行语音识别...")
        
        # 使用Whisper直接处理视频文件
        result = self.whisper_model.transcribe(video_path)
        
        # 提取文本段落和时间戳
        segments = []
        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            })
        
        print(f"语音识别完成，共识别出 {len(segments)} 个片段")
        return segments
    
    def translate_to_chinese_simple(self, text):
        """简单的英文到中文翻译（使用预定义词典或占位符）"""
        # 扩展的中英文词典
        common_translations = {
            # 基础词汇
            "hello": "你好", "world": "世界", "video": "视频", "music": "音乐",
            "the": "", "and": "和", "is": "是", "are": "是", "was": "是", "were": "是",
            "this": "这个", "that": "那个", "these": "这些", "those": "那些",
            "with": "与", "for": "为了", "to": "到", "in": "在", "on": "在", "at": "在",
            "by": "由", "from": "来自", "up": "上", "about": "关于", "into": "进入",
            "through": "通过", "during": "期间", "before": "之前", "after": "之后",
            "above": "上面", "below": "下面", "between": "之间", "under": "下面",
            
            # 人称代词
            "i": "我", "me": "我", "my": "我的", "mine": "我的",
            "you": "你", "your": "你的", "yours": "你的", 
            "he": "他", "him": "他", "his": "他的",
            "she": "她", "her": "她的", "hers": "她的",
            "we": "我们", "us": "我们", "our": "我们的", "ours": "我们的",
            "they": "他们", "them": "他们", "their": "他们的", "theirs": "他们的",
            
            # 常用动词
            "have": "有", "has": "有", "had": "有过",
            "do": "做", "does": "做", "did": "做了", "done": "完成",
            "go": "去", "goes": "去", "went": "去了", "gone": "去过",
            "come": "来", "comes": "来", "came": "来了",
            "see": "看", "saw": "看见", "seen": "看过",
            "know": "知道", "knew": "知道", "known": "知道",
            "get": "得到", "got": "得到", "gotten": "得到",
            "make": "制作", "made": "制作", "take": "拿", "took": "拿了",
            "give": "给", "gave": "给了", "given": "给过",
            "think": "想", "thought": "想过", "say": "说", "said": "说过",
            "tell": "告诉", "told": "告诉过", "ask": "问", "asked": "问过",
            "work": "工作", "worked": "工作过", "play": "玩", "played": "玩过",
            "look": "看", "looked": "看过", "seem": "似乎", "seemed": "似乎",
            "feel": "感觉", "felt": "感觉", "try": "尝试", "tried": "尝试过",
            "leave": "离开", "left": "离开", "find": "找到", "found": "找到",
            "become": "成为", "became": "成为", "let": "让", "put": "放",
            "mean": "意思", "meant": "意思", "keep": "保持", "kept": "保持",
            "begin": "开始", "began": "开始", "begun": "开始",
            "help": "帮助", "helped": "帮助", "show": "显示", "showed": "显示",
            "hear": "听", "heard": "听到", "bring": "带来", "brought": "带来",
            "turn": "转", "turned": "转", "start": "开始", "started": "开始",
            "might": "可能", "could": "可以", "should": "应该", "would": "会",
            "can": "可以", "will": "将", "shall": "应该", "may": "可能",
            
            # 常用名词
            "time": "时间", "year": "年", "day": "天", "week": "周", "month": "月",
            "man": "男人", "woman": "女人", "person": "人", "people": "人们",
            "child": "孩子", "children": "孩子们", "family": "家庭",
            "friend": "朋友", "friends": "朋友们", "house": "房子", "home": "家",
            "school": "学校", "work": "工作", "money": "钱", "book": "书",
            "car": "汽车", "food": "食物", "water": "水", "hand": "手",
            "eye": "眼睛", "head": "头", "face": "脸", "place": "地方",
            "country": "国家", "city": "城市", "state": "州", "world": "世界",
            "life": "生活", "death": "死亡", "love": "爱", "war": "战争",
            "peace": "和平", "business": "生意", "company": "公司",
            "government": "政府", "law": "法律", "court": "法院",
            "president": "总统", "minister": "部长", "party": "政党",
            
            # 常用形容词
            "good": "好", "bad": "坏", "great": "伟大", "small": "小", "big": "大",
            "new": "新", "old": "老", "young": "年轻", "high": "高", "low": "低",
            "long": "长", "short": "短", "right": "对", "wrong": "错", "true": "真",
            "false": "假", "real": "真实", "important": "重要", "possible": "可能",
            "different": "不同", "same": "相同", "next": "下一个", "last": "最后",
            "first": "第一", "second": "第二", "early": "早", "late": "晚",
            "black": "黑", "white": "白", "red": "红", "blue": "蓝", "green": "绿",
            
            # 数字
            "one": "一", "two": "二", "three": "三", "four": "四", "five": "五",
            "six": "六", "seven": "七", "eight": "八", "nine": "九", "ten": "十",
            "hundred": "百", "thousand": "千", "million": "百万",
            
            # 时间词汇
            "now": "现在", "today": "今天", "tomorrow": "明天", "yesterday": "昨天",
            "morning": "早上", "afternoon": "下午", "evening": "晚上", "night": "夜晚",
            "here": "这里", "there": "那里", "where": "哪里", "when": "什么时候",
            "how": "怎么", "what": "什么", "why": "为什么", "who": "谁",
            
            # 礼貌用语
            "please": "请", "thank": "谢谢", "thanks": "谢谢", "sorry": "对不起",
            "welcome": "欢迎", "hello": "你好", "goodbye": "再见", "yes": "是",
            "no": "不", "ok": "好的", "okay": "好的",
            
            # 特定内容相关
            "donald": "唐纳德", "trump": "特朗普", "charlie": "查理", "sheen": "辛",
            "watch": "手表", "dinner": "晚餐", "wedding": "婚礼", "wife": "妻子",
            "family": "家庭", "surprised": "惊讶", "supporter": "支持者",
            "fan": "粉丝", "invited": "邀请", "staring": "盯着", "noticed": "注意到",
            "listen": "听", "sorry": "对不起", "wasn't": "不是", "really": "真的",
            "halfway": "中途", "saying": "说", "started": "开始",
        }
        
        # 首先处理整句的常见表达
        full_sentence_translations = {
            "now i have to say": "现在我必须说",
            "i have to say": "我必须说",
            "i don't know": "我不知道",
            "you know": "你知道",
            "i'm really not": "我真的不是",
            "i am reminded of": "我想起了",
            "about five years ago": "大约五年前",
            "listen i'm sorry": "听着，我很抱歉",
            "i wasn't invited": "我没有被邀请",
        }
        
        # 先检查整句翻译
        text_lower = text.lower().strip()
        for eng_phrase, chi_phrase in full_sentence_translations.items():
            if eng_phrase in text_lower:
                return chi_phrase
        
        # 分词翻译
        import re
        # 去除标点符号，但保留中文字符
        words = re.findall(r'\b\w+\b', text.lower())
        translated_words = []
        
        for word in words:
            if word in common_translations:
                translation = common_translations[word]
                if translation:  # 不为空才添加
                    translated_words.append(translation)
            else:
                # 对于未翻译的词，保留原文
                translated_words.append(word)
        
        result = " ".join(translated_words)
        
        # 如果翻译效果不好（中文字符太少），添加原文备注
        chinese_chars = len([c for c in result if '\u4e00' <= c <= '\u9fff'])
        total_chars = len([c for c in result if c.isalpha() or '\u4e00' <= c <= '\u9fff'])
        
        if total_chars > 0 and chinese_chars / total_chars < 0.4:
            # 如果中文字符比例小于40%，添加原文
            result = f"{result} [{text}]"
        
        return result if result.strip() else f"[原文] {text}"
    
    def generate_chinese_subtitles(self, segments):
        """生成中文字幕"""
        print("正在翻译字幕为中文...")
        
        chinese_segments = []
        for i, segment in enumerate(segments):
            print(f"正在翻译第 {i+1}/{len(segments)} 个片段...")
            chinese_text = self.translate_to_chinese_simple(segment["text"])
            chinese_segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": chinese_text
            })
        
        print("字幕翻译完成")
        return chinese_segments
    
    def create_watermark_image(self, text="水印", size=(200, 50)):
        """创建水印图片"""
        img = Image.new('RGBA', size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        except:
            # 使用默认字体
            font = ImageFont.load_default()
        
        # 计算文本位置
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # 绘制半透明背景
        draw.rectangle([0, 0, size[0], size[1]], fill=(0, 0, 0, 100))
        
        # 绘制文本
        draw.text((x, y), text, fill=(255, 255, 255, 200), font=font)
        
        watermark_path = os.path.join(self.output_dir, "watermark.png")
        img.save(watermark_path)
        
        return watermark_path
    
    def add_subtitles_and_watermark(self, video_path, subtitles, watermark_text="我的视频", embed_subtitles=True):
        """添加字幕和水印到视频"""
        if embed_subtitles:
            print("正在添加字幕和水印到视频...")
        else:
            print("正在添加水印到视频...")
        
        # 加载视频
        video = VideoFileClip(video_path)
        
        # 创建水印
        watermark_path = self.create_watermark_image(watermark_text)
        watermark = (ImageClip(watermark_path)
                    .set_duration(video.duration)
                    .resize(height=50)
                    .set_position(('right', 'top'))
                    .set_opacity(0.7))
        
        # 创建字幕片段（如果选择嵌入）
        subtitle_clips = []
        if embed_subtitles and subtitles:
            print("正在创建字幕片段...")
            
            for i, subtitle in enumerate(subtitles):
                try:
                    # 创建字幕文本片段
                    txt_clip = (TextClip(subtitle["text"], 
                                       fontsize=40,  # 进一步增大字体
                                       color='yellow',  # 改为黄色更明显
                                       stroke_color='black',
                                       stroke_width=4,  # 增加描边宽度
                                       method='caption',  # 使用caption方法
                                       size=(video.w-80, None),  # 减少边距，增加显示区域
                                       align='center')
                               .set_position(('center', video.h - 120))  # 调整位置更靠上一些
                               .set_start(subtitle["start"])
                               .set_duration(subtitle["end"] - subtitle["start"]))
                    subtitle_clips.append(txt_clip)
                    
                    if (i + 1) % 10 == 0:  # 每10个片段显示进度
                        print(f"已创建 {i + 1}/{len(subtitles)} 个字幕片段")
                        
                except Exception as e:
                    print(f"创建字幕片段 {i+1} 时出错: {str(e)}")
                    # 继续处理其他字幕片段
                    continue
            
            print(f"成功创建 {len(subtitle_clips)} 个字幕片段")
        
        # 合成最终视频
        video_clips = [video, watermark]
        if subtitle_clips:
            video_clips.extend(subtitle_clips)
        
        final_video = CompositeVideoClip(video_clips)
        
        # 生成输出文件名
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        if embed_subtitles:
            output_path = os.path.join(self.output_dir, f"{base_name}_with_subtitles_and_watermark.mp4")
        else:
            output_path = os.path.join(self.output_dir, f"{base_name}_with_watermark.mp4")
        
        # 导出视频
        if embed_subtitles:
            print("正在导出带字幕和水印的视频...")
        else:
            print("正在导出带水印的视频...")
            
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # 清理资源
        video.close()
        final_video.close()
        for clip in subtitle_clips:
            clip.close()
        watermark.close()
        
        print(f"视频处理完成: {output_path}")
        if not embed_subtitles:
            print(f"字幕文件: {os.path.join(self.output_dir, os.path.splitext(os.path.basename(video_path))[0] + '_chinese.srt')}")
        return output_path
    
    def save_subtitles_to_srt(self, subtitles, filename):
        """保存字幕为SRT格式"""
        srt_path = os.path.join(self.output_dir, filename)
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, subtitle in enumerate(subtitles, 1):
                start_time = self.seconds_to_srt_time(subtitle["start"])
                end_time = self.seconds_to_srt_time(subtitle["end"])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{subtitle['text']}\n\n")
        
        print(f"字幕文件已保存: {srt_path}")
        return srt_path
    
    def seconds_to_srt_time(self, seconds):
        """将秒数转换为SRT时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
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
    
    def download_youtube_video_high_quality(self, url, show_formats=False):
        """下载YouTube视频的最高质量版本，并显示可用格式信息"""
        print(f"🎬 高质量下载模式: {url}")
        
        # 如果需要，先显示所有可用格式
        if show_formats:
            print("\n📋 查看可用格式...")
            list_opts = {'listformats': True}
            try:
                with yt_dlp.YoutubeDL(list_opts) as ydl:
                    ydl.extract_info(url, download=False)
            except:
                pass
            print("\n" + "="*50)
        
        # 尝试多种高质量格式选择策略
        format_strategies = [
            'bestvideo[ext=mp4][height>=1080]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'bestvideo[height>=1080]+bestaudio/best[height>=1080]',
            'bestvideo+bestaudio/best',
            'best'
        ]
        
        for i, format_selector in enumerate(format_strategies, 1):
            print(f"\n🔄 尝试策略 {i}: {format_selector}")
            
            ydl_opts = {
                'format': format_selector,
                'outtmpl': os.path.join(self.output_dir, '%(title)s_HQ.%(ext)s'),
                'writesubtitles': False,
                'writeautomaticsub': False,
                'prefer_ffmpeg': True,
                'merge_output_format': 'mp4',
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info['title']
                    video_ext = info['ext']
                    video_path = os.path.join(self.output_dir, f"{video_title}_HQ.{video_ext}")
                    
                    print(f"✅ 高质量视频下载成功!")
                    print(f"📁 文件路径: {video_path}")
                    print(f"📺 分辨率: {info.get('width', 'N/A')}x{info.get('height', 'N/A')}")
                    print(f"🎯 格式ID: {info.get('format_id', 'N/A')}")
                    print(f"📈 视频码率: {info.get('vbr', 'N/A')} kbps")
                    print(f"🔊 音频码率: {info.get('abr', 'N/A')} kbps")
                    print(f"⚙️ 编码器: {info.get('vcodec', 'N/A')} / {info.get('acodec', 'N/A')}")
                    
                    # 计算文件大小
                    if os.path.exists(video_path):
                        file_size = os.path.getsize(video_path) / (1024*1024)
                        print(f"📦 文件大小: {file_size:.2f} MB")
                    
                    return video_path, video_title
                    
            except Exception as e:
                print(f"❌ 策略 {i} 失败: {str(e)}")
                continue
        
        print("❌ 所有下载策略都失败了")
        return None, None
    
    def process_video(self, youtube_url, watermark_text="我的视频", quality="1080p", embed_subtitles=True):
        """完整的视频处理流程"""
        print("开始视频处理流程...")
        
        # 1. 下载YouTube视频
        video_path, video_title = self.download_youtube_video(youtube_url, quality)
        if not video_path:
            print("视频下载失败")
            return None
        
        # 2. 语音识别
        segments = self.extract_audio_and_transcribe(video_path)
        
        # 3. 翻译为中文
        chinese_subtitles = self.generate_chinese_subtitles(segments)
        
        # 4. 保存字幕文件
        self.save_subtitles_to_srt(chinese_subtitles, f"{video_title}_chinese.srt")
        
        # 5. 添加字幕和水印
        processed_video = self.add_subtitles_and_watermark(
            video_path, chinese_subtitles, watermark_text, embed_subtitles
        )
        
        print("视频处理完成！")
        return processed_video

def main():
    """主函数"""
    print("=== YouTube视频处理工具 ===")
    print("功能：下载YouTube视频 -> 生成中文字幕 -> 添加水印")
    print()
    
    # 示例YouTube视频URL（英文内容）
    example_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # 示例
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # 示例
    ]
    
    # 获取用户输入
    youtube_url = input("请输入YouTube视频URL: ").strip()
    if not youtube_url:
        print("使用示例URL进行演示...")
        youtube_url = example_urls[0]
    
    watermark_text = input("请输入水印文字 (默认: 我的视频): ").strip()
    if not watermark_text:
        watermark_text = "我的视频"
    
    # 创建处理器并执行
    processor = VideoProcessor()
    
    try:
        result = processor.process_video(youtube_url, watermark_text)
        if result:
            print(f"\n✅ 处理成功！输出文件: {result}")
        else:
            print("\n❌ 处理失败")
    except Exception as e:
        print(f"\n❌ 处理过程中出错: {str(e)}")

if __name__ == "__main__":
    main() 