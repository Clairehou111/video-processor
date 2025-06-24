#!/usr/bin/env python3
"""
创建TikTok定制版本 - 2:37秒结束，水印"董卓主演脱口秀"
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_custom_watermark(text="董卓主演脱口秀", output_path="output/tiktok_watermark.png"):
    """创建定制水印图片"""
    try:
        # 创建水印图片 - 稍微大一点以适应中文
        img = Image.new('RGBA', (350, 70), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            # 尝试使用系统中文字体
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 26)
        except:
            # 如果没有中文字体，使用默认字体
            font = ImageFont.load_default()
        
        # 计算文字尺寸
        try:
            # 新版PIL使用textbbox
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # 旧版PIL使用textsize
            text_width, text_height = draw.textsize(text, font=font)
        
        x = (350 - text_width) // 2
        y = (70 - text_height) // 2
        
        # 添加阴影效果
        draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 128))  # 阴影
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 220))  # 主文字
        
        img.save(output_path)
        print(f"✅ 定制水印创建成功: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 水印创建失败: {e}")
        return None

def create_tiktok_dual_subtitles():
    """创建TikTok版本的双语字幕视频 - 2:37结束"""
    
    # 找到原始视频
    video_files = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith('.mp4') and 'final' not in file and 'test' not in file and 'ffmpeg' not in file and 'dual' not in file and 'tiktok' not in file:
                video_files.append(os.path.join("output", file))
    
    if not video_files:
        print("❌ 未找到原始视频文件")
        return None
    
    video_path = video_files[0]
    english_srt = None
    chinese_srt = "chinese_subtitles.srt"
    
    # 查找英文字幕文件
    for file in os.listdir("output"):
        if file.endswith("_english.srt"):
            english_srt = os.path.join("output", file)
            break
    
    if not english_srt or not os.path.exists(english_srt):
        print("❌ 未找到英文字幕文件")
        return None
    
    if not os.path.exists(chinese_srt):
        print(f"❌ 中文字幕文件不存在: {chinese_srt}")
        return None
    
    # 创建定制水印
    watermark_path = create_custom_watermark("董卓主演脱口秀")
    if not watermark_path:
        return None
    
    output_path = "output/tiktok_version_2min37s.mp4"
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 英文字幕: {english_srt}")
    print(f"📝 中文字幕: {chinese_srt}")
    print(f"🏷️ 水印: 董卓主演脱口秀")
    print(f"⏱️ 视频长度: 2分37秒 (157秒)")
    
    try:
        # 使用ffmpeg命令: 截取视频 + 双语字幕 + 水印
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', watermark_path,
            '-filter_complex',
            f"[0:v]subtitles={english_srt}:force_style='FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=100,Alignment=2',"
            f"subtitles={chinese_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=10,Alignment=2'[v];"
            f"[v][1:v]overlay=W-w-10:10[final]",
            '-map', '[final]',
            '-map', '0:a',
            '-c:a', 'copy',
            '-t', '157',  # 截取到157秒 (2:37)
            '-y',
            output_path
        ]
        
        print("🔄 生成TikTok定制版本...")
        print("   ✂️ 截取到2分37秒")
        print("   🇺🇸 英文字幕: 白色，上方")
        print("   🇨🇳 中文字幕: 黄色，下方")
        print("   🏷️ 水印: 董卓主演脱口秀，右上角")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ TikTok版本生成成功!")
            print(f"   输出文件: {output_path}")
            
            # 显示文件信息
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024 / 1024
                print(f"   文件大小: {file_size:.2f} MB")
                print(f"   视频长度: 2分37秒")
                print(f"   水印内容: 董卓主演脱口秀")
            
            return output_path
        else:
            print(f"❌ FFmpeg处理失败:")
            print(f"   错误输出: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ FFmpeg未安装，请先安装FFmpeg")
        return None
    except Exception as e:
        print(f"❌ FFmpeg处理出错: {e}")
        return None

def create_tiktok_chinese_only():
    """创建TikTok版本的纯中文字幕视频 - 2:37结束"""
    
    # 找到原始视频
    video_files = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith('.mp4') and 'final' not in file and 'test' not in file and 'ffmpeg' not in file and 'dual' not in file and 'tiktok' not in file:
                video_files.append(os.path.join("output", file))
    
    if not video_files:
        print("❌ 未找到原始视频文件")
        return None
    
    video_path = video_files[0]
    chinese_srt = "chinese_subtitles.srt"
    
    if not os.path.exists(chinese_srt):
        print(f"❌ 中文字幕文件不存在: {chinese_srt}")
        return None
    
    # 创建定制水印
    watermark_path = create_custom_watermark("董卓主演脱口秀")
    if not watermark_path:
        return None
    
    output_path = "output/tiktok_chinese_only_2min37s.mp4"
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 中文字幕: {chinese_srt}")
    print(f"🏷️ 水印: 董卓主演脱口秀")
    print(f"⏱️ 视频长度: 2分37秒")
    
    try:
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', watermark_path,
            '-filter_complex',
            f"[0:v]subtitles={chinese_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1'[v];"
            f"[v][1:v]overlay=W-w-10:10[final]",
            '-map', '[final]',
            '-map', '0:a',
            '-c:a', 'copy',
            '-t', '157',  # 截取到157秒
            '-y',
            output_path
        ]
        
        print("🔄 生成TikTok中文版本...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ TikTok中文版本生成成功!")
            print(f"   输出文件: {output_path}")
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024 / 1024
                print(f"   文件大小: {file_size:.2f} MB")
            
            return output_path
        else:
            print(f"❌ FFmpeg处理失败: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 处理出错: {e}")
        return None

def main():
    """主函数"""
    print("🎬 TikTok定制版本生成器")
    print("=" * 50)
    print("🎯 定制要求:")
    print("   ✂️ 视频长度: 2分37秒")
    print("   🏷️ 水印: 董卓主演脱口秀")
    print("   📱 适用平台: TikTok")
    print()
    
    print("请选择版本:")
    print("1. 双语字幕版 (英文+中文)")
    print("2. 纯中文字幕版")
    print("3. 生成两个版本")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == '1':
        result = create_tiktok_dual_subtitles()
        if result:
            print(f"\n🎉 TikTok双语版本生成完成!")
    elif choice == '2':
        result = create_tiktok_chinese_only()
        if result:
            print(f"\n🎉 TikTok中文版本生成完成!")
    elif choice == '3':
        print("\n🔄 生成双语版本...")
        result1 = create_tiktok_dual_subtitles()
        print("\n🔄 生成中文版本...")
        result2 = create_tiktok_chinese_only()
        
        if result1 and result2:
            print(f"\n🎉 两个TikTok版本都生成完成!")
            print(f"   双语版: {result1}")
            print(f"   中文版: {result2}")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 