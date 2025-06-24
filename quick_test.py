#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本
"""

from video_processor import VideoProcessor

def test_with_sample_video():
    """使用示例视频进行测试"""
    print("=== 快速测试模式 ===")
    
    # 一些适合测试的短视频URL
    test_urls = [
        "https://www.youtube.com/watch?v=aqz-KE-bpKQ",  # 短视频示例
        "https://www.youtube.com/watch?v=ScMzIvxBSi4",  # 英文教程短视频
    ]
    
    print("选择测试视频:")
    for i, url in enumerate(test_urls, 1):
        print(f"{i}. {url}")
    
    choice = input("选择视频编号 (直接回车使用第1个): ").strip()
    
    if choice == "2":
        selected_url = test_urls[1]
    else:
        selected_url = test_urls[0]
    
    watermark_text = input("输入水印文字 (默认: 测试水印): ").strip()
    if not watermark_text:
        watermark_text = "测试水印"
    
    print(f"\n正在处理视频: {selected_url}")
    print(f"水印文字: {watermark_text}")
    
    processor = VideoProcessor()
    
    try:
        result = processor.process_video(selected_url, watermark_text, quality="480p")
        
        if result:
            print(f"\n✅ 测试成功！")
            print(f"输出文件: {result}")
            print(f"输出目录: {processor.output_dir}")
        else:
            print("\n❌ 测试失败")
            
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_sample_video() 