#!/usr/bin/env python3
"""
创建B站高清版本 - 优化视频质量，提高清晰度
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_bilibili_hd_watermark(text="董卓主演脱口秀", output_path="output/bilibili_hd_watermark.png"):
    """创建高清版本的B站水印"""
    try:
        # 创建更清晰的水印图片
        img = Image.new('RGBA', (200, 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            # 使用更清晰的字体渲染
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
        except:
            font = ImageFont.load_default()
        
        # 计算文字尺寸
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            text_width, text_height = draw.textsize(text, font=font)
        
        x = (200 - text_width) // 2
        y = (40 - text_height) // 2
        
        # 使用更清晰的渲染效果
        draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 100))   # 清晰阴影
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))  # 清晰主文字
        
        img.save(output_path, optimize=True, quality=95)  # 高质量保存
        print(f"✅ B站高清水印创建成功: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 水印创建失败: {e}")
        return None

def create_bilibili_hd_dual_subtitles():
    """创建B站高清版本的双语字幕视频"""
    
    # 找到原始视频
    video_files = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith('.mp4') and 'final' not in file and 'test' not in file and 'ffmpeg' not in file and 'dual' not in file and 'tiktok' not in file and 'bilibili' not in file:
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
    
    # 创建高清水印
    watermark_path = create_bilibili_hd_watermark("董卓主演脱口秀")
    if not watermark_path:
        return None
    
    output_path = "output/bilibili_hd_dual_2min37s.mp4"
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 英文字幕: {english_srt}")
    print(f"📝 中文字幕: {chinese_srt}")
    print(f"🏷️ 水印: 董卓主演脱口秀 (高清版)")
    print(f"⏱️ 视频长度: 2分37秒")
    
    try:
        # 使用优化的ffmpeg参数提高清晰度
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', watermark_path,
            '-filter_complex',
            f"[0:v]subtitles={english_srt}:force_style='FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=100,Alignment=2',"
            f"subtitles={chinese_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=10,Alignment=2'[v];"
            f"[v][1:v]overlay=W-w-5:5[final]",
            '-map', '[final]',
            '-map', '0:a',
            '-c:v', 'libx264',
            '-preset', 'medium',      # 平衡编码速度和质量
            '-crf', '18',             # 高质量（较低的CRF值）
            '-pix_fmt', 'yuv420p',    # 兼容性格式
            '-movflags', '+faststart', # 优化流式播放
            '-c:a', 'aac',
            '-b:a', '128k',           # 音频比特率
            '-t', '157',
            '-y',
            output_path
        ]
        
        print("🔄 生成B站高清版...")
        print("   📱 平台: 哔哩哔哩")
        print("   🎬 质量: 高清优化 (CRF=18)")
        print("   ✂️ 时长: 2分37秒")
        print("   🇺🇸 英文字幕: 白色，上方")
        print("   🇨🇳 中文字幕: 黄色，下方")
        print("   🏷️ 水印: 高清小字体，右上角")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ B站高清版生成成功!")
            print(f"   输出文件: {output_path}")
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024 / 1024
                print(f"   文件大小: {file_size:.2f} MB")
                print(f"   质量提升: ✅ 高清渲染")
            
            return output_path
        else:
            print(f"❌ FFmpeg处理失败:")
            print(f"   错误输出: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 处理出错: {e}")
        return None

def create_bilibili_hd_chinese_only():
    """创建B站高清版本的纯中文字幕视频"""
    
    # 找到原始视频
    video_files = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith('.mp4') and 'final' not in file and 'test' not in file and 'ffmpeg' not in file and 'dual' not in file and 'tiktok' not in file and 'bilibili' not in file:
                video_files.append(os.path.join("output", file))
    
    if not video_files:
        print("❌ 未找到原始视频文件")
        return None
    
    video_path = video_files[0]
    chinese_srt = "chinese_subtitles.srt"
    
    if not os.path.exists(chinese_srt):
        print(f"❌ 中文字幕文件不存在: {chinese_srt}")
        return None
    
    # 创建高清水印
    watermark_path = create_bilibili_hd_watermark("董卓主演脱口秀")
    if not watermark_path:
        return None
    
    output_path = "output/bilibili_hd_chinese_2min37s.mp4"
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 中文字幕: {chinese_srt}")
    print(f"🏷️ 水印: 董卓主演脱口秀 (高清)")
    
    try:
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', watermark_path,
            '-filter_complex',
            f"[0:v]subtitles={chinese_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1'[v];"
            f"[v][1:v]overlay=W-w-5:5[final]",
            '-map', '[final]',
            '-map', '0:a',
            '-c:v', 'libx264',
            '-preset', 'medium',      # 平衡编码速度和质量
            '-crf', '18',             # 高质量
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-t', '157',
            '-y',
            output_path
        ]
        
        print("🔄 生成B站高清中文版...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ B站高清中文版生成成功!")
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

def show_quality_comparison():
    """显示质量对比信息"""
    print("\n📊 高清版本优化说明:")
    print("=" * 40)
    print("🎬 视频质量提升:")
    print("   • CRF值: 23 → 18 (更低=更清晰)")
    print("   • 编码预设: fast → medium (更好质量)")
    print("   • 像素格式: 优化为yuv420p")
    print("   • 流式优化: +faststart参数")
    print()
    print("🎨 字幕渲染优化:")
    print("   • 更清晰的字体渲染")
    print("   • 优化的描边效果")
    print("   • 更好的抗锯齿")
    print()
    print("🏷️ 水印优化:")
    print("   • 高质量PNG保存")
    print("   • 更清晰的边缘处理")
    print("   • 优化的透明度混合")
    print()
    print("📏 预期效果:")
    print("   • 文字更清晰锐利")
    print("   • 视频细节更丰富")
    print("   • 文件稍大但质量更好")

def main():
    """主函数"""
    print("🎬 B站高清版生成器")
    print("=" * 50)
    print("🎯 高清优化特点:")
    print("   ✨ 视频质量: 高清渲染 (CRF=18)")
    print("   🏷️ 水印: 董卓主演脱口秀 (高清小字体)")
    print("   📱 适配平台: 哔哩哔哩")
    print("   🎨 优化: 比标准版更清晰")
    print()
    
    print("选择生成版本:")
    print("1. 高清双语字幕版")
    print("2. 高清纯中文字幕版")
    print("3. 生成两个高清版本")
    print("4. 查看质量优化说明")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == '1':
        result = create_bilibili_hd_dual_subtitles()
        if result:
            print(f"\n🎉 B站高清双语版本生成完成!")
            show_quality_comparison()
    elif choice == '2':
        result = create_bilibili_hd_chinese_only()
        if result:
            print(f"\n🎉 B站高清中文版本生成完成!")
            show_quality_comparison()
    elif choice == '3':
        print("\n🔄 生成高清双语版本...")
        result1 = create_bilibili_hd_dual_subtitles()
        print("\n🔄 生成高清中文版本...")
        result2 = create_bilibili_hd_chinese_only()
        
        if result1 and result2:
            print(f"\n🎉 两个B站高清版本都生成完成!")
            print(f"   高清双语版: {result1}")
            print(f"   高清中文版: {result2}")
            show_quality_comparison()
    elif choice == '4':
        show_quality_comparison()
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 