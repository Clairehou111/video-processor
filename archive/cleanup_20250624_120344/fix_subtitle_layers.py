#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复双层字幕问题
检测视频是否已有烧录字幕，并提供解决方案
"""

import os
import subprocess
import shutil
import time
from pathlib import Path

def check_video_has_burned_subtitles(video_path):
    """检测视频是否已有烧录字幕（通过文件大小和时长比较）"""
    try:
        # 获取视频信息
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-print_format', 'json', 
            '-show_format', '-show_streams', video_path
        ], capture_output=True, text=True, check=True)
        
        import json
        info = json.loads(result.stdout)
        
        duration = float(info['format']['duration'])
        size_mb = int(info['format']['size']) / (1024*1024)
        bitrate = int(info['format']['bit_rate']) / 1000  # kbps
        
        print(f"📊 视频信息:")
        print(f"   时长: {duration:.1f}秒")
        print(f"   大小: {size_mb:.1f}MB")
        print(f"   码率: {bitrate:.0f}kbps")
        
        # 根据经验判断是否有烧录字幕
        # 通常有字幕的视频码率会更高
        has_subtitles = bitrate > 1500 or size_mb > 50
        
        return has_subtitles, size_mb, duration, bitrate
        
    except Exception as e:
        print(f"❌ 检测视频信息失败: {e}")
        return False, 0, 0, 0

def find_clean_video_source():
    """寻找无字幕的原始视频源"""
    possible_sources = [
        "output/DailyShow_HQ_segment_Ted Cruz & Tucker Carlson Battle Over Iran While Trump Enters His Decorating Era ｜ The Daily Show.webm",
        # 可能的其他源文件
    ]
    
    for source in possible_sources:
        if os.path.exists(source):
            print(f"✅ 找到可能的原始视频源: {source}")
            return source
    
    print("❌ 未找到原始视频源")
    return None

def create_clean_video_from_source(source_video, target_video, start_time="2m36s", duration="3m23s"):
    """从原始源创建干净的视频片段"""
    print(f"🎬 从原始源创建干净视频片段...")
    
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', source_video,
        '-ss', start_time,
        '-t', duration,
        '-c', 'copy',  # 直接复制，不重新编码
        target_video
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        print(f"✅ 干净视频片段创建成功: {target_video}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建视频片段失败: {e}")
        return False

def create_subtitle_only_video(clean_video, subtitle_file, output_video, subtitle_type="chinese"):
    """在干净视频上添加单层字幕"""
    print(f"🎬 在干净视频上添加{subtitle_type}字幕...")
    
    # 字幕样式设置
    if subtitle_type == "chinese":
        style = "FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=60,Alignment=2"
    else:  # bilingual
        style = "FontSize=20,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=50,Alignment=2"
    
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', clean_video,
        '-vf', f"subtitles={subtitle_file}:force_style='{style}'",
        '-c:a', 'copy',
        output_video
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        print(f"✅ {subtitle_type}字幕视频创建成功: {output_video}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建{subtitle_type}字幕视频失败: {e}")
        return False

def backup_existing_files():
    """备份现有文件"""
    print("💾 备份现有文件...")
    
    files_to_backup = [
        "output/VP9_segment_2m36s-5m59s.mp4",
        "output/VP9_segment_2m36s-5m59s_chinese.mp4",
        "output/VP9_segment_2m36s-5m59s_bilingual.mp4"
    ]
    
    backup_dir = "output/backup_" + str(int(time.time()))
    os.makedirs(backup_dir, exist_ok=True)
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            backup_path = os.path.join(backup_dir, os.path.basename(file_path))
            shutil.copy2(file_path, backup_path)
            print(f"   ✅ 已备份: {file_path} -> {backup_path}")
    
    print(f"📁 备份目录: {backup_dir}")
    return backup_dir

def main():
    """主函数"""
    print("🔧 双层字幕问题修复工具")
    print("="*50)
    
    # 检查当前视频状态
    current_video = "output/VP9_segment_2m36s-5m59s.mp4"
    chinese_video = "output/VP9_segment_2m36s-5m59s_chinese.mp4"
    bilingual_video = "output/VP9_segment_2m36s-5m59s_bilingual.mp4"
    
    if not os.path.exists(current_video):
        print(f"❌ 视频文件不存在: {current_video}")
        return
    
    print(f"🔍 检查当前视频: {current_video}")
    has_subtitles, size_mb, duration, bitrate = check_video_has_burned_subtitles(current_video)
    
    if has_subtitles:
        print(f"⚠️ 检测到当前视频可能已有烧录字幕")
        print(f"   这解释了为什么后续处理会产生双层字幕")
        print()
        
        # 寻找原始源
        source_video = find_clean_video_source()
        
        if source_video:
            print("🎯 修复方案:")
            print("1. 备份现有文件")
            print("2. 从原始源重新创建干净的视频片段")
            print("3. 重新生成单层字幕视频")
            print()
            
            choice = input("是否执行修复? (y/N): ").strip().lower()
            
            if choice == 'y':
                import time
                
                # 步骤1: 备份
                backup_dir = backup_existing_files()
                
                # 步骤2: 创建干净视频
                clean_video = "output/VP9_segment_2m36s-5m59s_clean.mp4"
                if create_clean_video_from_source(source_video, clean_video):
                    
                    # 步骤3: 重新创建字幕视频
                    chinese_srt = "output/VP9_segment_2m36s-5m59s_chinese.srt"
                    bilingual_srt = "output/VP9_segment_2m36s-5m59s_bilingual.srt"
                    
                    if os.path.exists(chinese_srt):
                        create_subtitle_only_video(clean_video, chinese_srt, chinese_video, "chinese")
                    
                    if os.path.exists(bilingual_srt):
                        create_subtitle_only_video(clean_video, bilingual_srt, bilingual_video, "bilingual")
                    
                    # 用干净版本替换原版本
                    shutil.move(clean_video, current_video)
                    
                    print("\n🎉 修复完成!")
                    print("📁 现在您有了:")
                    print(f"   🎬 干净原版: {current_video}")
                    if os.path.exists(chinese_video):
                        size = os.path.getsize(chinese_video) / (1024*1024)
                        print(f"   🇨🇳 中文字幕: {chinese_video} ({size:.1f}MB)")
                    if os.path.exists(bilingual_video):
                        size = os.path.getsize(bilingual_video) / (1024*1024)
                        print(f"   🌏 双语字幕: {bilingual_video} ({size:.1f}MB)")
                    print(f"   💾 备份文件: {backup_dir}")
                
            else:
                print("❌ 用户取消修复")
        else:
            print("💡 建议手动获取无字幕的原始视频源")
    else:
        print("✅ 当前视频看起来没有烧录字幕")
        print("   双层字幕问题可能来自其他原因")

if __name__ == "__main__":
    main() 