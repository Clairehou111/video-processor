#!/usr/bin/env python3
"""
测试版本 - 使用更明显的字幕样式
"""

import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def create_test_video_with_subtitles():
    """创建测试视频，只显示前几个字幕"""
    
    # 找到原始视频
    video_files = []
    if os.path.exists("output"):
        for file in os.listdir("output"):
            if file.endswith('.mp4') and 'final' not in file and 'test' not in file:
                video_files.append(os.path.join("output", file))
    
    if not video_files:
        print("❌ 未找到原始视频文件")
        return None
    
    video_path = video_files[0]
    print(f"📹 使用视频: {video_path}")
    
    try:
        # 加载视频
        video = VideoFileClip(video_path)
        
        # 创建测试字幕 - 使用非常明显的样式
        test_subtitles = [
            {
                'text': '测试字幕 - 如果你能看到这个就说明字幕工作正常',
                'start': 5,
                'end': 10
            },
            {
                'text': '现在我得说，他看起来有点惊讶\n反对这么做，因为，我不知道你们知不知道',
                'start': 0,
                'end': 5
            }
        ]
        
        subtitle_clips = []
        
        for subtitle in test_subtitles:
            # 使用非常明显的样式
            txt_clip = TextClip(
                subtitle['text'],
                fontsize=40,  # 更大的字体
                color='red',  # 红色字体
                stroke_color='white',  # 白色描边
                stroke_width=5,  # 更粗的描边
                method='caption',
                size=(video.w - 50, None),
                align='center'
            ).set_start(subtitle['start']).set_duration(subtitle['end'] - subtitle['start'])
            
            # 设置在视频中央
            txt_clip = txt_clip.set_position(('center', 'center'))
            subtitle_clips.append(txt_clip)
        
        # 合成视频
        final_video = CompositeVideoClip([video] + subtitle_clips)
        
        # 只导出前15秒作为测试
        test_video = final_video.subclip(0, 15)
        
        output_path = "output/test_subtitles.mp4"
        test_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        print(f"✅ 测试视频生成成功: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 测试视频生成失败: {e}")
        return None

if __name__ == "__main__":
    print("🧪 生成测试视频")
    result = create_test_video_with_subtitles()
    if result:
        print("🎬 请播放测试视频，检查是否能看到红色字幕")
        print("   如果能看到，说明字幕功能正常，可能是原视频的字幕样式问题")
        print("   如果看不到，说明可能是QuickTime Player的兼容性问题") 