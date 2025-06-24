#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版工作流程演示脚本
展示：独立文件夹 + 字幕确认 + B站生成的完整流程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from improved_video_processor import ImprovedVideoProcessor
from improved_bilibili_generator import ImprovedBilibiliGenerator

def demo_workflow():
    """演示完整的改进版工作流程"""
    print("🎬 改进版视频处理工作流程演示")
    print("=" * 50)
    print("本演示将展示以下改进功能：")
    print("1. ✅ 每个视频创建独立输出文件夹")
    print("2. ✅ 生成字幕后先让用户确认")
    print("3. ✅ 支持手动编辑字幕文件")
    print("4. ✅ 从独立文件夹生成B站版本")
    print("=" * 50)
    
    # 使用你之前提供的YouTube URL作为演示
    youtube_url = "https://www.youtube.com/watch?v=_jOTww0E0b4"
    watermark_text = "董卓主演脱口秀"
    
    print(f"📹 演示视频: {youtube_url}")
    print(f"🏷️ 水印文字: {watermark_text}")
    
    # 询问用户是否继续
    confirm = input("\n是否开始演示？(y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '是', '好']:
        print("❌ 演示已取消")
        return
    
    print("\n" + "="*50)
    print("第一步：下载视频并生成字幕（支持确认功能）")
    print("="*50)
    
    # 第一步：使用改进版处理器
    processor = ImprovedVideoProcessor()
    
    try:
        result = processor.process_video_with_confirmation(
            youtube_url=youtube_url,
            watermark_text=watermark_text,
            quality="1080p"
        )
        
        if not result:
            print("❌ 视频处理失败或被取消")
            return
        
        print(f"\n✅ 第一步完成!")
        print(f"📁 视频文件夹: {result['output_dir']}")
        print(f"📹 视频文件: {os.path.basename(result['video_path'])}")
        print(f"📝 英文字幕: {os.path.basename(result['english_srt'])}")
        print(f"📝 中文字幕: {os.path.basename(result['chinese_srt'])}")
        
        print("\n" + "="*50)
        print("第二步：从独立文件夹生成B站版本")
        print("="*50)
        
        # 第二步：使用改进版B站生成器
        generator = ImprovedBilibiliGenerator()
        
        print(f"🔄 正在为文件夹生成B站版本: {os.path.basename(result['output_dir'])}")
        
        # 自动生成推荐版本（高清双语版）
        bilibili_result = generator.generate_bilibili_version(
            video_folder=result['output_dir'],
            version_type="dual",
            quality="hd"
        )
        
        if bilibili_result:
            print(f"\n🎉 B站版本生成完成!")
            print(f"📁 输出文件: {os.path.basename(bilibili_result)}")
            
            # 显示文件夹内容
            print(f"\n📂 {os.path.basename(result['output_dir'])} 文件夹内容:")
            for file in sorted(os.listdir(result['output_dir'])):
                if os.path.isfile(os.path.join(result['output_dir'], file)):
                    file_path = os.path.join(result['output_dir'], file)
                    file_size = os.path.getsize(file_path) / 1024 / 1024
                    if file.endswith('.mp4'):
                        print(f"   🎬 {file} ({file_size:.1f} MB)")
                    elif file.endswith('.srt'):
                        print(f"   📝 {file}")
                    elif file.endswith('.png'):
                        print(f"   🏷️ {file}")
                    elif file.endswith('.txt'):
                        print(f"   📋 {file}")
                    else:
                        print(f"   📄 {file}")
            
            print(f"\n🎯 推荐上传到B站的文件:")
            print(f"   {os.path.basename(bilibili_result)}")
            
        else:
            print("❌ B站版本生成失败")
    
    except Exception as e:
        print(f"❌ 演示过程中出错: {str(e)}")

def show_existing_folders():
    """显示现有的视频文件夹"""
    output_dir = "output"
    if not os.path.exists(output_dir):
        print("❌ output目录不存在")
        return
    
    folders = []
    files_in_root = []
    
    for item in os.listdir(output_dir):
        if item.startswith('.'):
            continue
        item_path = os.path.join(output_dir, item)
        if os.path.isdir(item_path):
            folders.append(item)
        elif os.path.isfile(item_path):
            files_in_root.append(item)
    
    # 显示独立文件夹
    if folders:
        print("📁 独立视频文件夹:")
        for i, folder in enumerate(sorted(folders), 1):
            folder_path = os.path.join(output_dir, folder)
            
            # 统计文件夹内容
            video_count = 0
            srt_count = 0
            for file in os.listdir(folder_path):
                if file.endswith('.mp4'):
                    video_count += 1
                elif file.endswith('.srt'):
                    srt_count += 1
            
            print(f"{i}. {folder}")
            print(f"   📹 视频文件: {video_count}个")
            print(f"   📝 字幕文件: {srt_count}个")
    else:
        print("📁 未找到独立视频文件夹")
    
    # 显示根目录下的散乱文件
    if files_in_root:
        print(f"\n📄 output根目录下的文件 (共{len(files_in_root)}个):")
        video_files = [f for f in files_in_root if f.endswith('.mp4')]
        srt_files = [f for f in files_in_root if f.endswith('.srt')]
        
        if video_files:
            print(f"   🎬 视频文件: {len(video_files)}个")
            for video in sorted(video_files)[:3]:  # 只显示前3个
                print(f"      - {video}")
            if len(video_files) > 3:
                print(f"      ... 还有{len(video_files)-3}个")
        
        if srt_files:
            print(f"   📝 字幕文件: {len(srt_files)}个")
        
        print("💡 建议：旧文件可以用改进版脚本重新组织到独立文件夹")
    
    if not folders and not files_in_root:
        print("❌ output目录为空")
        print("💡 请先运行演示生成一些视频文件夹")

def main():
    """主菜单"""
    while True:
        print("\n🎬 改进版视频处理系统")
        print("=" * 30)
        print("1. 🚀 运行完整工作流程演示")
        print("2. 📁 查看现有视频文件夹")
        print("3. 🎬 单独运行视频处理器")
        print("4. 📺 单独运行B站生成器") 
        print("5. ❌ 退出")
        
        choice = input("请选择 (1-5): ").strip()
        
        if choice == "1":
            demo_workflow()
        elif choice == "2":
            show_existing_folders()
        elif choice == "3":
            print("🔄 启动改进版视频处理器...")
            from improved_video_processor import main as processor_main
            processor_main()
        elif choice == "4":
            print("🔄 启动改进版B站生成器...")
            from improved_bilibili_generator import main as generator_main
            generator_main()
        elif choice == "5":
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main() 