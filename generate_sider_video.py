#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Sider AI翻译字幕生成最终视频
保存到指定的目录中
"""

import os
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont
import textwrap

def setup_target_directory():
    """设置目标目录"""
    target_dir = "output/_jOTww0E0b4_Trump_seen_in_new_clip_released_by_filmmaker_following_Jan_6_committee_subpoena"
    os.makedirs(target_dir, exist_ok=True)
    return target_dir

def copy_sider_subtitles_to_target(target_dir):
    """将Sider翻译字幕复制到目标目录"""
    # 源文件路径
    source_chinese_srt = "output/real_sider_trump_translation/Trump_Sider_AI_Chinese_Subtitles.srt"
    source_review = "output/real_sider_trump_translation/Trump_Sider_AI_Translation_Review.txt"
    
    # 目标文件路径
    target_chinese_srt = os.path.join(target_dir, "Trump_Sider_Chinese_Subtitles.srt")
    target_review = os.path.join(target_dir, "Trump_Sider_Translation_Review.txt")
    
    # 复制字幕文件
    if os.path.exists(source_chinese_srt):
        shutil.copy2(source_chinese_srt, target_chinese_srt)
        print(f"✅ 已复制Sider中文字幕到: {target_chinese_srt}")
    
    if os.path.exists(source_review):
        shutil.copy2(source_review, target_review)
        print(f"✅ 已复制翻译对照文件到: {target_review}")
    
    # 复制bilibili水印
    source_bilibili_watermark = "output/bilibili_watermark.png"
    target_bilibili_watermark = os.path.join(target_dir, "bilibili_watermark.png")
    
    if os.path.exists(source_bilibili_watermark):
        shutil.copy2(source_bilibili_watermark, target_bilibili_watermark)
        print(f"✅ 已复制bilibili水印到: {target_bilibili_watermark}")
    else:
        print(f"⚠️ bilibili水印文件不存在: {source_bilibili_watermark}")
    
    return target_chinese_srt, target_review

def get_source_video_path():
    """获取源视频文件路径"""
    source_video = "output/sider__jOTww0E0b4_Trump_seen_in_new_clip_released_by_filmmaker_following_Jan_6_committee_subpoena/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena.mp4"
    
    if os.path.exists(source_video):
        return source_video
    else:
        print(f"❌ 源视频文件不存在: {source_video}")
        return None

def create_sider_watermark(target_dir):
    """创建Sider专用水印"""
    watermark_path = os.path.join(target_dir, "sider_watermark.png")
    
    # 创建水印图片
    width, height = 400, 100
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        # 使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
    except:
        font = ImageFont.load_default()
    
    # 水印文字
    watermark_text = "Sider AI翻译 • 董卓主演脱口秀"
    
    # 获取文字尺寸
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 居中绘制文字
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # 绘制阴影
    draw.text((x+2, y+2), watermark_text, font=font, fill=(0, 0, 0, 180))
    # 绘制主文字
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 220))
    
    img.save(watermark_path)
    print(f"✅ 已创建Sider水印: {watermark_path}")
    return watermark_path

def generate_video_with_sider_subtitles(source_video, chinese_srt, target_dir, watermark_path):
    """生成带Sider字幕和水印的视频"""
    
    output_video = os.path.join(target_dir, "Trump_Sider_AI_Final_Video.mp4")
    
    print("🎬 正在生成带Sider字幕的最终视频...")
    
    # FFmpeg命令：添加中文字幕和水印
    cmd = [
        'ffmpeg', '-y',
        '-i', source_video,
        '-i', watermark_path,
        '-filter_complex', 
        f"[0:v]subtitles='{chinese_srt}':force_style='FontName=PingFang SC,FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Shadow=1,MarginV=50'[subtitled];"
        f"[1:v]scale=400:100[watermark];"
        f"[subtitled][watermark]overlay=W-w-20:H-h-20[output]",
        '-map', '[output]',
        '-map', '0:a',
        '-c:a', 'copy',
        '-preset', 'medium',
        '-crf', '23',
        output_video
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ 视频生成成功: {output_video}")
        return output_video
    except subprocess.CalledProcessError as e:
        print(f"❌ 视频生成失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None

def generate_dual_subtitle_video(source_video, target_dir):
    """生成英中双语字幕版本 - 优化版"""
    
    # 获取英文字幕路径
    english_srt = "output/sider__jOTww0E0b4_Trump_seen_in_new_clip_released_by_filmmaker_following_Jan_6_committee_subpoena/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena_english.srt"
    chinese_srt = os.path.join(target_dir, "Trump_Sider_Chinese_Subtitles.srt")
    
    if not os.path.exists(english_srt):
        print("⚠️ 英文字幕文件不存在，跳过双语版本生成")
        return None
    
    output_video = os.path.join(target_dir, "Trump_Sider_AI_Dual_Subtitles.mp4")
    
    # 使用bilibili水印
    bilibili_watermark_path = os.path.join(target_dir, "bilibili_watermark.png")
    
    print("🎬 正在生成优化版Sider双语字幕版本...")
    print("✨ 优化内容: 布局改进、bilibili水印右上角、颜色协调")
    
    # FFmpeg命令：添加优化的双语字幕和bilibili水印
    cmd = [
        'ffmpeg', '-y',
        '-i', source_video,
        '-i', bilibili_watermark_path,
        '-filter_complex',
        # 英文字幕在上方，增大间距，统一字体大小和颜色
        f"[0:v]subtitles='{english_srt}':force_style='FontName=Arial,FontSize=22,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Shadow=1,MarginV=120,Alignment=2'[english];"
        # 中文字幕在下方，改为白色提高可读性，增加阴影效果
        f"[english]subtitles='{chinese_srt}':force_style='FontName=PingFang SC,FontSize=22,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Shadow=1,MarginV=40,Alignment=2'[dual];"
        # bilibili水印缩放并放置在右上角
        f"[1:v]scale=200:50[watermark];"
        f"[dual][watermark]overlay=W-w-20:20[output]",
        '-map', '[output]',
        '-map', '0:a',
        '-c:a', 'copy',
        '-preset', 'medium',
        '-crf', '23',
        output_video
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ 优化版双语字幕视频生成成功: {output_video}")
        print("🎯 优化效果:")
        print("   • 英文字幕上移至120px位置，避免重叠")
        print("   • 中文字幕下移至40px位置，增加间距")
        print("   • 统一字体大小为22px，视觉更协调")
        print("   • 两个字幕都使用白色，提高可读性")
        print("   • 增加阴影效果，增强对比度")
        print("   • bilibili水印放置在右上角")
        print("   • 水印尺寸调整为200x50，不遮挡内容")
        return output_video
    except subprocess.CalledProcessError as e:
        print(f"❌ 双语视频生成失败: {e}")
        print(f"错误详情: {e.stderr}")
        return None

def create_video_summary(target_dir, videos_created):
    """创建视频生成总结文件"""
    summary_path = os.path.join(target_dir, "Sider_Video_Generation_Summary.txt")
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("🎬 Sider AI视频生成总结\n")
        f.write("=" * 50 + "\n")
        f.write(f"生成时间: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("翻译引擎: 真实Sider AI (Cursor MCP)\n")
        f.write("翻译模型: Claude Sonnet 4\n")
        f.write("视频风格: 搞笑幽默特朗普幕后花絮\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("📁 生成的视频文件:\n")
        for i, video in enumerate(videos_created, 1):
            if video:
                f.write(f"{i}. {os.path.basename(video)}\n")
        
        f.write(f"\n📝 相关文件:\n")
        f.write("- Trump_Sider_Chinese_Subtitles.srt (Sider中文字幕)\n")
        f.write("- Trump_Sider_Translation_Review.txt (翻译对照)\n")
        f.write("- sider_watermark.png (专用水印)\n")
        
        f.write(f"\n🌟 特色:\n")
        f.write("✅ 使用真实Sider AI翻译\n")
        f.write("✅ Claude Sonnet 4模型\n")
        f.write("✅ 搞笑幽默风格\n")
        f.write("✅ 特朗普风格保持\n")
        f.write("✅ 专业视频制作\n")
    
    print(f"📋 已创建视频生成总结: {summary_path}")

def main():
    """主函数"""
    print("🎬 Sider AI视频生成器")
    print("=" * 50)
    print("🌟 使用真实Sider AI翻译字幕")
    print("🤖 翻译模型: Claude Sonnet 4")
    print("😄 风格: 搞笑幽默")
    print("📁 目标目录: _jOTww0E0b4_Trump_seen_in_new_clip...")
    print("=" * 50)
    
    # 1. 设置目标目录
    target_dir = setup_target_directory()
    print(f"📁 目标目录: {target_dir}")
    
    # 2. 获取源视频
    source_video = get_source_video_path()
    if not source_video:
        print("❌ 无法找到源视频文件")
        return
    
    # 3. 复制Sider字幕到目标目录
    chinese_srt, review_file = copy_sider_subtitles_to_target(target_dir)
    
    # 4. 创建Sider专用水印
    watermark_path = create_sider_watermark(target_dir)
    
    # 5. 生成带Sider字幕的视频
    video1 = generate_video_with_sider_subtitles(source_video, chinese_srt, target_dir, watermark_path)
    
    # 6. 生成双语字幕版本
    video2 = generate_dual_subtitle_video(source_video, target_dir)
    
    # 7. 创建总结文件
    videos_created = [video1, video2]
    create_video_summary(target_dir, videos_created)
    
    print(f"\n🎉 Sider AI视频生成完成!")
    print(f"📁 所有文件保存在: {target_dir}")
    print(f"\n📹 生成的视频:")
    if video1:
        print(f"   1. {os.path.basename(video1)} (Sider中文字幕版)")
    if video2:
        print(f"   2. {os.path.basename(video2)} (Sider双语字幕版)")
    
    print(f"\n🌟 特色:")
    print("✅ 真实Sider AI翻译 + Claude Sonnet 4")
    print("✅ 搞笑幽默的特朗普幕后风格")
    print("✅ 专业视频制作质量")
    print("✅ 自定义Sider水印")

if __name__ == "__main__":
    main() 