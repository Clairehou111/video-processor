#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双语视频生成器 - 简化版本
直接使用已有的英文字幕和中文翻译生成双语视频
"""

import os
import re
import subprocess

def parse_english_srt(srt_file):
    """解析英文SRT字幕文件"""
    segments = []
    with open(srt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割字幕块
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            # 序号
            index = lines[0]
            # 时间戳
            timestamp = lines[1]
            # 文本内容
            text = ' '.join(lines[2:])
            
            segments.append({
                'index': index,
                'timestamp': timestamp,
                'text': text
            })
    
    return segments

def parse_chinese_translation(translation_file):
    """解析中文翻译文件"""
    chinese_texts = []
    with open(translation_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and re.match(r'^\d+\.', line):
            # 提取编号后的文本
            text = re.sub(r'^\d+\.\s*', '', line)
            chinese_texts.append(text)
    
    return chinese_texts

def create_bilingual_srt(english_segments, chinese_texts, output_file):
    """创建双语SRT字幕文件"""
    min_count = min(len(english_segments), len(chinese_texts))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in range(min_count):
            segment = english_segments[i]
            chinese_text = chinese_texts[i]
            
            f.write(f"{segment['index']}\n")
            f.write(f"{segment['timestamp']}\n")
            f.write(f"{segment['text']}\n")
            f.write(f"{chinese_text}\n\n")
    
    print(f"✅ 双语字幕已生成: {output_file}")
    return True

def create_bilingual_video(video_file, subtitle_file, output_file):
    """创建带双语字幕的视频"""
    print(f"🎬 正在创建双语视频...")
    
    # 使用ffmpeg添加字幕
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', video_file,
        '-vf', f"subtitles={subtitle_file}:force_style='FontSize=20,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=50'",
        '-c:a', 'copy',
        output_file
    ]
    
    try:
        print("🔄 执行ffmpeg命令...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        print(f"✅ 双语视频创建成功: {output_file}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建双语视频失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def main():
    """主函数"""
    print("🎯 双语视频生成器")
    print("="*50)
    
    # 文件路径
    video_file = "output/VP9_segment_2m36s-5m59s.mp4"
    english_srt = "output/VP9_segment_2m36s-5m59s_english.srt"
    chinese_translation = "output/chinese_translation.txt"
    bilingual_srt = "output/VP9_segment_2m36s-5m59s_bilingual.srt"
    bilingual_video = "output/VP9_segment_2m36s-5m59s_bilingual.mp4"
    
    # 检查文件是否存在
    files_to_check = [video_file, english_srt, chinese_translation]
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return
    
    print("📁 输入文件检查:")
    print(f"✅ 视频文件: {video_file}")
    print(f"✅ 英文字幕: {english_srt}")
    print(f"✅ 中文翻译: {chinese_translation}")
    print()
    
    # 步骤1: 解析英文字幕
    print("📝 步骤1: 解析英文字幕")
    english_segments = parse_english_srt(english_srt)
    print(f"✅ 解析完成，共 {len(english_segments)} 个片段")
    
    # 步骤2: 解析中文翻译
    print("\n📖 步骤2: 解析中文翻译")
    chinese_texts = parse_chinese_translation(chinese_translation)
    print(f"✅ 解析完成，共 {len(chinese_texts)} 条翻译")
    
    # 步骤3: 创建双语字幕
    print(f"\n🎭 步骤3: 创建双语字幕")
    if len(english_segments) != len(chinese_texts):
        print(f"⚠️ 英文字幕({len(english_segments)})和中文翻译({len(chinese_texts)})数量不匹配")
        print("将使用较小的数量进行匹配")
    
    create_bilingual_srt(english_segments, chinese_texts, bilingual_srt)
    
    # 步骤4: 创建双语视频
    print(f"\n🎬 步骤4: 创建双语视频")
    success = create_bilingual_video(video_file, bilingual_srt, bilingual_video)
    
    if success:
        print("\n🎉 双语视频处理完成!")
        print(f"📁 输出文件:")
        print(f"   • 双语字幕: {bilingual_srt}")
        print(f"   • 双语视频: {bilingual_video}")
        
        # 显示文件大小
        if os.path.exists(bilingual_video):
            size_mb = os.path.getsize(bilingual_video) / (1024*1024)
            print(f"   • 视频大小: {size_mb:.1f}MB")
    else:
        print("\n❌ 双语视频处理失败")

if __name__ == "__main__":
    main() 