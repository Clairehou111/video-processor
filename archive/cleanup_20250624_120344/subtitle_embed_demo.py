#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字幕嵌入演示脚本 - 将中文字幕直接嵌入到视频中
"""

from video_processor import VideoProcessor
import os

def subtitle_embed_demo():
    """字幕嵌入演示"""
    print("=== 字幕嵌入视频演示 ===")
    print("本演示将把中文字幕直接嵌入到视频中")
    print()
    
    # 获取用户输入
    youtube_url = input("请输入YouTube视频URL (直接回车使用默认): ").strip()
    if not youtube_url:
        youtube_url = "https://www.youtube.com/watch?v=dp6BIDCZRic"
        print(f"使用默认URL: {youtube_url}")
    
    watermark_text = input("请输入水印文字 (默认: 字幕演示): ").strip()
    if not watermark_text:
        watermark_text = "字幕演示"
    
    # 字幕选择
    print("\n字幕嵌入选项:")
    print("1. 嵌入字幕到视频 (推荐)")
    print("2. 只生成SRT文件，不嵌入")
    print("3. 同时生成两个版本")
    
    embed_choice = input("请选择 (1-3, 默认1): ").strip()
    
    # 质量选择
    print("\n视频质量选项:")
    print("1. 1080p - Full HD (推荐)")
    print("2. 720p - HD") 
    print("3. 480p - 标清")
    print("4. best - 最佳可用")
    
    quality_choice = input("请选择质量 (1-4, 默认1080p): ").strip()
    
    quality_map = {
        "1": "1080p",
        "2": "720p", 
        "3": "480p",
        "4": "best"
    }
    quality = quality_map.get(quality_choice, "1080p")
    
    print(f"\n开始处理...")
    print(f"视频URL: {youtube_url}")
    print(f"水印文字: {watermark_text}")
    print(f"视频质量: {quality}")
    
    # 创建处理器
    processor = VideoProcessor()
    
    try:
        if embed_choice == "2":
            # 只生成SRT文件
            print("模式: 只生成SRT字幕文件")
            result = processor.process_video(
                youtube_url=youtube_url,
                watermark_text=watermark_text,
                quality=quality,
                embed_subtitles=False
            )
        elif embed_choice == "3":
            # 生成两个版本
            print("模式: 生成两个版本")
            print("\n--- 第一步: 生成嵌入字幕版本 ---")
            result1 = processor.process_video(
                youtube_url=youtube_url,
                watermark_text=watermark_text,
                quality=quality,
                embed_subtitles=True
            )
            
            print("\n--- 第二步: 生成外挂字幕版本 ---")
            result2 = processor.process_video(
                youtube_url=youtube_url,
                watermark_text=watermark_text + "_外挂",
                quality=quality,
                embed_subtitles=False
            )
            result = result1  # 主要结果
        else:
            # 默认：嵌入字幕
            print("模式: 嵌入字幕到视频")
            result = processor.process_video(
                youtube_url=youtube_url,
                watermark_text=watermark_text,
                quality=quality,
                embed_subtitles=True
            )
        
        if result:
            print(f"\n🎉 字幕嵌入处理成功！")
            print(f"主输出文件: {result}")
            
            # 显示所有生成的文件
            print("\n📁 生成的所有文件:")
            files_info = []
            for file in os.listdir(processor.output_dir):
                if file.endswith(('.mp4', '.srt', '.png')):
                    file_path = os.path.join(processor.output_dir, file)
                    size_mb = os.path.getsize(file_path) / (1024*1024)
                    files_info.append((file, size_mb))
            
            # 按文件大小排序
            files_info.sort(key=lambda x: x[1], reverse=True)
            for file, size_mb in files_info:
                if "subtitles" in file:
                    print(f"  🎬 {file} ({size_mb:.2f}MB) ← 嵌入字幕版本")
                elif file.endswith('.mp4'):
                    print(f"  📹 {file} ({size_mb:.2f}MB)")
                elif file.endswith('.srt'):
                    print(f"  📝 {file} ({size_mb:.2f}MB) ← SRT字幕文件")
                else:
                    print(f"  🖼️ {file} ({size_mb:.2f}MB)")
            
            print(f"\n💡 使用说明:")
            print(f"• 嵌入字幕的视频可以直接播放，无需额外字幕文件")
            print(f"• SRT文件可以在支持外挂字幕的播放器中使用")
            print(f"• 推荐使用VLC播放器获得最佳体验")
            
            print(f"\n📂 输出目录: {processor.output_dir}")
        else:
            print("\n❌ 处理失败")
            
    except Exception as e:
        print(f"\n❌ 处理过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    subtitle_embed_demo() 