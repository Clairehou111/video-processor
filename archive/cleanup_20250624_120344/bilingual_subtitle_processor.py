#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双语字幕处理器
1. 使用Whisper提取英文字幕
2. 使用Sider.AI翻译为中文
3. 生成双语视频
"""

import os
import sys
import json
import time
import whisper
import subprocess
from pathlib import Path
import re

class BilingualSubtitleProcessor:
    """双语字幕处理器"""
    
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.whisper_model = None
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_whisper_model(self, model_size="base"):
        """加载Whisper模型"""
        print(f"🔄 加载Whisper {model_size} 模型...")
        try:
            self.whisper_model = whisper.load_model(model_size)
            print(f"✅ Whisper模型加载成功")
            return True
        except Exception as e:
            print(f"❌ Whisper模型加载失败: {e}")
            return False
    
    def extract_english_subtitles(self, video_path):
        """提取英文字幕"""
        if not self.whisper_model:
            if not self.load_whisper_model():
                return None
        
        print(f"🎧 正在提取英文字幕: {os.path.basename(video_path)}")
        
        try:
            # 使用Whisper转录
            result = self.whisper_model.transcribe(video_path)
            
            # 提取段落信息
            segments = []
            for segment in result["segments"]:
                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                })
            
            print(f"✅ 英文字幕提取完成，共 {len(segments)} 个片段")
            return segments
            
        except Exception as e:
            print(f"❌ 英文字幕提取失败: {e}")
            return None
    
    def save_english_srt(self, segments, output_path):
        """保存英文SRT字幕文件"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments, 1):
                    start_time = self.seconds_to_srt_time(segment['start'])
                    end_time = self.seconds_to_srt_time(segment['end'])
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{segment['text']}\n\n")
            
            print(f"✅ 英文字幕已保存: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 保存英文字幕失败: {e}")
            return False
    
    def seconds_to_srt_time(self, seconds):
        """将秒数转换为SRT时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def prepare_text_for_sider(self, segments):
        """准备文本供Sider.AI翻译"""
        print("📝 准备文本供Sider.AI翻译...")
        
        # 创建翻译文本文件
        text_lines = []
        for i, segment in enumerate(segments, 1):
            text_lines.append(f"{i}. {segment['text']}")
        
        translation_text = "\n".join(text_lines)
        
        # 保存到文件
        sider_input_path = os.path.join(self.output_dir, "sider_translation_input.txt")
        with open(sider_input_path, 'w', encoding='utf-8') as f:
            f.write("请将以下英文文本翻译为中文，保持原有的编号格式：\n\n")
            f.write(translation_text)
        
        print(f"✅ 翻译输入文件已准备: {sider_input_path}")
        return sider_input_path
    
    def create_sider_prompt(self, segments):
        """创建Sider.AI翻译提示"""
        prompt = """请将以下英文字幕翻译为中文，要求：
1. 保持原有的编号格式
2. 翻译要自然流畅，符合中文表达习惯
3. 保持政治脱口秀的幽默感和讽刺语调
4. 专有名词（人名、地名）保持英文或使用通用中文译名
5. 每行翻译后请换行

英文字幕内容：

