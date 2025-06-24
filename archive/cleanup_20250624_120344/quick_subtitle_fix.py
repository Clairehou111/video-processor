#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速字幕修正工具 - 使用规则修正和重新生成
"""

import os
import sys
import re
import whisper
import time
from pathlib import Path

class QuickSubtitleFixer:
    """快速字幕修正器"""
    
    def __init__(self):
        self.whisper_model = None
        
    def load_available_model(self):
        """加载最好的可用模型"""
        models_to_try = ["large-v3", "base"]  # 按优先级排序
        
        for model_name in models_to_try:
            try:
                print(f"🔄 尝试加载 {model_name} 模型...")
                self.whisper_model = whisper.load_model(model_name)
                print(f"✅ 成功加载 {model_name} 模型")
                return model_name
            except Exception as e:
                print(f"⚠️ {model_name} 模型加载失败: {e}")
                continue
        
        print("❌ 无法加载任何Whisper模型")
        return None
    
    def apply_rule_based_fixes(self, text):
        """应用基于规则的修正"""
        corrections = {
            # 主要错误
            "rosary's a down": "groceries are down",
            "rosary a down": "groceries are down", 
            "rosary's": "groceries",
            "rosary": "groceries",
            "rosaries": "groceries",
            
            # 语法修正
            " a down": " are down",
            " is down": " are down",
            
            # 人名修正
            "ted crews": "ted cruz",
            "tucker karlson": "tucker carlson",
            "tucker carlsen": "tucker carlson",
            
            # 其他常见错误
            "iran's": "iran",
            "israel's": "israel",
        }
        
        fixed_text = text
        for wrong, correct in corrections.items():
            if wrong in fixed_text.lower():
                # 保持原始大小写模式
                pattern = re.compile(re.escape(wrong), re.IGNORECASE)
                fixed_text = pattern.sub(correct, fixed_text)
        
        return fixed_text
    
    def fix_srt_file(self, srt_path):
        """修正SRT文件中的错误"""
        print(f"🔄 修正字幕文件: {os.path.basename(srt_path)}")
        
        try:
            with open(srt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            fixed_lines = []
            fixes_count = 0
            
            for line in lines:
                # 跳过时间戳和序号行
                if '-->' in line or line.strip().isdigit() or line.strip() == '':
                    fixed_lines.append(line)
                else:
                    # 这是字幕文本行
                    original = line
                    fixed = self.apply_rule_based_fixes(line)
                    
                    if fixed != original:
                        fixes_count += 1
                        print(f"   修正: '{original}' -> '{fixed}'")
                    
                    fixed_lines.append(fixed)
            
            # 保存修正后的文件
            fixed_path = srt_path.replace('.srt', '_fixed.srt')
            with open(fixed_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(fixed_lines))
            
            print(f"✅ 字幕修正完成，共修正 {fixes_count} 处错误")
            print(f"   原始文件: {srt_path}")
            print(f"   修正文件: {fixed_path}")
            
            return fixed_path
            
        except Exception as e:
            print(f"❌ 文件修正失败: {e}")
            return None
    
    def regenerate_with_better_model(self, video_path, output_path):
        """使用更好的模型重新生成字幕"""
        if not self.whisper_model:
            model_name = self.load_available_model()
            if not model_name:
                return None
        
        print(f"🔄 使用改进参数重新生成字幕...")
        
        try:
            # 使用优化参数重新转录
            result = self.whisper_model.transcribe(
                video_path,
                language="en",
                temperature=0.0,  # 更确定性的结果
                initial_prompt="This is a political comedy show discussing groceries, eggs, Trump, Iran, Israel.",
                condition_on_previous_text=True
            )
            
            segments = result.get("segments", [])
            
            # 保存新的字幕文件
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments, 1):
                    start_time = self.format_time_srt(segment['start'])
                    end_time = self.format_time_srt(segment['end'])
                    text = segment['text'].strip()
                    
                    # 应用规则修正
                    text = self.apply_rule_based_fixes(text)
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            print(f"✅ 重新生成完成，共 {len(segments)} 个片段")
            return output_path
            
        except Exception as e:
            print(f"❌ 重新生成失败: {e}")
            return None
    
    def format_time_srt(self, seconds):
        """将秒数转换为SRT时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
    def quick_fix_project(self, project_dir):
        """快速修正项目中的字幕"""
        print("🚀 快速字幕修正工具")
        print("="*50)
        
        # 查找原始视频文件
        video_file = None
        for ext in ['.mp4', '.webm', '.mkv', '.avi']:
            for file in os.listdir(project_dir):
                if file.endswith(ext) and not any(x in file.lower() for x in ['bilingual', 'chinese', 'final']):
                    video_file = os.path.join(project_dir, file)
                    break
            if video_file:
                break
        
        # 查找英文字幕文件
        subtitle_file = None
        subtitle_dir = os.path.join(project_dir, 'subtitles')
        if os.path.exists(subtitle_dir):
            for file in os.listdir(subtitle_dir):
                if file.endswith('_english.srt') and 'fixed' not in file:
                    subtitle_file = os.path.join(subtitle_dir, file)
                    break
        
        if not video_file or not subtitle_file:
            print(f"❌ 未找到视频文件或字幕文件")
            return None
        
        print(f"📁 项目: {os.path.basename(project_dir)}")
        print(f"🎬 视频: {os.path.basename(video_file)}")
        print(f"📝 字幕: {os.path.basename(subtitle_file)}")
        
        # 方法1: 快速规则修正
        print(f"\n🔧 方法1: 应用规则修正...")
        fixed_srt = self.fix_srt_file(subtitle_file)
        
        # 方法2: 重新生成（可选）
        regenerated_srt = None
        user_choice = input(f"\n❓ 是否要用更好的模型重新生成字幕？(y/N): ").strip().lower()
        if user_choice == 'y':
            print(f"\n🔧 方法2: 重新生成字幕...")
            regenerated_path = subtitle_file.replace('.srt', '_regenerated.srt')
            regenerated_srt = self.regenerate_with_better_model(video_file, regenerated_path)
        
        return {
            'fixed_srt': fixed_srt,
            'regenerated_srt': regenerated_srt,
            'video_file': video_file
        }

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python quick_subtitle_fix.py <项目目录>")
        print("例如: python quick_subtitle_fix.py output/Ted_Cruz_&_Tucker_Carlson_Battle_Over_Iran_While_T_20250623_172209")
        return
    
    project_dir = sys.argv[1]
    
    if not os.path.exists(project_dir):
        print(f"❌ 项目目录不存在: {project_dir}")
        return
    
    fixer = QuickSubtitleFixer()
    result = fixer.quick_fix_project(project_dir)
    
    if result:
        print(f"\n🎉 字幕修正完成！")
        if result['fixed_srt']:
            print(f"   规则修正版: {result['fixed_srt']}")
        if result['regenerated_srt']:
            print(f"   重新生成版: {result['regenerated_srt']}")
        
        print(f"\n💡 下一步: 使用修正后的字幕重新生成视频")
        print(f"   可以修改 continue_workflow_with_watermark.py 来使用新字幕文件")

if __name__ == "__main__":
    main() 