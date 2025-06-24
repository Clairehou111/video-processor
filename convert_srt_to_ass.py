#!/usr/bin/env python3
"""
Convert bilingual SRT subtitles to ASS format with different font sizes
Chinese: 22px, English: 18px
"""

def convert_srt_to_ass(srt_file, ass_file):
    # ASS header
    ass_content = """[Script Info]
Title: Bilingual Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Chinese,PingFang SC,22,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,60,1
Style: English,Arial,18,&Hffffff,&Hffffff,&H000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    # Read SRT file
    with open(srt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip subtitle number
        if line.isdigit():
            i += 1
            continue
        
        # Parse time
        if '-->' in line:
            time_line = line.replace(',', '.')
            start_time, end_time = time_line.split(' --> ')
            
            # Convert time format from SRT to ASS
            start_ass = start_time.replace('.', ':')[:-1]  # Remove last digit
            end_ass = end_time.replace('.', ':')[:-1]      # Remove last digit
            
            i += 1
            
            # Get Chinese subtitle
            chinese_line = lines[i].strip() if i < len(lines) else ""
            i += 1
            
            # Get English subtitle  
            english_line = lines[i].strip() if i < len(lines) else ""
            i += 1
            
            # Add to ASS content
            if chinese_line:
                ass_content += f"Dialogue: 0,{start_ass},{end_ass},Chinese,,0,0,0,,{chinese_line}\n"
            if english_line:
                ass_content += f"Dialogue: 0,{start_ass},{end_ass},English,,0,0,0,,{english_line}\n"
        else:
            i += 1
    
    # Write ASS file
    with open(ass_file, 'w', encoding='utf-8') as f:
        f.write(ass_content)
    
    print(f"Converted {srt_file} to {ass_file}")

if __name__ == "__main__":
    convert_srt_to_ass("output/optimized_bilingual.srt", "output/complete_bilingual.ass") 