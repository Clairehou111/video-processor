#!/usr/bin/env python3
"""
改进版B站视频生成器 - 支持独立文件夹结构
"""

import os
import subprocess
import glob
from PIL import Image, ImageDraw, ImageFont

class ImprovedBilibiliGenerator:
    def __init__(self):
        self.base_output_dir = "output"
    
    def list_video_folders(self):
        """列出所有视频文件夹"""
        folders = []
        if os.path.exists(self.base_output_dir):
            for item in os.listdir(self.base_output_dir):
                item_path = os.path.join(self.base_output_dir, item)
                if os.path.isdir(item_path) and not item.startswith('.'):
                    folders.append(item_path)
        return sorted(folders)
    
    def select_video_folder(self):
        """让用户选择要处理的视频文件夹"""
        folders = self.list_video_folders()
        
        if not folders:
            print("❌ 未找到任何视频文件夹")
            print("💡 请先运行 improved_video_processor.py 下载和处理视频")
            return None
        
        print("📁 可用的视频文件夹:")
        for i, folder in enumerate(folders, 1):
            folder_name = os.path.basename(folder)
            print(f"{i}. {folder_name}")
        
        while True:
            try:
                choice = input(f"\n请选择文件夹 (1-{len(folders)}): ").strip()
                if choice:
                    index = int(choice) - 1
                    if 0 <= index < len(folders):
                        selected_folder = folders[index]
                        print(f"✅ 已选择: {os.path.basename(selected_folder)}")
                        return selected_folder
                print("❌ 无效选择，请重新输入")
            except ValueError:
                print("❌ 请输入有效数字")
    
    def find_video_files(self, folder_path):
        """在指定文件夹中查找视频文件"""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        video_files = []
        
        for ext in video_extensions:
            pattern = os.path.join(folder_path, f"*{ext}")
            video_files.extend(glob.glob(pattern))
        
        # 过滤掉已经处理过的B站版本
        original_videos = [v for v in video_files if 'bilibili' not in os.path.basename(v).lower()]
        
        return original_videos
    
    def find_subtitle_files(self, folder_path):
        """在指定文件夹中查找字幕文件"""
        english_srt = None
        chinese_srt = None
        
        for file in os.listdir(folder_path):
            if file.endswith('_english.srt'):
                english_srt = os.path.join(folder_path, file)
            elif file.endswith('_chinese.srt'):
                chinese_srt = os.path.join(folder_path, file)
        
        return english_srt, chinese_srt
    
    def create_bilibili_watermark(self, text="董卓主演脱口秀", output_path=None, is_hd=False):
        """创建B站水印"""
        if output_path is None:
            filename = "bilibili_hd_watermark.png" if is_hd else "bilibili_watermark.png"
            output_path = filename
        
        try:
            img = Image.new('RGBA', (200, 40), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
            except:
                font = ImageFont.load_default()
            
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except AttributeError:
                text_width, text_height = draw.textsize(text, font=font)
            
            x = (200 - text_width) // 2
            y = (40 - text_height) // 2
            
            if is_hd:
                draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 100))
                draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))
                img.save(output_path, optimize=True, quality=95)
            else:
                draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 80))
                draw.text((x, y), text, font=font, fill=(255, 255, 255, 150))
                img.save(output_path)
            
            print(f"✅ B站水印创建成功: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 水印创建失败: {e}")
            return None
    
    def generate_bilibili_version(self, video_folder, version_type="dual", quality="standard"):
        """生成B站版本"""
        print(f"🔄 开始生成B站{quality}版本...")
        
        # 查找视频文件
        video_files = self.find_video_files(video_folder)
        if not video_files:
            print("❌ 未找到原始视频文件")
            return None
        
        video_path = video_files[0]  # 使用第一个找到的视频
        print(f"📹 视频文件: {os.path.basename(video_path)}")
        
        # 查找字幕文件
        english_srt, chinese_srt = self.find_subtitle_files(video_folder)
        
        if version_type == "dual" and not english_srt:
            print("❌ 未找到英文字幕文件")
            return None
        
        if not chinese_srt:
            print("❌ 未找到中文字幕文件")
            return None
        
        # 创建水印
        is_hd = (quality == "hd")
        watermark_path = os.path.join(video_folder, f"bilibili{'_hd' if is_hd else ''}_watermark.png")
        if not self.create_bilibili_watermark("董卓主演脱口秀", watermark_path, is_hd):
            return None
        
        # 生成输出文件名
        quality_prefix = "hd_" if is_hd else ""
        version_suffix = "dual" if version_type == "dual" else "chinese"
        output_filename = f"bilibili_{quality_prefix}{version_suffix}_2min37s.mp4"
        output_path = os.path.join(video_folder, output_filename)
        
        print(f"📝 英文字幕: {os.path.basename(english_srt) if english_srt else '无'}")
        print(f"📝 中文字幕: {os.path.basename(chinese_srt)}")
        print(f"🏷️ 水印: 董卓主演脱口秀")
        print(f"⏱️ 时长: 2分37秒")
        
        try:
            # 构建ffmpeg命令
            cmd = ['ffmpeg', '-i', video_path, '-i', watermark_path]
            
            # 构建滤镜
            if version_type == "dual":
                filter_complex = (
                    f"[0:v]subtitles={english_srt}:force_style='FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=100,Alignment=2',"
                    f"subtitles={chinese_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1,MarginV=10,Alignment=2'[v];"
                    f"[v][1:v]overlay=W-w-5:5[final]"
                )
            else:
                filter_complex = (
                    f"[0:v]subtitles={chinese_srt}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,Outline=2,Shadow=1'[v];"
                    f"[v][1:v]overlay=W-w-5:5[final]"
                )
            
            cmd.extend(['-filter_complex', filter_complex])
            cmd.extend(['-map', '[final]', '-map', '0:a'])
            
            # 视频编码参数
            if is_hd:
                cmd.extend([
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '18',
                    '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart',
                    '-c:a', 'aac',
                    '-b:a', '128k'
                ])
            else:
                cmd.extend(['-c:a', 'copy'])
            
            cmd.extend(['-t', '157', '-y', output_path])  # 157秒 = 2分37秒
            
            print(f"🔄 生成B站{quality}版 ({'双语' if version_type == 'dual' else '中文'})...")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ B站版本生成成功!")
                print(f"   输出文件: {output_filename}")
                
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path) / 1024 / 1024
                    print(f"   文件大小: {file_size:.2f} MB")
                
                return output_path
            else:
                print(f"❌ FFmpeg处理失败:")
                print(f"   错误输出: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ 处理出错: {e}")
            return None
    
    def show_bilibili_guidelines(self):
        """显示B站上传指南"""
        print("\n📋 B站视频上传建议:")
        print("=" * 40)
        print("🎯 推荐规格:")
        print("   • 分辨率: 1080P")
        print("   • 文件大小: <100MB")
        print("   • 时长: 2-10分钟")
        print("   • 格式: MP4")
        print("\n🏷️ 水印规范:")
        print("   • 不遮挡主要内容")
        print("   • 字体适中不影响观看")
        print("   • 个人创作者标识允许")
        print("\n📝 推荐标题:")
        print("   • 脱口秀：[内容描述]")
        print("   • 董卓主演脱口秀：[具体话题]")
        print("   • [明星名字]爆料[事件]")
        print("\n🏷️ 推荐标签:")
        print("   • 脱口秀、搞笑、翻译、娱乐、海外")

