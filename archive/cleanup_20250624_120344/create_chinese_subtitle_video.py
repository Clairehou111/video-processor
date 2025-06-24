#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文字幕视频生成器
只添加中文字幕，避免双层字幕问题
"""

import os
import re
import subprocess

def parse_english_srt(srt_file):
    """解析英文SRT字幕文件获取时间戳"""
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
            
            segments.append({
                'index': index,
                'timestamp': timestamp
            })
    
    return segments

def parse_chinese_translation(translation_file):
    """解析中文翻译文件"""
    chinese_texts = []
    
    # 检查是否是已有的双语字幕文件
    if translation_file.endswith('_bilingual.srt'):
        print("📖 从双语字幕文件中提取中文翻译...")
        with open(translation_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = content.strip().split('\n\n')
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 4:
                # 第4行是中文翻译
                chinese_text = lines[3]
                chinese_texts.append(chinese_text)
    else:
        # 从普通翻译文件中提取
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

def create_chinese_srt(english_segments, chinese_texts, output_file):
    """创建纯中文SRT字幕文件"""
    min_count = min(len(english_segments), len(chinese_texts))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in range(min_count):
            segment = english_segments[i]
            chinese_text = chinese_texts[i]
            
            f.write(f"{segment['index']}\n")
            f.write(f"{segment['timestamp']}\n")
            f.write(f"{chinese_text}\n\n")
    
    print(f"✅ 中文字幕已生成: {output_file}")
    return True

def create_chinese_subtitle_video(video_file, subtitle_file, output_file):
    """创建带中文字幕的视频"""
    print(f"🎬 正在创建中文字幕视频...")
    
    # 使用ffmpeg添加字幕，设置合适的样式
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', video_file,
        '-vf', f"subtitles={subtitle_file}:force_style='FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=60,Alignment=2'",
        '-c:a', 'copy',
        output_file
    ]
    
    try:
        print("🔄 执行ffmpeg命令...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        print(f"✅ 中文字幕视频创建成功: {output_file}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建视频失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def create_clean_video_with_chinese_subtitles(original_video, chinese_srt, output_file):
    """使用原始视频（无字幕）+ 中文字幕创建视频"""
    print(f"🎬 正在创建纯净的中文字幕视频...")
    
    # 检查是否有原始无字幕视频
    clean_video = original_video.replace('_bilingual.mp4', '.mp4')
    if not os.path.exists(clean_video):
        clean_video = original_video
    
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', clean_video,
        '-vf', f"subtitles={chinese_srt}:force_style='FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=60,Alignment=2'",
        '-c:a', 'copy',
        output_file
    ]
    
    try:
        print("🔄 执行ffmpeg命令...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        print(f"✅ 中文字幕视频创建成功: {output_file}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建视频失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def main():
    """主函数"""
    print("🎯 中文字幕视频生成器")
    print("="*50)
    
    # 文件路径
    original_video = "output/VP9_segment_2m36s-5m59s.mp4"
    english_srt = "output/VP9_segment_2m36s-5m59s_english.srt" 
    bilingual_srt = "output/VP9_segment_2m36s-5m59s_bilingual.srt"
    
    # 输出文件
    chinese_srt = "output/VP9_segment_2m36s-5m59s_chinese.srt"
    chinese_video = "output/VP9_segment_2m36s-5m59s_chinese.mp4"
    
    # 检查输入文件
    if not os.path.exists(original_video):
        print(f"❌ 原始视频文件不存在: {original_video}")
        return
    
    if not os.path.exists(english_srt):
        print(f"❌ 英文字幕文件不存在: {english_srt}")
        return
    
    # 选择翻译来源
    translation_source = None
    if os.path.exists(bilingual_srt):
        print(f"✅ 发现双语字幕文件: {bilingual_srt}")
        translation_source = bilingual_srt
    elif os.path.exists("output/chinese_translation.txt"):
        print(f"✅ 发现中文翻译文件: output/chinese_translation.txt")
        translation_source = "output/chinese_translation.txt"
    else:
        print("❌ 未找到中文翻译文件")
        return
    
    print(f"📁 输入文件:")
    print(f"   🎬 原始视频: {original_video}")
    print(f"   📝 英文字幕: {english_srt}")
    print(f"   📖 翻译来源: {translation_source}")
    print()
    
    # 步骤1: 解析英文字幕时间戳
    print("📝 步骤1: 解析英文字幕时间戳")
    english_segments = parse_english_srt(english_srt)
    print(f"✅ 解析完成，共 {len(english_segments)} 个时间段")
    
    # 步骤2: 解析中文翻译
    print(f"\n📖 步骤2: 解析中文翻译")
    chinese_texts = parse_chinese_translation(translation_source)
    print(f"✅ 解析完成，共 {len(chinese_texts)} 条翻译")
    
    # 步骤3: 创建中文字幕
    print(f"\n🎭 步骤3: 创建中文字幕文件")
    if len(english_segments) != len(chinese_texts):
        print(f"⚠️ 时间段({len(english_segments)})和中文翻译({len(chinese_texts)})数量不匹配")
        print("将使用较小的数量进行匹配")
    
    create_chinese_srt(english_segments, chinese_texts, chinese_srt)
    
    # 步骤4: 创建中文字幕视频
    print(f"\n🎬 步骤4: 创建中文字幕视频")
    success = create_clean_video_with_chinese_subtitles(original_video, chinese_srt, chinese_video)
    
    if success:
        print("\n🎉 中文字幕视频处理完成!")
        print(f"📁 输出文件:")
        print(f"   📝 中文字幕: {chinese_srt}")
        print(f"   🎬 中文视频: {chinese_video}")
        
        # 显示文件大小
        if os.path.exists(chinese_video):
            size_mb = os.path.getsize(chinese_video) / (1024*1024)
            print(f"   📊 视频大小: {size_mb:.1f}MB")
            
        print(f"\n💡 现在您有了3个版本:")
        print(f"   🇺🇸 英文字幕: {original_video.replace('.mp4', '_english.mp4')}")
        print(f"   🇨🇳 中文字幕: {chinese_video}")
        print(f"   🌏 双语字幕: {original_video.replace('.mp4', '_bilingual.mp4')}")
    else:
        print("\n❌ 中文字幕视频处理失败")

if __name__ == "__main__":
    main() 