"""
        
        for i, segment in enumerate(segments, 1):
            prompt += f"{i}. {segment['text']}\n"
        
        return prompt
    
    def show_sider_instructions(self, segments):
        """显示Sider.AI使用说明"""
        print("\n" + "="*60)
        print("🤖 Sider.AI 翻译指南")
        print("="*60)
        
        # 创建提示词
        prompt = self.create_sider_prompt(segments)
        
        # 保存提示词到文件
        prompt_file = os.path.join(self.output_dir, "sider_translation_prompt.txt")
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"📝 翻译提示词已保存到: {prompt_file}")
        print()
        print("🔧 使用步骤:")
        print("1. 打开 https://sider.ai")
        print("2. 选择 ChatGPT 或 Claude 模型")
        print("3. 复制以下提示词:")
        print()
        print("─" * 40)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        print("─" * 40)
        print()
        print("4. 等待翻译完成")
        print("5. 将翻译结果保存到文件")
        print(f"6. 将结果保存为: {os.path.join(self.output_dir, 'chinese_translation.txt')}")
        print()
        print("⏳ 完成翻译后，按回车继续...")
        input()
    
    def parse_chinese_translation(self, translation_file):
        """解析中文翻译结果"""
        try:
            with open(translation_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析翻译结果
            chinese_texts = []
            lines = content.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if line and re.match(r'^\d+\.', line):
                    # 提取编号后的文本
                    text = re.sub(r'^\d+\.\s*', '', line)
                    chinese_texts.append(text)
            
            print(f"✅ 解析中文翻译完成，共 {len(chinese_texts)} 条")
            return chinese_texts
            
        except Exception as e:
            print(f"❌ 解析中文翻译失败: {e}")
            return None
    
    def create_bilingual_subtitles(self, segments, chinese_texts):
        """创建双语字幕"""
        if len(segments) != len(chinese_texts):
            print(f"⚠️ 英文字幕({len(segments)})和中文翻译({len(chinese_texts)})数量不匹配")
            # 取较小的数量
            min_count = min(len(segments), len(chinese_texts))
            segments = segments[:min_count]
            chinese_texts = chinese_texts[:min_count]
        
        # 创建双语字幕
        bilingual_segments = []
        for i, (segment, chinese_text) in enumerate(zip(segments, chinese_texts)):
            bilingual_segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "english": segment["text"],
                "chinese": chinese_text
            })
        
        return bilingual_segments
    
    def save_bilingual_srt(self, bilingual_segments, output_path):
        """保存双语SRT字幕文件"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(bilingual_segments, 1):
                    start_time = self.seconds_to_srt_time(segment['start'])
                    end_time = self.seconds_to_srt_time(segment['end'])
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{segment['english']}\n")
                    f.write(f"{segment['chinese']}\n\n")
            
            print(f"✅ 双语字幕已保存: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 保存双语字幕失败: {e}")
            return False
    
    def create_bilingual_video(self, video_path, subtitle_path, output_path):
        """创建带双语字幕的视频"""
        print(f"🎬 正在创建双语视频...")
        
        # 使用ffmpeg添加字幕
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vf', f"subtitles={subtitle_path}:force_style='FontSize=16,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=1'",
            '-c:a', 'copy',
            output_path
        ]
        
        try:
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print(f"✅ 双语视频创建成功: {output_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 创建双语视频失败: {e}")
            print(f"错误输出: {e.stderr}")
            return False
    
    def process_video(self, video_path):
        """处理视频的完整流程"""
        print("🎯 双语字幕处理开始")
        print("="*50)
        
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # 步骤1: 提取英文字幕
        print("\n📝 步骤1: 提取英文字幕")
        segments = self.extract_english_subtitles(video_path)
        if not segments:
            return False
        
        # 保存英文字幕
        english_srt_path = os.path.join(self.output_dir, f"{video_name}_english.srt")
        self.save_english_srt(segments, english_srt_path)
        
        # 步骤2: 准备Sider.AI翻译
        print("\n🤖 步骤2: 准备Sider.AI翻译")
        self.show_sider_instructions(segments)
        
        # 步骤3: 解析中文翻译
        print("\n📖 步骤3: 解析中文翻译")
        translation_file = os.path.join(self.output_dir, "chinese_translation.txt")
        
        if not os.path.exists(translation_file):
            print(f"❌ 未找到翻译文件: {translation_file}")
            print("请确保已将Sider.AI的翻译结果保存到该文件")
            return False
        
        chinese_texts = self.parse_chinese_translation(translation_file)
        if not chinese_texts:
            return False
        
        # 步骤4: 创建双语字幕
        print("\n🎭 步骤4: 创建双语字幕")
        bilingual_segments = self.create_bilingual_subtitles(segments, chinese_texts)
        
        # 保存双语字幕
        bilingual_srt_path = os.path.join(self.output_dir, f"{video_name}_bilingual.srt")
        self.save_bilingual_srt(bilingual_segments, bilingual_srt_path)
        
        # 步骤5: 创建双语视频
        print("\n🎬 步骤5: 创建双语视频")
        bilingual_video_path = os.path.join(self.output_dir, f"{video_name}_bilingual.mp4")
        success = self.create_bilingual_video(video_path, bilingual_srt_path, bilingual_video_path)
        
        if success:
            print("\n🎉 双语字幕处理完成!")
            print(f"📁 输出文件:")
            print(f"   • 英文字幕: {english_srt_path}")
            print(f"   • 双语字幕: {bilingual_srt_path}")
            print(f"   • 双语视频: {bilingual_video_path}")
            return True
        else:
            return False

def main():
    """主函数"""
    print("🎯 双语字幕处理器")
    print("="*50)
    
    # 检查可用视频
    output_dir = "output"
    video_files = []
    
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            if file.endswith(('.mp4', '.webm', '.mkv')):
                video_files.append(os.path.join(output_dir, file))
    
    if not video_files:
        print("❌ 未找到视频文件")
        return
    
    print("📺 可用视频文件:")
    for i, video_file in enumerate(video_files, 1):
        size_mb = os.path.getsize(video_file) / (1024*1024)
        print(f"   {i}. {os.path.basename(video_file)} ({size_mb:.1f}MB)")
    
    # 选择视频
    try:
        choice = int(input(f"\n请选择视频 (1-{len(video_files)}): ")) - 1
        if 0 <= choice < len(video_files):
            selected_video = video_files[choice]
        else:
            print("❌ 无效选择")
            return
    except ValueError:
        print("❌ 无效输入")
        return
    
    # 处理视频
    processor = BilingualSubtitleProcessor()
    processor.process_video(selected_video)

if __name__ == "__main__":
    main() 