def main():
    """主函数"""
    print("🎬 改进版B站视频生成器")
    print("=" * 40)
    print("支持功能:")
    print("✅ 独立文件夹结构")
    print("✅ 自动查找视频和字幕")
    print("✅ 标准版和高清版")
    print("✅ 双语和纯中文版本")
    print("=" * 40)
    
    generator = ImprovedBilibiliGenerator()
    
    # 选择视频文件夹
    video_folder = generator.select_video_folder()
    if not video_folder:
        return
    
    print(f"\n📁 处理文件夹: {os.path.basename(video_folder)}")
    
    # 选择生成版本
    print("\n🎬 选择生成版本:")
    print("1. 标准双语版 (推荐)")
    print("2. 标准中文版")
    print("3. 高清双语版 (文件较大)")
    print("4. 高清中文版")
    print("5. 生成全部版本")
    print("6. 查看B站上传指南")
    
    while True:
        choice = input("请选择 (1-6): ").strip()
        
        if choice == "1":
            result = generator.generate_bilibili_version(video_folder, "dual", "standard")
            break
        elif choice == "2":
            result = generator.generate_bilibili_version(video_folder, "chinese", "standard")
            break
        elif choice == "3":
            result = generator.generate_bilibili_version(video_folder, "dual", "hd")
            break
        elif choice == "4":
            result = generator.generate_bilibili_version(video_folder, "chinese", "hd")
            break
        elif choice == "5":
            print("🔄 生成全部版本...")
            results = []
            for version_type in ["dual", "chinese"]:
                for quality in ["standard", "hd"]:
                    result = generator.generate_bilibili_version(video_folder, version_type, quality)
                    if result:
                        results.append(result)
            
            if results:
                print(f"\n🎉 生成完成! 共生成 {len(results)} 个版本:")
                for result in results:
                    print(f"   ✅ {os.path.basename(result)}")
            break
        elif choice == "6":
            generator.show_bilibili_guidelines()
            continue
        else:
            print("❌ 无效选择，请重新输入")
    
    print(f"\n📁 所有文件保存在: {video_folder}")
    print("🎉 可以上传到B站了!")

if __name__ == "__main__":
    main() 