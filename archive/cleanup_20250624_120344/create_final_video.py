#!/usr/bin/env python3
"""
生成最终视频 - 使用提供的中文字幕和水印
"""

import os
import sys
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_watermark(text="高质量中文字幕", output_path="output/watermark.png"):
    """创建水印图片"""
    try:
        # 创建水印图片
        img = Image.new('RGBA', (300, 60), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
        except:
            # 如果没有中文字体，使用默认字体
            font = ImageFont.load_default()
        
        # 绘制文字
        try:
            # 新版PIL使用textbbox
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # 旧版PIL使用textsize
            text_width, text_height = draw.textsize(text, font=font)
        
        x = (300 - text_width) // 2
        y = (60 - text_height) // 2
        
        # 添加阴影效果
        draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 128))  # 阴影
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))  # 主文字
        
        img.save(output_path)
        print(f"✅ 水印创建成功: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 水印创建失败: {e}")
        return None

def parse_srt_subtitles(srt_file):
    """解析SRT字幕文件"""
    subtitles = []
    
    try:
        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        blocks = content.split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                # 序号
                index = lines[0]
                # 时间
                time_line = lines[1]
                # 字幕文本
                text = '\n'.join(lines[2:])
                
                # 解析时间
                start_str, end_str = time_line.split(' --> ')
                start_time = parse_srt_time(start_str)
                end_time = parse_srt_time(end_str)
                
                subtitles.append({
                    'start': start_time,
                    'end': end_time,
                    'text': text
                })
        
        print(f"✅ 解析字幕完成，共 {len(subtitles)} 个片段")
        return subtitles
        
    except Exception as e:
        print(f"❌ 字幕解析失败: {e}")
        return []

def parse_srt_time(time_str):
    """将SRT时间格式转换为秒数"""
    # 格式: 00:01:23,456
    time_part, ms_part = time_str.split(',')
    h, m, s = map(int, time_part.split(':'))
    ms = int(ms_part)
    
    total_seconds = h * 3600 + m * 60 + s + ms / 1000.0
    return total_seconds

def create_subtitle_clip(subtitle, video_width, video_height):
    """创建单个字幕片段"""
    try:
        # 字幕样式
        fontsize = 32
        color = 'yellow'
        stroke_color = 'black'
        stroke_width = 3
        
        # 创建字幕
        txt_clip = TextClip(
            subtitle['text'],
            fontsize=fontsize,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            method='caption',
            size=(video_width - 100, None),
            align='center'
        ).set_start(subtitle['start']).set_duration(subtitle['end'] - subtitle['start'])
        
        # 设置位置（底部居中）
        txt_clip = txt_clip.set_position(('center', video_height - 120))
        
        return txt_clip
        
    except Exception as e:
        print(f"❌ 字幕片段创建失败: {e}")
        return None

def create_final_video(video_path, srt_path, watermark_text="高质量中文字幕", output_path=None):
    """创建最终带字幕和水印的视频"""
    
    if not output_path:
        base_name = os.path.basename(video_path).rsplit('.', 1)[0]
        output_path = f"output/{base_name}_final_chinese.mp4"
    
    try:
        print("🔄 加载原视频...")
        video = VideoFileClip(video_path)
        
        print("🔄 创建水印...")
        watermark_img_path = create_watermark(watermark_text)
        if not watermark_img_path:
            return None
        
        # 创建水印片段
        watermark = (ImageClip(watermark_img_path, transparent=True, duration=video.duration)
                    .set_position(('right', 'top'))
                    .resize(0.3))  # 缩小水印
        
        print("🔄 解析中文字幕...")
        subtitles = parse_srt_subtitles(srt_path)
        if not subtitles:
            return None
        
        print("🔄 创建字幕片段...")
        subtitle_clips = []
        for i, subtitle in enumerate(subtitles):
            if i % 10 == 0:  # 每10个片段显示进度
                print(f"   处理字幕 {i+1}/{len(subtitles)}")
                
            clip = create_subtitle_clip(subtitle, video.w, video.h)
            if clip:
                subtitle_clips.append(clip)
        
        print(f"✅ 创建了 {len(subtitle_clips)} 个字幕片段")
        
        print("🔄 合成最终视频...")
        # 合成所有元素
        final_clips = [video, watermark] + subtitle_clips
        final_video = CompositeVideoClip(final_clips)
        
        print("🔄 导出视频...")
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        # 清理
        video.close()
        final_video.close()
        
        print(f"✅ 最终视频创建成功!")
        print(f"   输出文件: {output_path}")
        
        # 显示文件信息
        file_size = os.path.getsize(output_path) / 1024 / 1024
        print(f"   文件大小: {file_size:.2f} MB")
        
        return output_path
        
    except Exception as e:
        print(f"❌ 视频创建失败: {e}")
        return None

def main():
    """主函数"""
    print("🎬 创建最终中文字幕视频")
    print("=" * 50)
    
    # 查找现有的视频文件
    video_files = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith(('.mp4', '.avi', '.mov')) and 'final' not in file:
                video_files.append(os.path.join("output", file))
    
    if not video_files:
        print("❌ 未找到视频文件，请先运行视频下载脚本")
        return
    
    # 使用第一个找到的视频文件
    video_path = video_files[0]
    srt_path = "chinese_subtitles.srt"
    
    if not os.path.exists(srt_path):
        print(f"❌ 中文字幕文件不存在: {srt_path}")
        return
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 字幕文件: {srt_path}")
    
    # 创建最终视频
    result = create_final_video(
        video_path=video_path,
        srt_path=srt_path,
        watermark_text="高质量中文字幕"
    )
    
    if result:
        print(f"\n🎉 任务完成!")
        print(f"🎬 带中文字幕的视频已生成: {result}")
        print(f"\n💡 你现在可以:")
        print(f"   1. 播放视频查看效果")
        print(f"   2. 分享给朋友观看")
        print(f"   3. 上传到视频平台")
    else:
        print(f"\n❌ 视频生成失败")

if __name__ == "__main__":
    main() 