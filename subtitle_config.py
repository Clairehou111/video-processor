#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字幕配置模块 - 统一管理字幕格式标准

经过实际测试验证的最佳字幕配置：
- 完美的位置设置，避免字幕忽高忽低
- 精确的时间同步，无延迟问题
- 专业的白色字幕格式
- 标准化的水印设置

版本: v2.0 (2025-01-23)
最后更新: 字幕位置下移20像素优化
"""

# 字幕配置标准 (已验证的最佳设置)
SUBTITLE_CONFIG = {
    # 中文字幕配置
    'chinese': {
        'fontname': 'PingFang SC',
        'fontsize': 22,
        'margin_v_bilingual': 60,  # 双语模式下的位置
        'margin_v_single': 40,     # 单语模式下的位置
        'color': '&Hffffff',       # 白色
        'outline_color': '&H000000',
        'back_color': '&H80000000',
        'outline': 2,
        'alignment': 2,            # 底部居中
    },
    
    # 英文字幕配置
    'english': {
        'fontname': 'Arial',
        'fontsize': 18,
        'margin_v': 20,            # 固定位置
        'color': '&Hffffff',       # 白色
        'outline_color': '&H000000',
        'back_color': '&H80000000',
        'outline': 2,
        'alignment': 2,            # 底部居中
    },
    
    # 水印配置
    'watermark': {
        'fontname': 'PingFang SC',
        'fontsize': 24,
        'margin_v': 15,            # 顶部边距
        'margin_l': 10,            # 左边距
        'margin_r': 15,            # 右边距
        'color': '&Hffffff',       # 白色
        'outline_color': '&H000000',
        'back_color': '&H80000000',
        'outline': 1,
        'alignment': 9,            # 右上角
        'text': '董卓主演脱口秀',
        'duration_start': '0:00:00.00',
        'duration_end': '9:59:59.99',
    }
}

def get_bilingual_ass_template():
    """获取双语字幕ASS模板"""
    config = SUBTITLE_CONFIG
    
    template = f"""[Script Info]
