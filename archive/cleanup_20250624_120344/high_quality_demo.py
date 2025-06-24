#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高清视频处理演示脚本
"""

from video_processor import VideoProcessor
import os

def high_quality_demo():
    """高清视频处理演示"""
    print("=== 高清YouTube视频处理演示 ===")
    print("本演示将使用1080p高清质量进行处理")
    print()
    
    # 获取用户输入
    youtube_url = input("请输入YouTube视频URL: ").strip()
    if not youtube_url:
        youtube_url = "https://www.youtube.com/watch?v=dp6BIDCZRic"
        print(f"使用默认URL: {youtube_url}")
    
    watermark_text = input("请输入水印文字 (默认: 高清演示): ").strip()
    if not watermark_text:
        watermark_text = "高清演示"
    
    # 质量选择
    print("\n选择视频质量:")
    print("1. best - 最佳可用质量")
    print("2. 1080p - Full HD")
    print("3. 720p - HD")
    print("4. 480p - 标清")
    
    quality_choice = input("请选择质量 (1-4, 默认1080p): ").strip()
    
    quality_map = {
        "1": "best",
        "2": "1080p", 
        "3": "720p",
        "4": "480p"
    }
    quality = quality_map.get(quality_choice, "1080p")
    
    print(f"\n开始处理...")
    print(f"视频URL: {youtube_url}")
    print(f"水印文字: {watermark_text}")
    print(f"视频质量: {quality}")
    print()
    
    # 创建处理器并执行
    processor = VideoProcessor()
    
    try:
        result = processor.process_video(
            youtube_url=youtube_url,
            watermark_text=watermark_text,
            quality=quality
        )
        
        if result:
            print(f"\n🎉 高清视频处理成功！")
            print(f"输出视频: {result}")
            print(f"字幕文件: {result.replace('_with_watermark.mp4', '_chinese.srt')}")
            
            # 显示文件信息
            print("\n📁 生成的文件详情:")
            for file in os.listdir(processor.output_dir):
                if file.endswith(('.mp4', '.srt', '.png')):
                    file_path = os.path.join(processor.output_dir, file)
                    size_mb = os.path.getsize(file_path) / (1024*1024)
                    print(f"  📄 {file} ({size_mb:.2f}MB)")
            
            print(f"\n输出目录: {processor.output_dir}")
        else:
            print("\n❌ 处理失败")
            
    except Exception as e:
        print(f"\n❌ 处理过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    high_quality_demo() 