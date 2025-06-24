#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正字幕位置一致性的工作流
解决字幕忽高忽低的问题

字幕配置标准 (已验证的最佳设置):
- 中文字幕: PingFang SC, 22px, MarginV=60, 白色(&Hffffff)
- 英文字幕: Arial, 18px, MarginV=20, 白色(&Hffffff)  
- 水印: PingFang SC, 24px, 右上角(Alignment=9), MarginV=15, 白色
- 水印内容: "董卓主演脱口秀"
- 水印定位: MarginL=10, MarginR=15, MarginV=15

这些参数经过测试，确保:
1. 字幕位置稳定，不会忽高忽低
2. 中文字幕在英文字幕上方，间距适中
3. 白色字幕在各种背景下清晰可见
4. 水印位置固定在右上角
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def print_step(step_num, title, description=""):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"📍 步骤 {step_num}: {title}")
    if description:
        print(f"   {description}")
    print(f"{'='*60}")

def srt_time_to_seconds(time_str):
    """将SRT时间格式转换为秒数"""
    time_str = time_str.replace(',', '.')
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def seconds_to_ass_time(seconds):
    """将秒数转换为ASS时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:01d}:{minutes:02d}:{secs:05.2f}"

def create_stable_ass_subtitles(english_srt, chinese_srt, output_path, subtitle_type="bilingual"):
    """创建位置稳定的ASS字幕 - 改进时间同步"""
    
    # 稳定的样式定义 - 调整中文字幕到英文字幕上方
    if subtitle_type == "bilingual":
        ass_content = """[Script Info]