Title: Bilingual Subtitles - Perfect Configuration
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,{config['chinese']['fontname']},{config['chinese']['fontsize']},{config['chinese']['color']},{config['chinese']['color']},{config['chinese']['outline_color']},{config['chinese']['back_color']},0,0,0,0,100,100,0,0,1,{config['chinese']['outline']},0,{config['chinese']['alignment']},10,10,{config['chinese']['margin_v_bilingual']},1
Style: English,{config['english']['fontname']},{config['english']['fontsize']},{config['english']['color']},{config['english']['color']},{config['english']['outline_color']},{config['english']['back_color']},0,0,0,0,100,100,0,0,1,{config['english']['outline']},0,{config['english']['alignment']},10,10,{config['english']['margin_v']},1
Style: Watermark,{config['watermark']['fontname']},{config['watermark']['fontsize']},{config['watermark']['color']},{config['watermark']['color']},{config['watermark']['outline_color']},{config['watermark']['back_color']},1,0,0,0,100,100,0,0,1,{config['watermark']['outline']},0,{config['watermark']['alignment']},{config['watermark']['margin_l']},{config['watermark']['margin_r']},{config['watermark']['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{config['watermark']['duration_start']},{config['watermark']['duration_end']},Watermark,,0,0,0,,{config['watermark']['text']}
"""
    return template

def get_chinese_ass_template():
    """获取中文字幕ASS模板"""
    config = SUBTITLE_CONFIG
    
    template = f"""[Script Info]
Title: Chinese Subtitles - Perfect Configuration
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,{config['chinese']['fontname']},{config['chinese']['fontsize']},{config['chinese']['color']},{config['chinese']['color']},{config['chinese']['outline_color']},{config['chinese']['back_color']},0,0,0,0,100,100,0,0,1,{config['chinese']['outline']},0,{config['chinese']['alignment']},10,10,{config['chinese']['margin_v_single']},1
Style: Watermark,{config['watermark']['fontname']},{config['watermark']['fontsize']},{config['watermark']['color']},{config['watermark']['color']},{config['watermark']['outline_color']},{config['watermark']['back_color']},1,0,0,0,100,100,0,0,1,{config['watermark']['outline']},0,{config['watermark']['alignment']},{config['watermark']['margin_l']},{config['watermark']['margin_r']},{config['watermark']['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{config['watermark']['duration_start']},{config['watermark']['duration_end']},Watermark,,0,0,0,,{config['watermark']['text']}
"""
    return template

def srt_time_to_seconds(time_str):
    """将SRT时间格式转换为秒数 - 精确处理"""
    time_str = time_str.replace(',', '.')
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def seconds_to_ass_time(seconds):
    """将秒数转换为ASS时间格式 - 精确同步"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:01d}:{minutes:02d}:{secs:05.2f}"

def create_perfect_bilingual_ass(english_srt_path, chinese_srt_path, output_path):
    """创建完美配置的双语ASS字幕"""
    
    # 获取模板
    ass_content = get_bilingual_ass_template()
    
    # 读取并处理字幕
    def process_subtitles(srt_path, style_name):
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = content.strip().split('\n\n')
        lines = []
        
        for block in blocks:
            block_lines = block.strip().split('\n')
            if len(block_lines) >= 3:
                time_line = block_lines[1]
                text_lines = block_lines[2:]
                text = ' '.join(text_lines).strip()
                
                if '-->' in time_line:
                    start_str, end_str = time_line.split(' --> ')
                    start_str = start_str.strip()
                    end_str = end_str.strip()
                    
                    # 精确时间转换
                    start_seconds = srt_time_to_seconds(start_str)
                    end_seconds = srt_time_to_seconds(end_str)
                    start_ass = seconds_to_ass_time(start_seconds)
                    end_ass = seconds_to_ass_time(end_seconds)
                    
                    lines.append(f"Dialogue: 0,{start_ass},{end_ass},{style_name},,0,0,0,,{text}")
        
        return lines
    
    # 处理中文和英文字幕
    chinese_lines = process_subtitles(chinese_srt_path, 'Chinese')
    english_lines = process_subtitles(english_srt_path, 'English')
    
    # 合并字幕行
    all_lines = chinese_lines + english_lines
    ass_content += '\n'.join(all_lines)
    
    # 保存文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ass_content)
    
    return output_path

def create_perfect_chinese_ass(chinese_srt_path, output_path):
    """创建完美配置的中文ASS字幕"""
    
    # 获取模板
    ass_content = get_chinese_ass_template()
    
    # 处理中文字幕
    with open(chinese_srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        block_lines = block.strip().split('\n')
        if len(block_lines) >= 3:
            time_line = block_lines[1]
            text_lines = block_lines[2:]
            text = ' '.join(text_lines).strip()
            
            if '-->' in time_line:
                start_str, end_str = time_line.split(' --> ')
                start_str = start_str.strip()
                end_str = end_str.strip()
                
                # 精确时间转换
                start_seconds = srt_time_to_seconds(start_str)
                end_seconds = srt_time_to_seconds(end_str)
                start_ass = seconds_to_ass_time(start_seconds)
                end_ass = seconds_to_ass_time(end_seconds)
                
                ass_content += f"Dialogue: 0,{start_ass},{end_ass},Chinese,,0,0,0,,{text}\n"
    
    # 保存文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ass_content)
    
    return output_path

def print_config_summary():
    """打印配置摘要"""
    config = SUBTITLE_CONFIG
    
    print("📝 字幕配置标准 (已验证的最佳设置):")
    print(f"   - 中文字幕: {config['chinese']['fontname']}, {config['chinese']['fontsize']}px, MarginV={config['chinese']['margin_v_bilingual']}, 白色({config['chinese']['color']})")
    print(f"   - 英文字幕: {config['english']['fontname']}, {config['english']['fontsize']}px, MarginV={config['english']['margin_v']}, 白色({config['english']['color']})")
    print(f"   - 水印: {config['watermark']['fontname']}, {config['watermark']['fontsize']}px, 右上角(Alignment={config['watermark']['alignment']}), MarginV={config['watermark']['margin_v']}, 白色")
    print(f"   - 水印内容: \"{config['watermark']['text']}\"")
    print("   - 这些参数确保字幕位置稳定、时间精确同步、显示效果最佳")

if __name__ == "__main__":
    print_config_summary() 