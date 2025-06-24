#!/usr/bin/env python3
"""
英文字幕提取器 - 专门提取英文字幕，供用户手动翻译
"""

import os
import sys
import time
import whisper
import yt_dlp
from datetime import timedelta

class EnglishSubtitleExtractor:
    """英文字幕提取器"""
    
    def __init__(self):
        self.whisper_model = None
        
    def load_whisper_model(self, model_size="base"):
        """加载Whisper模型"""
        print(f"🔄 加载Whisper {model_size} 模型...")
        try:
            self.whisper_model = whisper.load_model(model_size)
            print(f"✅ Whisper模型加载成功")
            return True
        except Exception as e:
            print(f"❌ Whisper模型加载失败: {e}")
            return False
    
    def download_video(self, url, output_dir="output"):
        """下载YouTube视频"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        ydl_opts = {
            'format': 'best[height<=720]',  # 选择720p或以下质量
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'writesubtitles': False,  # 不下载现有字幕
            'writeautomaticsub': False,  # 不下载自动生成字幕
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"🔄 正在下载视频...")
                info = ydl.extract_info(url, download=True)
                video_title = info.get('title', 'video')
                # 找到下载的文件
                for file in os.listdir(output_dir):
                    if video_title.replace('/', '-') in file:
                        video_path = os.path.join(output_dir, file)
                        print(f"✅ 视频下载完成: {video_path}")
                        return video_path, video_title
                        
        except Exception as e:
            print(f"❌ 视频下载失败: {e}")
            return None, None
    
    def extract_audio(self, video_path):
        """从视频中提取音频"""
        try:
            from moviepy.editor import VideoFileClip
            
            audio_path = video_path.rsplit('.', 1)[0] + '_audio.wav'
            print(f"🔄 正在提取音频...")
            
            with VideoFileClip(video_path) as video:
                audio = video.audio
                audio.write_audiofile(audio_path, verbose=False, logger=None)
                
            print(f"✅ 音频提取完成: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ 音频提取失败: {e}")
            return None
    
    def transcribe_to_english(self, audio_path):
        """使用Whisper进行英文语音识别"""
        if not self.whisper_model:
            if not self.load_whisper_model():
                return None
                
        try:
            print(f"🔄 正在进行语音识别...")
            result = self.whisper_model.transcribe(
                audio_path,
                language="en",  # 指定英文
                task="transcribe"  # 转录任务（不翻译）
            )
            
            segments = result.get("segments", [])
            print(f"✅ 语音识别完成，共识别出 {len(segments)} 个片段")
            return segments
            
        except Exception as e:
            print(f"❌ 语音识别失败: {e}")
            return None
    
    def format_time_srt(self, seconds):
        """将秒数转换为SRT时间格式"""
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        milliseconds = int((seconds - total_seconds) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
    def save_english_srt(self, segments, output_path):
        """保存英文SRT字幕文件"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments, 1):
                    start_time = self.format_time_srt(segment['start'])
                    end_time = self.format_time_srt(segment['end'])
                    text = segment['text'].strip()
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            print(f"✅ 英文字幕已保存: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 字幕保存失败: {e}")
            return False
    
    def print_english_subtitles(self, segments):
        """在控制台打印英文字幕内容"""
        print("\n" + "="*80)
        print("📝 英文字幕内容 (可复制用于翻译)")
        print("="*80)
        
        for i, segment in enumerate(segments, 1):
            start_time = self.format_time_srt(segment['start'])
            end_time = self.format_time_srt(segment['end'])
            text = segment['text'].strip()
            
            print(f"\n{i}")
            print(f"{start_time} --> {end_time}")
            print(f"{text}")
        
        print("\n" + "="*80)
        print("💡 提示：你可以复制上面的内容，然后:")
        print("   1. 手动翻译成中文")
        print("   2. 或者把英文内容发给AI助手来翻译")
        print("="*80)
    
    def extract_subtitles(self, youtube_url):
        """完整的字幕提取流程"""
        print("🚀 开始提取英文字幕")
        print("="*60)
        
        # 1. 下载视频
        video_path, video_title = self.download_video(youtube_url)
        if not video_path:
            return False
        
        # 2. 提取音频
        audio_path = self.extract_audio(video_path)
        if not audio_path:
            return False
        
        # 3. 语音识别
        segments = self.transcribe_to_english(audio_path)
        if not segments:
            return False
        
        # 4. 保存英文SRT文件
        srt_filename = video_title.replace('/', '-') + '_english.srt'
        srt_path = os.path.join('output', srt_filename)
        
        if self.save_english_srt(segments, srt_path):
            # 5. 在控制台显示内容
            self.print_english_subtitles(segments)
            
            print(f"\n✅ 英文字幕提取完成!")
            print(f"   文件保存在: {srt_path}")
            print(f"   共 {len(segments)} 个字幕片段")
            
            return srt_path
        
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python extract_english_subtitles.py <YouTube_URL>")
        print("示例: python extract_english_subtitles.py https://www.youtube.com/watch?v=dp6BIDCZRic")
        return
    
    youtube_url = sys.argv[1]
    
    print(f"🎬 目标视频: {youtube_url}")
    
    # 创建提取器
    extractor = EnglishSubtitleExtractor()
    
    try:
        # 开始提取
        start_time = time.time()
        result = extractor.extract_subtitles(youtube_url)
        end_time = time.time()
        
        if result:
            processing_time = end_time - start_time
            print(f"\n🎉 任务完成! 总耗时: {processing_time:.1f} 秒")
            print(f"\n📋 下一步:")
            print(f"   1. 查看生成的英文字幕文件: {result}")
            print(f"   2. 复制字幕内容进行翻译")
            print(f"   3. 或者把字幕内容发给AI助手翻译")
        else:
            print("\n❌ 字幕提取失败")
            
    except KeyboardInterrupt:
        print(f"\n⚠️  用户中断提取")
    except Exception as e:
        print(f"\n❌ 提取过程出错: {e}")

if __name__ == "__main__":
    main() 