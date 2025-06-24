#!/usr/bin/env python3
"""
弹幕效果预览工具
提供多种方式预览弹幕效果
"""

import json
import os
import subprocess
import tempfile
from typing import List, Dict

class DanmakuPreviewTool:
    def __init__(self):
        self.temp_files = []
    
    def open_video_with_player(self, video_path: str):
        """使用系统默认播放器打开视频"""
        
        if not os.path.exists(video_path):
            print(f"❌ 视频文件不存在: {video_path}")
            return False
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(video_path)
            elif os.name == 'posix':  # macOS/Linux
                if 'darwin' in os.uname().sysname.lower():  # macOS
                    subprocess.run(['open', video_path])
                else:  # Linux
                    subprocess.run(['xdg-open', video_path])
            
            print(f"✅ 已使用系统播放器打开: {os.path.basename(video_path)}")
            return True
            
        except Exception as e:
            print(f"❌ 打开视频失败: {e}")
            return False
    
    def open_with_quicktime(self, video_path: str):
        """使用QuickTime Player打开（macOS）"""
        
        if not os.path.exists(video_path):
            print(f"❌ 视频文件不存在: {video_path}")
            return False
        
        try:
            subprocess.run(['open', '-a', 'QuickTime Player', video_path])
            print(f"✅ 已用QuickTime打开: {os.path.basename(video_path)}")
            return True
        except Exception as e:
            print(f"❌ QuickTime打开失败: {e}")
            return False
    
    def open_with_vlc(self, video_path: str):
        """使用VLC播放器打开"""
        
        if not os.path.exists(video_path):
            print(f"❌ 视频文件不存在: {video_path}")
            return False
        
        vlc_paths = [
            '/Applications/VLC.app/Contents/MacOS/VLC',  # macOS
            '/usr/bin/vlc',  # Linux
            'vlc',  # 系统PATH中
        ]
        
        for vlc_path in vlc_paths:
            try:
                if os.path.exists(vlc_path) or vlc_path == 'vlc':
                    subprocess.run([vlc_path, video_path])
                    print(f"✅ 已用VLC打开: {os.path.basename(video_path)}")
                    return True
            except:
                continue
        
        print("❌ 未找到VLC播放器")
        return False
    
    def create_preview_gif(self, video_path: str, output_path: str = None, 
                          start_time: int = 10, duration: int = 5) -> str:
        """创建预览GIF"""
        
        if output_path is None:
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = f"output/{video_name}_preview.gif"
        
        # FFmpeg命令创建GIF
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', str(start_time),  # 开始时间
            '-t', str(duration),     # 持续时间
            '-vf', 'fps=10,scale=640:-1:flags=lanczos',  # 降低帧率和分辨率
            '-y',
            output_path
        ]
        
        try:
            print(f"🎬 正在生成预览GIF...")
            print(f"⏰ 截取时间: {start_time}s-{start_time+duration}s")
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print(f"✅ GIF预览已生成: {output_path}")
            
            # 自动打开GIF
            self.open_file(output_path)
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"❌ GIF生成失败: {e}")
            return None
        except FileNotFoundError:
            print("❌ 未找到FFmpeg，请确保已安装")
            return None
    
    def create_danmaku_timeline_preview(self, danmaku_file: str) -> str:
        """创建弹幕时间轴预览"""
        
        with open(danmaku_file, 'r', encoding='utf-8') as f:
            danmaku_data = json.load(f)
        
        preview_content = []
        preview_content.append("🎬 弹幕时间轴预览")
        preview_content.append("=" * 50)
        preview_content.append("")
        
        # 按时间排序
        danmaku_list = sorted(danmaku_data["danmaku_list"], key=lambda x: x["time"])
        
        for i, danmaku in enumerate(danmaku_list, 1):
            time_ms = danmaku["time"]
            time_s = time_ms / 1000.0
            minutes = int(time_s // 60)
            seconds = int(time_s % 60)
            
            # 弹幕类型
            mode_map = {1: "滚动", 4: "底部", 5: "顶部"}
            mode_name = mode_map.get(danmaku["mode"], "其他")
            
            # 颜色信息
            color = int(danmaku["color"])
            color_name = "白色" if color == 16777215 else "彩色"
            
            preview_content.append(
                f"{i:2d}. [{minutes:02d}:{seconds:02d}] "
                f"{danmaku['text']} "
                f"({mode_name}, {color_name}, {danmaku['fontsize']}px)"
            )
        
        preview_content.append("")
        preview_content.append(f"📊 总计: {len(danmaku_list)} 条弹幕")
        preview_content.append(f"⏱️ 持续时间: {time_s:.1f}秒")
        
        # 保存预览文件
        preview_file = danmaku_file.replace('.json', '_timeline_preview.txt')
        with open(preview_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(preview_content))
        
        print(f"✅ 时间轴预览已生成: {preview_file}")
        
        # 显示预览内容
        print("\n" + '\n'.join(preview_content))
        
        return preview_file
    
    def create_frame_snapshots(self, video_path: str, danmaku_file: str, 
                             output_dir: str = "output/snapshots") -> List[str]:
        """在关键弹幕时间点创建截图"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        with open(danmaku_file, 'r', encoding='utf-8') as f:
            danmaku_data = json.load(f)
        
        snapshots = []
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        
        for i, danmaku in enumerate(danmaku_data["danmaku_list"][:3]):  # 只截取前3个
            time_s = danmaku["time"] / 1000.0
            output_image = os.path.join(output_dir, f"{video_name}_snapshot_{i+1}.png")
            
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', video_path,
                '-ss', str(time_s),
                '-vframes', '1',
                '-y',
                output_image
            ]
            
            try:
                subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
                snapshots.append(output_image)
                print(f"📸 截图 {i+1}: {time_s:.1f}s -> {os.path.basename(output_image)}")
            except:
                print(f"❌ 截图 {i+1} 失败")
        
        if snapshots:
            print(f"✅ 已生成 {len(snapshots)} 张关键时刻截图")
            # 打开截图文件夹
            self.open_file(output_dir)
        
        return snapshots
    
    def open_file(self, file_path: str):
        """使用系统默认程序打开文件"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif 'darwin' in os.uname().sysname.lower():  # macOS
                subprocess.run(['open', file_path])
            else:  # Linux
                subprocess.run(['xdg-open', file_path])
        except:
            pass
    
    def show_preview_menu(self):
        """显示预览选项菜单"""
        
        print("\n🎬 弹幕效果预览选项")
        print("=" * 40)
        print("1. 📱 系统默认播放器预览")
        print("2. 🎞️ QuickTime Player预览")
        print("3. 🦄 VLC播放器预览") 
        print("4. 🖼️ 生成预览GIF")
        print("5. 📋 弹幕时间轴预览")
        print("6. 📸 关键时刻截图")
        print("7. 🚀 一键全部预览")
        print("0. 退出")
        
        return input("\n请选择预览方式 (0-7): ").strip()


def main():
    """主函数"""
    preview_tool = DanmakuPreviewTool()
    
    # 可用的视频文件
    video_files = {
        "1": "output/trump_jan6_with_danmaku.mp4",
        "2": "output/trump_jan6_enhanced_with_danmaku.mp4"
    }
    
    danmaku_file = "output/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena_jan6_special_danmaku.json"
    
    print("🎯 弹幕效果预览工具")
    print("=" * 30)
    
    # 选择视频文件
    print("\n📹 可用视频:")
    print("1. 基础版 (trump_jan6_with_danmaku.mp4)")
    print("2. 增强版 (trump_jan6_enhanced_with_danmaku.mp4)")
    
    video_choice = input("\n选择视频 (1-2): ").strip()
    if video_choice not in video_files:
        print("❌ 无效选择，使用增强版")
        video_choice = "2"
    
    selected_video = video_files[video_choice]
    
    if not os.path.exists(selected_video):
        print(f"❌ 视频文件不存在: {selected_video}")
        return
    
    print(f"\n✅ 已选择: {os.path.basename(selected_video)}")
    
    while True:
        choice = preview_tool.show_preview_menu()
        
        if choice == "0":
            print("👋 再见！")
            break
        elif choice == "1":
            preview_tool.open_video_with_player(selected_video)
        elif choice == "2":
            preview_tool.open_with_quicktime(selected_video)
        elif choice == "3":
            preview_tool.open_with_vlc(selected_video)
        elif choice == "4":
            start_time = input("开始时间(秒，默认10): ").strip() or "10"
            duration = input("持续时间(秒，默认5): ").strip() or "5"
            preview_tool.create_preview_gif(selected_video, 
                                          start_time=int(start_time), 
                                          duration=int(duration))
        elif choice == "5":
            preview_tool.create_danmaku_timeline_preview(danmaku_file)
        elif choice == "6":
            preview_tool.create_frame_snapshots(selected_video, danmaku_file)
        elif choice == "7":
            print("🚀 执行全部预览...")
            preview_tool.open_video_with_player(selected_video)
            preview_tool.create_preview_gif(selected_video)
            preview_tool.create_danmaku_timeline_preview(danmaku_file)
            preview_tool.create_frame_snapshots(selected_video, danmaku_file)
            print("✅ 全部预览完成！")
        else:
            print("❌ 无效选择，请重试")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    main() 