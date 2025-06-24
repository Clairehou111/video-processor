#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整视频处理自动化系统
支持：下载、切片、字幕提取、翻译、烧制、B站优化
"""

import os
import subprocess
import json
import re
from pathlib import Path
import yt_dlp
import whisper

class CompleteVideoAutomation:
    def __init__(self):
        self.base_output_dir = "output"
        self.current_project_dir = None
        self.whisper_model = None
        
    def load_whisper_model(self):
        """加载Whisper模型"""
        if not self.whisper_model:
            print("🔄 加载Whisper模型...")
            self.whisper_model = whisper.load_model("base")
            print("✅ Whisper模型加载完成")
    
    def create_project_directory(self, video_title):
        """为视频创建专属项目目录"""
        import re
        import datetime
        
        # 清理视频标题，创建安全的目录名
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', video_title)
        safe_title = safe_title.replace(' ', '_')[:50]  # 限制长度
        
        # 添加时间戳避免重复
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        project_name = f"{safe_title}_{timestamp}"
        self.current_project_dir = os.path.join(self.base_output_dir, project_name)
        
        # 创建目录结构
        os.makedirs(self.current_project_dir, exist_ok=True)
        os.makedirs(os.path.join(self.current_project_dir, "subtitles"), exist_ok=True)
        os.makedirs(os.path.join(self.current_project_dir, "final"), exist_ok=True)
        
        print(f"📁 项目目录已创建: {self.current_project_dir}")
        return self.current_project_dir

    def find_latest_project(self):
        """查找最新的项目目录"""
        if not os.path.exists(self.base_output_dir):
            return None
            
        projects = []
        for item in os.listdir(self.base_output_dir):
            project_path = os.path.join(self.base_output_dir, item)
            if os.path.isdir(project_path):
                state_file = os.path.join(project_path, "automation_state.json")
                if os.path.exists(state_file):
                    # 获取目录修改时间
                    mtime = os.path.getmtime(state_file)
                    projects.append((mtime, project_path, state_file))
        
        if projects:
            # 按时间排序，返回最新的项目
            projects.sort(key=lambda x: x[0], reverse=True)
            latest_project = projects[0]
            self.current_project_dir = latest_project[1]
            print(f"📁 找到最新项目: {self.current_project_dir}")
            return latest_project[2]
        
        return None

    def list_projects(self):
        """列出所有项目"""
        if not os.path.exists(self.base_output_dir):
            print("📁 输出目录不存在")
            return []
            
        projects = []
        for item in os.listdir(self.base_output_dir):
            project_path = os.path.join(self.base_output_dir, item)
            if os.path.isdir(project_path):
                state_file = os.path.join(project_path, "automation_state.json")
                if os.path.exists(state_file):
                    try:
                        with open(state_file, 'r', encoding='utf-8') as f:
                            state = json.load(f)
                        projects.append({
                            "path": project_path,
                            "title": state.get("video_title", "Unknown"),
                            "status": state.get("status", "unknown"),
                            "timestamp": os.path.getmtime(state_file)
                        })
                    except:
                        continue
        
        projects.sort(key=lambda x: x["timestamp"], reverse=True)
        return projects

    def download_video(self, url, start_time=None, end_time=None):
        """下载视频（支持完整或切片）"""
        print(f"📥 开始下载视频...")
        if start_time and end_time:
            print(f"   切片时间: {start_time} - {end_time}")
        
        # 先获取视频信息来创建项目目录
        temp_ydl_opts = {'quiet': True}
        try:
            with yt_dlp.YoutubeDL(temp_ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'video')
        except Exception as e:
            print(f"⚠️ 无法获取视频信息，使用默认名称: {e}")
            video_title = "unknown_video"
        
        # 创建项目目录
        project_dir = self.create_project_directory(video_title)
        
        # 高质量下载配置
        ydl_opts = {
            'format': 'bestvideo[height>=1080]+bestaudio/best[height>=1080]',
            'outtmpl': f'{project_dir}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
        }
        
        # 如果是切片下载
        if start_time and end_time:
            ydl_opts['external_downloader'] = 'ffmpeg'
            ydl_opts['external_downloader_args'] = [
                '-ss', start_time,
                '-to', end_time
            ]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'video')
                video_path = f"{project_dir}/{title}.mp4"
                
                # 处理文件名
                if os.path.exists(video_path):
                    print(f"✅ 视频下载成功: {video_path}")
                    return video_path, title
                else:
                    # 查找实际下载的文件
                    for file in os.listdir(project_dir):
                        if file.endswith('.mp4'):
                            actual_path = f"{project_dir}/{file}"
                            print(f"✅ 视频下载成功: {actual_path}")
                            return actual_path, title
                    
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return None, None
    
    def extract_english_subtitles(self, video_path):
        """提取英文字幕"""
        print("🔄 提取英文字幕...")
        self.load_whisper_model()
        
        result = self.whisper_model.transcribe(video_path)
        segments = []
        
        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            })
        
        # 保存英文SRT到subtitles子目录
        video_name = Path(video_path).stem
        english_srt = f"{self.current_project_dir}/subtitles/{video_name}_english.srt"
        
        with open(english_srt, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                start_time = self.seconds_to_srt_time(segment["start"])
                end_time = self.seconds_to_srt_time(segment["end"])
                f.write(f"{i}\n{start_time} --> {end_time}\n{segment['text']}\n\n")
        
        print(f"✅ 英文字幕提取完成: {english_srt}")
        print(f"📊 共 {len(segments)} 个片段")
        return english_srt, segments
    
    def create_translation_prompt(self, segments):
        """创建翻译提示词"""
        prompt_file = f"{self.current_project_dir}/translation_prompt.txt"
        translation_file = f"{self.current_project_dir}/subtitles/chinese_translation.srt"
        
        prompt_content = f"""# 政治脱口秀翻译指南

