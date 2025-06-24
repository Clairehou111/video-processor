#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超高质量YouTube视频下载演示
解决视频清晰度问题的专用工具
"""

from video_processor import VideoProcessor
import os

def ultra_high_quality_demo():
    """超高质量视频下载演示"""
    print("🎯 超高质量YouTube视频下载器")
    print("=" * 50)
    print("🔧 解决清晰度问题的专用工具")
    print("✨ 特点：")
    print("   • 多策略尝试下载最高质量")
    print("   • 分离视频/音频流获得最佳质量")
    print("   • 详细的质量信息显示")
    print("   • 格式列表查看功能")
    print()
    
    # 获取用户输入
    youtube_url = input("🔗 请输入YouTube视频URL: ").strip()
    if not youtube_url:
        print("❌ 必须提供视频URL")
        return
    
    # 选择模式
    print("\n📋 选择下载模式:")
    print("1. 直接下载最高质量 (推荐)")
    print("2. 查看可用格式后选择")
    print("3. 对比标准vs高质量下载")
    
    mode = input("请选择模式 (1-3): ").strip()
    
    # 创建处理器
    processor = VideoProcessor()
    
    if mode == "1":
        print("\n🚀 启动高质量下载模式...")
        video_path, video_title = processor.download_youtube_video_high_quality(youtube_url)
        
        if video_path:
            print(f"\n🎉 超高质量下载完成!")
            print(f"📁 输出目录: {processor.output_dir}")
        else:
            print("\n❌ 下载失败")
            
    elif mode == "2":
        print("\n📋 查看可用格式并下载...")
        video_path, video_title = processor.download_youtube_video_high_quality(youtube_url, show_formats=True)
        
        if video_path:
            print(f"\n🎉 高质量下载完成!")
            print(f"📁 输出目录: {processor.output_dir}")
        else:
            print("\n❌ 下载失败")
            
    elif mode == "3":
        print("\n⚖️ 对比下载模式...")
        
        # 标准下载
        print("\n📥 1. 标准质量下载:")
        std_path, std_title = processor.download_youtube_video(youtube_url, quality="1080p")
        
        # 高质量下载
        print("\n📥 2. 超高质量下载:")
        hq_path, hq_title = processor.download_youtube_video_high_quality(youtube_url)
        
        # 对比结果
        if std_path and hq_path:
            print("\n📊 质量对比结果:")
            print("=" * 40)
            
            # 获取文件大小
            std_size = os.path.getsize(std_path) / (1024*1024)
            hq_size = os.path.getsize(hq_path) / (1024*1024)
            
            print(f"📁 标准版: {os.path.basename(std_path)}")
            print(f"   文件大小: {std_size:.2f} MB")
            print(f"📁 高质量版: {os.path.basename(hq_path)}")
            print(f"   文件大小: {hq_size:.2f} MB")
            print(f"📈 大小差异: {((hq_size/std_size-1)*100):+.1f}%")
            
            print(f"\n✅ 两个版本都已保存到: {processor.output_dir}")
    else:
        print("❌ 无效选择")

def show_quality_tips():
    """显示质量优化建议"""
    print("\n💡 视频清晰度优化建议:")
    print("=" * 40)
    print("🎯 下载方面:")
    print("   • 使用 bestvideo+bestaudio 格式")
    print("   • 优先选择mp4容器格式")
    print("   • 启用ffmpeg合并选项")
    print()
    print("🔍 诊断方法:")
    print("   • 对比原视频格式列表")
    print("   • 检查实际下载的格式ID")
    print("   • 查看码率和分辨率信息")
    print()
    print("⚙️ 处理优化:")
    print("   • 使用CRF而非固定码率")
    print("   • 选择合适的编码预设")
    print("   • 避免不必要的重编码")

def main():
    """主函数"""
    try:
        ultra_high_quality_demo()
        show_quality_tips()
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 出现错误: {str(e)}")

if __name__ == "__main__":
    main() 