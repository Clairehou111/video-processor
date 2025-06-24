#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示脚本：使用一个短YouTube视频来展示所有功能
"""

from video_processor import VideoProcessor
import os

def demo():
    """演示视频处理功能"""
    print("=== YouTube视频处理工具演示 ===")
    print("这个演示将下载一个短视频并进行处理")
    print()
    
    # 使用一个短视频URL进行演示
    demo_url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"  # 大约30秒的短视频
    watermark_text = "演示水印"
    
    print(f"演示视频URL: {demo_url}")
    print(f"水印文字: {watermark_text}")
    print()
    
    # 创建处理器
    processor = VideoProcessor()
    
    try:
        print("开始处理...")
        result = processor.process_video(
            youtube_url=demo_url,
            watermark_text=watermark_text,
            quality="1080p"  # 使用1080p高清质量
        )
        
        if result:
            print(f"\n🎉 演示成功完成！")
            print(f"处理后的视频: {result}")
            print(f"输出目录: {processor.output_dir}")
            
            # 列出所有生成的文件
            print("\n生成的文件:")
            for file in os.listdir(processor.output_dir):
                print(f"  - {file}")
        else:
            print("\n❌ 演示失败")
            
    except Exception as e:
        print(f"\n❌ 演示过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()

def show_info():
    """显示项目信息"""
    print("=== 项目功能说明 ===")
    print("1. YouTube视频下载")
    print("2. 使用Whisper进行语音识别")
    print("3. 简单英中翻译（基于词典）")
    print("4. 添加水印")
    print("5. 生成带字幕的视频")
    print("6. 导出SRT字幕文件")
    print()
    print("注意：翻译功能使用简单词典，实际项目可集成更好的翻译API")
    print()

if __name__ == "__main__":
    show_info()
    
    choice = input("是否运行演示？(y/n): ").strip().lower()
    if choice in ['y', 'yes', '是']:
        demo()
    else:
        print("演示已取消")
        print("你可以直接运行 python video_processor.py 来使用完整功能") 