## 翻译要求
1. 保持政治幽默的精髓和讽刺效果
2. 适应中文表达习惯，但保留原意
3. 专有名词准确翻译（人名、地名、机构名）
4. 保持时间节奏，适合字幕显示

## 待翻译内容 ({len(segments)} 个片段)
"""
        
        for i, segment in enumerate(segments, 1):
            prompt_content += f"\n{i}. {segment['text']}"
        
        prompt_content += f"""

## 翻译格式要求
请将翻译结果保存到: {translation_file}
格式如下:

1
00:00:01,000 --> 00:00:03,500
中文翻译内容1

2
00:00:03,500 --> 00:00:05,800
中文翻译内容2

...

## 翻译完成后
请运行: python complete_video_automation.py --finalize
"""
        
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt_content)
        
        print(f"✅ 翻译提示词已生成: {prompt_file}")
        print(f"📝 请将中文翻译保存到: {translation_file}")
        return prompt_file, translation_file
    
    def create_bilingual_video(self, video_path, chinese_srt):
        """创建双语视频"""
        print("🎬 开始创建双语视频...")
        
        video_name = Path(video_path).stem
        output_video = f"{self.current_project_dir}/final/{video_name}_bilingual_final.mp4"
        english_srt = f"{self.current_project_dir}/subtitles/{video_name}_english.srt"
        
        # 使用优化的FFmpeg命令
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vf', (
                f"drawbox=x=10:y=10:w=320:h=100:color=black@0.8:t=fill,"
                f"drawbox=x=10:y=h-120:w=280:h=80:color=black@0.8:t=fill,"
                f"drawtext=text='董卓主演脱口秀':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=32:fontcolor=white:x=w-tw-30:y=30:alpha=0.9,"
                f"subtitles={chinese_srt}:force_style='FontSize=22,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=70,Alignment=2',"
                f"subtitles={english_srt}:force_style='FontSize=18,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=25,Alignment=2'"
            ),
            '-c:a', 'copy',
            output_video
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 双语视频创建成功: {output_video}")
            return output_video
        except subprocess.CalledProcessError as e:
            print(f"❌ 视频创建失败: {e}")
            return None
    
    def generate_bilibili_metadata(self, video_title):
        """生成B站上传元数据"""
        metadata = {
            "标题": f"【中英字幕】{video_title} | 政治脱口秀",
            "标签": ["政治", "脱口秀", "中英字幕", "每日秀", "政治讽刺", "美国政治"],
            "分类": "知识·科普·社科",
            "简介": f"""🎭 {video_title}

