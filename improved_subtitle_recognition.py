#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的字幕识别工具
使用更高精度的模型和优化参数来提高语音识别准确率
"""

import os
import sys
import whisper
import subprocess
import tempfile
from pathlib import Path
import time

class ImprovedSubtitleRecognizer:
    """改进的字幕识别器"""
    
    def __init__(self):
        self.whisper_model = None
        self.model_size = "large-v3"  # 使用最新最高精度模型
        
    def load_whisper_model(self, model_size=None):
        """加载更高精度的Whisper模型"""
        if model_size:
            self.model_size = model_size
            
        print(f"🔄 加载Whisper {self.model_size} 模型（高精度版本）...")
        try:
            self.whisper_model = whisper.load_model(self.model_size)
            print(f"✅ 高精度Whisper模型加载成功")
            return True
        except Exception as e:
            print(f"❌ 高精度模型加载失败，尝试medium模型: {e}")
            try:
                self.model_size = "medium"
                self.whisper_model = whisper.load_model("medium")
                print(f"✅ Medium模型加载成功")
                return True
            except Exception as e2:
                print(f"❌ Medium模型也失败，使用base模型: {e2}")
                self.model_size = "base"
                self.whisper_model = whisper.load_model("base")
                return True
    
    def preprocess_audio(self, video_path):
        """预处理音频以提高识别质量"""
        try:
            # 创建临时音频文件
            temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_audio.close()
            
            # 使用ffmpeg提取高质量音频
            cmd = [
                'ffmpeg', '-i', video_path,
                '-vn',  # 不要视频
                '-acodec', 'pcm_s16le',  # 16位PCM
                '-ar', '16000',  # 16kHz采样率
                '-ac', '1',  # 单声道
                '-af', 'highpass=f=200,lowpass=f=3000',  # 滤波器减少噪音
                '-y',  # 覆盖输出文件
                temp_audio.name
            ]
            
            print(f"🔄 预处理音频以提高识别质量...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ 音频预处理完成")
                return temp_audio.name
            else:
                print(f"⚠️ 音频预处理失败，使用原始文件")
                os.unlink(temp_audio.name)
                return video_path
                
        except Exception as e:
            print(f"⚠️ 音频预处理异常: {e}，使用原始文件")
            return video_path
    
    def transcribe_with_improved_params(self, audio_path):
        """使用优化参数进行语音识别"""
        if not self.whisper_model:
            self.load_whisper_model()
        
        print(f"🔄 开始高精度语音识别...")
        print(f"📊 使用模型: {self.model_size}")
        
        start_time = time.time()
        
        try:
            # 使用优化的参数
            result = self.whisper_model.transcribe(
                audio_path,
                language="en",  # 明确指定英文
                task="transcribe",  # 转录任务
                temperature=0.0,  # 降低随机性，提高一致性
                best_of=5,  # 尝试5次取最佳结果
                beam_size=5,  # 使用束搜索
                patience=1.0,  # 耐心参数
                length_penalty=1.0,  # 长度惩罚
                suppress_tokens=[-1],  # 抑制特定token
                initial_prompt="This is a political comedy show with clear English speech. Common words include: groceries, eggs, politics, Trump, Iran, Israel, war.",  # 上下文提示
                condition_on_previous_text=True,  # 基于前文推断
                fp16=False,  # 不使用半精度以提高准确性
                compression_ratio_threshold=2.4,
                logprob_threshold=-1.0,
                no_speech_threshold=0.6
            )
            
            end_time = time.time()
            print(f"✅ 高精度识别完成，耗时 {end_time - start_time:.1f}秒")
            
            segments = result.get("segments", [])
            print(f"📊 识别出 {len(segments)} 个片段")
            
            # 显示一些识别结果作为质量检查
            print(f"\n🔍 识别质量检查 (前3个片段):")
            for i, segment in enumerate(segments[:3]):
                print(f"   {i+1}. {segment['text']}")
            
            return segments
            
        except Exception as e:
            print(f"❌ 高精度识别失败: {e}")
            return None
    
    def post_process_segments(self, segments):
        """后处理识别结果，修复常见错误"""
        print(f"🔄 后处理识别结果，修复常见错误...")
        
        # 常见错误修正词典
        corrections = {
            # 政治相关
            "rosary's": "groceries",
            "rosary": "groceries", 
            "rosaries": "groceries",
            "grocery's": "groceries",
            "groceries a down": "groceries are down",
            "rosary's a down": "groceries are down",
            "rosary a down": "groceries are down",
            
            # 人名修正
            "ted crews": "ted cruz",
            "tucker karlson": "tucker carlson",
            "tucker carlsen": "tucker carlson",
            
            # 常见词汇
            "iran's": "iran",
            "israel's": "israel",
            "polls": "polls",
            "poll": "poll",
            
            # 语法修正
            " a down": " are down",
            " is down": " are down",
        }
        
        corrected_count = 0
        for segment in segments:
            original_text = segment['text']
            corrected_text = original_text.lower()
            
            # 应用修正
            for wrong, correct in corrections.items():
                if wrong in corrected_text:
                    corrected_text = corrected_text.replace(wrong, correct)
                    corrected_count += 1
            
            # 恢复大小写（简单处理）
            if corrected_text != original_text.lower():
                # 句首大写
                corrected_text = corrected_text.capitalize()
                # 专有名词大写
                proper_nouns = ["trump", "donald", "ted cruz", "tucker carlson", "iran", "israel", "biden", "america", "american"]
                for noun in proper_nouns:
                    corrected_text = corrected_text.replace(noun, noun.title())
                
                segment['text'] = corrected_text
        
        if corrected_count > 0:
            print(f"✅ 修正了 {corrected_count} 个常见错误")
        else:
            print(f"✅ 后处理完成，未发现需要修正的错误")
        
        return segments
    
    def save_improved_subtitles(self, segments, output_path):
        """保存改进后的字幕"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments, 1):
                    start_time = self.format_time_srt(segment['start'])
                    end_time = self.format_time_srt(segment['end'])
                    text = segment['text'].strip()
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            print(f"✅ 改进版字幕已保存: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 字幕保存失败: {e}")
            return False
    
    def format_time_srt(self, seconds):
        """将秒数转换为SRT时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
    def improve_existing_subtitles(self, video_path, original_srt_path):
        """改进现有字幕文件"""
        print("🚀 开始改进现有字幕识别质量")
        print("="*60)
        
        # 1. 预处理音频
        processed_audio = self.preprocess_audio(video_path)
        
        try:
            # 2. 重新识别
            segments = self.transcribe_with_improved_params(processed_audio)
            
            if segments:
                # 3. 后处理
                segments = self.post_process_segments(segments)
                
                # 4. 保存改进版本
                improved_path = original_srt_path.replace('.srt', '_improved.srt')
                if self.save_improved_subtitles(segments, improved_path):
                    print(f"\n✅ 字幕识别改进完成!")
                    print(f"   原始文件: {original_srt_path}")
                    print(f"   改进文件: {improved_path}")
                    print(f"   共 {len(segments)} 个字幕片段")
                    return improved_path
            
        finally:
            # 清理临时文件
            if processed_audio != video_path and os.path.exists(processed_audio):
                os.unlink(processed_audio)
        
        return None

def main():
    """主函数：改进现有项目的字幕识别"""
    if len(sys.argv) != 2:
        print("使用方法: python improved_subtitle_recognition.py <项目目录>")
        print("例如: python improved_subtitle_recognition.py output/Ted_Cruz_&_Tucker_Carlson_Battle_Over_Iran_While_T_20250623_172209")
        return
    
    project_dir = sys.argv[1]
    
    if not os.path.exists(project_dir):
        print(f"❌ 项目目录不存在: {project_dir}")
        return
    
    # 查找视频文件
    video_file = None
    for ext in ['.mp4', '.webm', '.mkv', '.avi']:
        for file in os.listdir(project_dir):
            if file.endswith(ext) and not 'bilingual' in file and not 'chinese' in file:
                video_file = os.path.join(project_dir, file)
                break
        if video_file:
            break
    
    if not video_file:
        print(f"❌ 在项目目录中未找到原始视频文件")
        return
    
    # 查找原始英文字幕文件
    subtitle_file = None
    subtitle_dir = os.path.join(project_dir, 'subtitles')
    if os.path.exists(subtitle_dir):
        for file in os.listdir(subtitle_dir):
            if file.endswith('_english.srt'):
                subtitle_file = os.path.join(subtitle_dir, file)
                break
    
    if not subtitle_file:
        print(f"❌ 在项目中未找到英文字幕文件")
        return
    
    print(f"📁 项目目录: {project_dir}")
    print(f"🎬 视频文件: {os.path.basename(video_file)}")
    print(f"📝 字幕文件: {os.path.basename(subtitle_file)}")
    
    # 开始改进
    recognizer = ImprovedSubtitleRecognizer()
    improved_srt = recognizer.improve_existing_subtitles(video_file, subtitle_file)
    
    if improved_srt:
        print(f"\n🎉 改进完成！请检查改进后的字幕文件：")
        print(f"   {improved_srt}")
        print(f"\n💡 如果效果满意，可以用改进版字幕重新生成视频")
    else:
        print(f"\n❌ 字幕改进失败")

if __name__ == "__main__":
    main() 