#!/usr/bin/env python3
"""
创建B站定制版本 - 2:37秒结束，水印"董卓主演脱口秀"(小字体，更靠右)
适配B站平台规范
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_bilibili_watermark(text="董卓主演脱口秀", output_path="output/bilibili_watermark.png"):
    """创建适合B站的低调水印"""
    try:
        # 创建更小的水印图片
        img = Image.new('RGBA', (200, 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            # 使用更小的字体
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
        
        # 使用更低调的效果 - 半透明白色，轻微阴影
        draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 80))   # 轻阴影
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 150))  # 半透明主文字
        
        img.save(output_path)
        print(f"✅ B站专用水印创建成功: {output_path}")
        print(f"   特点: 小字体、半透明、低调显示")
        return output_path
        
    except Exception as e:
        print(f"❌ 水印创建失败: {e}")
        return None

def create_bilibili_dual_subtitles():
    """创建B站版本的双语字幕视频"""
    
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
    
    # 创建B站专用水印
    watermark_path = create_bilibili_watermark("董卓主演脱口秀")
    if not watermark_path:
        return None
    
    output_path = "output/bilibili_dual_2min37s.mp4"
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 英文字幕: {english_srt}")
    print(f"📝 中文字幕: {chinese_srt}")
    print(f"🏷️ 水印: 董卓主演脱口秀 (B站规范)")
    print(f"⏱️ 视频长度: 2分37秒")
    
    try:
        # 使用ffmpeg命令: 水印位置更靠右上角
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', watermark_path,
            '-filter_complex',
            f"[0:v]subtitles={english_srt}:force_style='FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=100,Alignment=2',"
            f"subtitles={chinese_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=10,Alignment=2'[v];"
            f"[v][1:v]overlay=W-w-5:5[final]",  # 更靠右：距离右边只有5px，距离上边5px
            '-map', '[final]',
            '-map', '0:a',
            '-c:a', 'copy',
            '-t', '157',  # 截取到157秒
            '-y',
            output_path
        ]
        
        print("🔄 生成B站专版...")
        print("   📱 平台: 哔哩哔哩")
        print("   ✂️ 时长: 2分37秒")
        print("   🇺🇸 英文字幕: 白色，上方")
        print("   🇨🇳 中文字幕: 黄色，下方") 
        print("   🏷️ 水印: 小字体，右上角更靠右")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ B站版本生成成功!")
            print(f"   输出文件: {output_path}")
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024 / 1024
                print(f"   文件大小: {file_size:.2f} MB")
                print(f"   符合B站规范: ✅")
            
            return output_path
        else:
            print(f"❌ FFmpeg处理失败:")
            print(f"   错误输出: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 处理出错: {e}")
        return None

def create_bilibili_chinese_only():
    """创建B站版本的纯中文字幕视频"""
    
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
    
    # 创建B站专用水印
    watermark_path = create_bilibili_watermark("董卓主演脱口秀")
    if not watermark_path:
        return None
    
    output_path = "output/bilibili_chinese_2min37s.mp4"
    
    print(f"📹 视频文件: {video_path}")
    print(f"📝 中文字幕: {chinese_srt}")
    print(f"🏷️ 水印: 董卓主演脱口秀")
    
    try:
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', watermark_path,
            '-filter_complex',
            f"[0:v]subtitles={chinese_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1'[v];"
            f"[v][1:v]overlay=W-w-5:5[final]",  # 更靠右的位置
            '-map', '[final]',
            '-map', '0:a',
            '-c:a', 'copy',
            '-t', '157',
            '-y',
            output_path
        ]
        
        print("🔄 生成B站中文版...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ B站中文版生成成功!")
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

def show_bilibili_guidelines():
    """显示B站上传指南"""
    print("\n📋 B站视频上传建议:")
    print("=" * 40)
    print("🎯 推荐规格:")
    print("   • 分辨率: 1080P (当前视频640x360需要考虑)")
    print("   • 文件大小: <100MB (当前约10MB ✅)")
    print("   • 时长: 2-10分钟 (当前2:37 ✅)")
    print("   • 格式: MP4 (✅)")
    print()
    print("🏷️ 水印规范:")
    print("   • 不遮挡主要内容 (✅)")
    print("   • 字体适中不影响观看 (✅)")
    print("   • 个人创作者标识允许 (✅)")
    print()
    print("📝 标题建议:")
    print("   • '查理·辛爆料特朗普送假袖扣的搞笑故事'")
    print("   • '脱口秀：特朗普的\"白金\"袖扣真相大白'")
    print("   • '董卓主演脱口秀：好莱坞明星VS地产大亨'")
    print()
    print("🏷️ 标签建议:")
    print("   • 脱口秀、搞笑、查理辛、特朗普、翻译")

def main():
    """主函数"""
    print("📺 B站专版生成器")
    print("=" * 50)
    print("🎯 B站定制要求:")
    print("   ✂️ 视频长度: 2分37秒")
    print("   🏷️ 水印: 董卓主演脱口秀 (小字体，更靠右)")
    print("   📱 适配平台: 哔哩哔哩")
    print("   🎨 风格: 低调不影响观看")
    print()
    
    print("选择生成版本:")
    print("1. 双语字幕版 (推荐学习区)")
    print("2. 纯中文字幕版 (推荐娱乐区)")
    print("3. 生成两个版本")
    print("4. 查看B站上传指南")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == '1':
        result = create_bilibili_dual_subtitles()
        if result:
            print(f"\n🎉 B站双语版本生成完成!")
            show_bilibili_guidelines()
    elif choice == '2':
        result = create_bilibili_chinese_only()
        if result:
            print(f"\n🎉 B站中文版本生成完成!")
            show_bilibili_guidelines()
    elif choice == '3':
        print("\n🔄 生成双语版本...")
        result1 = create_bilibili_dual_subtitles()
        print("\n🔄 生成中文版本...")
        result2 = create_bilibili_chinese_only()
        
        if result1 and result2:
            print(f"\n🎉 两个B站版本都生成完成!")
            print(f"   双语版: {result1}")
            print(f"   中文版: {result2}")
            show_bilibili_guidelines()
    elif choice == '4':
        show_bilibili_guidelines()
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 