📺 来源：The Daily Show等政治脱口秀节目
🎯 内容：犀利政治评论，幽默时事解读
📝 字幕：中英双语，准确翻译
🔥 更多精彩政治脱口秀，关注UP主！

#政治脱口秀 #中英字幕 #时事评论
董卓主演脱口秀 出品""",
            "封面": "建议使用节目关键镜头作为封面",
            "投稿说明": "请确保内容符合平台规范，避免敏感政治内容"
        }
        
        metadata_file = f"{self.current_project_dir}/bilibili_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"✅ B站元数据已生成: {metadata_file}")
        return metadata
    
    def seconds_to_srt_time(self, seconds):
        """转换秒数为SRT时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def process_video(self, url, start_time=None, end_time=None):
        """完整视频处理流程"""
        print("🎯 完整视频处理自动化开始")
        print("="*50)
        
        # 步骤1: 下载视频
        print("\n📥 步骤1: 下载视频")
        video_path, video_title = self.download_video(url, start_time, end_time)
        if not video_path:
            return False
        
        # 步骤2: 提取英文字幕
        print("\n📝 步骤2: 提取英文字幕")
        english_srt, segments = self.extract_english_subtitles(video_path)
        
        # 步骤3: 生成翻译提示词
        print("\n📖 步骤3: 生成翻译提示词")
        prompt_file, translation_file = self.create_translation_prompt(segments)
        
        print("\n⏳ 请完成以下步骤:")
        print(f"1. 查看翻译提示词: {prompt_file}")
        print(f"2. 完成中文翻译并保存到: {translation_file}")
        print("3. 运行完成命令: python complete_video_automation.py --finalize")
        
        # 保存状态
        state = {
            "video_path": video_path,
            "video_title": video_title,
            "english_srt": english_srt,
            "translation_file": translation_file,
            "project_dir": self.current_project_dir,
            "status": "waiting_translation"
        }
        
        with open(f"{self.current_project_dir}/automation_state.json", 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        return True
    
    def finalize_video(self, project_dir=None):
        """完成视频处理"""
        print("🎬 完成视频处理...")
        
        # 如果指定了项目目录，直接使用
        if project_dir:
            state_file = f"{project_dir}/automation_state.json"
            self.current_project_dir = project_dir
        else:
            # 尝试查找最新的项目
            state_file = self.find_latest_project()
            if not state_file:
                print("❌ 未找到处理状态文件")
                return False
        
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        video_path = state["video_path"]
        video_title = state["video_title"]
        translation_file = state["translation_file"]
        
        # 更新项目目录（兼容旧格式）
        if "project_dir" in state:
            self.current_project_dir = state["project_dir"]
        
        # 检查翻译文件
        if not os.path.exists(translation_file):
            print(f"❌ 未找到翻译文件: {translation_file}")
            return False
        
        # 步骤4: 创建双语视频
        print("\n🎭 步骤4: 创建双语视频")
        bilingual_video = self.create_bilingual_video(video_path, translation_file)
        if not bilingual_video:
            return False
        
        # 步骤5: 生成B站元数据
        print("\n📊 步骤5: 生成B站上传信息")
        metadata = self.generate_bilibili_metadata(video_title)
        
        print("\n🎉 视频处理完成!")
        print("="*50)
        print("📁 项目目录结构:")
        self.show_project_structure()
        
        file_size = os.path.getsize(bilingual_video) / (1024*1024)
        print(f"\n📊 视频大小: {file_size:.1f}MB")
        
        print("\n🚀 B站上传建议:")
        print(f"标题: {metadata['标题']}")
        print(f"标签: {', '.join(metadata['标签'])}")
        print(f"分类: {metadata['分类']}")
        
        return True

    def show_project_structure(self):
        """显示项目目录结构"""
        if not self.current_project_dir:
            return
            
        print(f"📁 {os.path.basename(self.current_project_dir)}/")
        
        # 显示主要文件
        for root, dirs, files in os.walk(self.current_project_dir):
            level = root.replace(self.current_project_dir, '').count(os.sep)
            indent = '   ' * level
            subdir = os.path.basename(root)
            if subdir:
                print(f"{indent}📂 {subdir}/")
            
            sub_indent = '   ' * (level + 1)
            for file in files:
                if file.endswith(('.mp4', '.srt', '.json', '.txt')):
                    emoji = self.get_file_emoji(file)
                    print(f"{sub_indent}{emoji} {file}")

    def get_file_emoji(self, filename):
        """根据文件类型返回对应emoji"""
        if filename.endswith('.mp4'):
            return '🎬'
        elif filename.endswith('.srt'):
            return '📝'
        elif filename.endswith('.json'):
            return '⚙️'
        elif filename.endswith('.txt'):
            return '📖'
        else:
            return '📄'

def main():
    import sys
    
    automation = CompleteVideoAutomation()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--finalize":
            # 完成处理
            automation.finalize_video()
        elif sys.argv[1] == "--list":
            # 列出所有项目
            projects = automation.list_projects()
            if projects:
                print("📁 所有项目:")
                print("="*50)
                for i, project in enumerate(projects, 1):
                    status_emoji = "✅" if project["status"] == "completed" else "⏳"
                    print(f"{i}. {status_emoji} {project['title']}")
                    print(f"   📂 {os.path.basename(project['path'])}")
                    print(f"   📊 状态: {project['status']}")
                    print()
            else:
                print("📁 暂无项目")
        elif sys.argv[1] == "--continue":
            # 继续指定项目
            if len(sys.argv) > 2:
                project_dir = sys.argv[2]
                automation.finalize_video(project_dir)
            else:
                print("❌ 请指定项目目录")
        else:
            print("❌ 未知参数")
            print("使用方式:")
            print("  python complete_video_automation.py           # 开始新项目")
            print("  python complete_video_automation.py --finalize # 完成最新项目")
            print("  python complete_video_automation.py --list     # 列出所有项目")
            print("  python complete_video_automation.py --continue <项目目录> # 继续指定项目")
    else:
        # 交互式开始
        print("🎯 完整视频处理自动化")
        print("="*50)
        
        # 检查是否有未完成的项目
        projects = automation.list_projects()
        unfinished = [p for p in projects if p["status"] == "waiting_translation"]
        
        if unfinished:
            print(f"⚠️  发现 {len(unfinished)} 个未完成的项目:")
            for project in unfinished[:3]:  # 只显示最近3个
                print(f"   📂 {project['title']}")
            
            choice = input("\n是否继续未完成的项目? (y/N): ").strip().lower()
            if choice == 'y':
                # 选择要继续的项目
                if len(unfinished) == 1:
                    automation.finalize_video(unfinished[0]["path"])
                    return
                else:
                    print("\n选择要继续的项目:")
                    for i, project in enumerate(unfinished, 1):
                        print(f"{i}. {project['title']}")
                    
                    try:
                        idx = int(input("请输入项目编号: ")) - 1
                        if 0 <= idx < len(unfinished):
                            automation.finalize_video(unfinished[idx]["path"])
                            return
                        else:
                            print("❌ 无效的项目编号")
                            return
                    except ValueError:
                        print("❌ 请输入有效数字")
                        return
        
        # 开始新项目
        print("\n🆕 开始新项目")
        url = input("📥 请输入YouTube视频URL: ").strip()
        if not url:
            print("❌ URL不能为空")
            return
        
        use_segment = input("✂️  是否需要切片? (y/N): ").strip().lower()
        
        start_time = None
        end_time = None
        
        if use_segment == 'y':
            start_time = input("⏱️  开始时间 (如: 2m36s): ").strip()
            end_time = input("⏱️  结束时间 (如: 5m59s): ").strip()
            
            if not start_time or not end_time:
                print("❌ 切片时间不能为空")
                return
        
        automation.process_video(url, start_time, end_time)

if __name__ == "__main__":
    main() 