Title: Bilingual Subtitles - Stable Positioning
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,PingFang SC,22,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,60,1
Style: English,Arial,18,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,20,1
Style: Watermark,PingFang SC,24,&Hffffff,&Hffffff,&H000000,&H80000000,1,0,0,0,100,100,0,0,1,1,0,9,10,15,15,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    else:
        ass_content = """[Script Info]
Title: Chinese Subtitles - Stable Positioning
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,PingFang SC,22,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,40,1
Style: Watermark,PingFang SC,24,&Hffffff,&Hffffff,&H000000,&H80000000,1,0,0,0,100,100,0,0,1,1,0,9,10,15,15,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    # 添加水印
    ass_content += "Dialogue: 0,0:00:00.00,9:59:59.99,Watermark,,0,0,0,,董卓主演脱口秀\n"
    
    # 读取中文字幕 - 改进时间处理
    chinese_subtitles = []
    if os.path.exists(chinese_srt):
        with open(chinese_srt, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析SRT格式，精确处理时间
        blocks = content.strip().split('\n\n')
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                time_line = lines[1]
                text_lines = lines[2:]
                text = ' '.join(text_lines).strip()
                
                # 解析时间，确保精确同步
                if '-->' in time_line:
                    start_str, end_str = time_line.split(' --> ')
                    start_str = start_str.strip()
                    end_str = end_str.strip()
                    
                    # 转换为ASS时间格式，保持精确性
                    start_seconds = srt_time_to_seconds(start_str)
                    end_seconds = srt_time_to_seconds(end_str)
                    start_ass = seconds_to_ass_time(start_seconds)
                    end_ass = seconds_to_ass_time(end_seconds)
                    
                    # 强制使用固定的MarginV确保位置一致
                    if subtitle_type == "bilingual":
                        ass_content += f"Dialogue: 0,{start_ass},{end_ass},Chinese,,0,0,0,,{text}\n"
                    else:
                        ass_content += f"Dialogue: 0,{start_ass},{end_ass},Chinese,,0,0,0,,{text}\n"
    
    # 添加英文字幕（如果是双语）- 改进时间处理
    if subtitle_type == "bilingual" and os.path.exists(english_srt):
        with open(english_srt, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = content.strip().split('\n\n')
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                time_line = lines[1]
                text_lines = lines[2:]
                text = ' '.join(text_lines).strip()
                
                if '-->' in time_line:
                    start_str, end_str = time_line.split(' --> ')
                    start_str = start_str.strip()
                    end_str = end_str.strip()
                    
                    # 转换为ASS时间格式，保持精确性
                    start_seconds = srt_time_to_seconds(start_str)
                    end_seconds = srt_time_to_seconds(end_str)
                    start_ass = seconds_to_ass_time(start_seconds)
                    end_ass = seconds_to_ass_time(end_seconds)
                    
                    # 强制使用固定的MarginV确保位置一致
                    ass_content += f"Dialogue: 0,{start_ass},{end_ass},English,,0,0,0,,{text}\n"
    
    # 保存ASS文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ass_content)
    
    print(f"✅ 稳定位置ASS字幕已生成: {output_path}")
    return True

def generate_video_with_stable_subtitles(video_path, ass_path, output_path):
    """使用稳定位置的字幕生成视频"""
    print(f"🔄 生成带稳定字幕的视频...")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "128k",
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # 获取文件大小
        file_size = os.path.getsize(output_path)
        size_mb = file_size / (1024 * 1024)
        
        print(f"✅ 稳定字幕视频生成完成: {size_mb:.1f}MB")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 视频生成失败: {e}")
        if e.stderr:
            print(f"错误详情: {e.stderr}")
        return False

def main():
    """主函数"""
    project_dir = "output/Ted_Cruz_&_Tucker_Carlson_Battle_Over_Iran_While_T_20250623_172209"
    
    if not os.path.exists(project_dir):
        print(f"❌ 项目目录不存在: {project_dir}")
        return
    
    print("📁 修正字幕位置一致性项目")
    print("🔧 解决问题: 字幕忽高忽低 → 固定稳定位置")
    print("🔄 使用调整后的中文字幕重新生成视频")
    
    # 查找文件
    video_file = None
    for file in os.listdir(project_dir):
        if file.endswith('.mp4') and not any(x in file for x in ['bilingual', 'chinese', 'final']):
            video_file = os.path.join(project_dir, file)
            break
    
    english_srt = f"{project_dir}/subtitles/Ted Cruz & Tucker Carlson Battle Over Iran While Trump Enters His Decorating Era ｜ The Daily Show_english.srt"
    chinese_srt = f"{project_dir}/subtitles/Ted Cruz & Tucker Carlson Battle Over Iran While Trump Enters His Decorating Era ｜ The Daily Show_chinese.srt"
    
    if not all([video_file, os.path.exists(english_srt), os.path.exists(chinese_srt)]):
        print(f"❌ 缺少必要文件")
        return
    
    print(f"🎬 处理视频: {os.path.basename(video_file)}")
    print(f"✅ 英文字幕: {os.path.basename(english_srt)}")
    print(f"✅ 中文字幕: {os.path.basename(chinese_srt)} (已调整)")
    
    print_step(1, "生成稳定位置双语视频", "使用固定MarginV确保字幕位置一致")
    
    # 生成稳定位置的双语ASS字幕
    bilingual_ass = f"{project_dir}/subtitles/bilingual_stable.ass"
    create_stable_ass_subtitles(english_srt, chinese_srt, bilingual_ass, "bilingual")
    
    # 生成双语视频
    bilingual_output = f"{project_dir}/final/Ted Cruz & Tucker Carlson Battle Over Iran While Trump Enters His Decorating Era ｜ The Daily Show_bilingual_stable.mp4"
    os.makedirs(os.path.dirname(bilingual_output), exist_ok=True)
    
    if generate_video_with_stable_subtitles(video_file, bilingual_ass, bilingual_output):
        print(f"✅ 稳定位置双语视频完成")
    
    print_step(2, "生成稳定位置中文视频", "中文字幕居中显示，位置固定")
    
    # 生成稳定位置的中文ASS字幕
    chinese_ass = f"{project_dir}/subtitles/chinese_stable.ass"
    create_stable_ass_subtitles(english_srt, chinese_srt, chinese_ass, "chinese")
    
    # 生成中文视频
    chinese_output = f"{project_dir}/final/Ted Cruz & Tucker Carlson Battle Over Iran While Trump Enters His Decorating Era ｜ The Daily Show_chinese_stable.mp4"
    
    if generate_video_with_stable_subtitles(video_file, chinese_ass, chinese_output):
        print(f"✅ 稳定位置中文视频完成")
    
    print_step(3, "完成稳定字幕视频生成")
    
    print(f"\n🎉 字幕位置修正完成！")
    print(f"📁 项目目录: {project_dir}")
    print(f"🎬 稳定双语视频: {bilingual_output}")
    print(f"🎬 稳定中文视频: {chinese_output}")
    print(f"\n✨ 特点:")
    print(f"   • 中文字幕位置固定稳定（不再忽高忽低）")
    print(f"   • 英文字幕位置固定在底部")
    print(f"   • 水印位置固定在右上角")
    print(f"   • 使用你调整过的中文字幕内容")

if __name__ == "__main__":
    main() 