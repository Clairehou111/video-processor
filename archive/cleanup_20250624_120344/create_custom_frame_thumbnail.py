#!/usr/bin/env python3
"""
自定义时间点封面制作脚本
可以选择不同的视频时间点制作封面
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import cv2
import os
import argparse

def extract_video_frame(video_path, frame_time=30):
    """从视频中提取指定时间的帧"""
    cap = cv2.VideoCapture(video_path)
    
    # 获取视频总时长
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps if fps > 0 else 0
    
    print(f"视频总时长: {duration:.1f}秒")
    
    # 设置到指定时间（秒）
    cap.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)
    
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        # 转换颜色空间从BGR到RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 转换为PIL Image
        pil_image = Image.fromarray(frame_rgb)
        print(f"成功提取 {frame_time}秒 处的视频帧")
        return pil_image
    else:
        print(f"无法提取 {frame_time}秒 处的视频帧")
        return None

def create_enhanced_thumbnail(video_path, frame_time=30, title_text="特朗普的哈里·温斯顿袖扣？", subtitle_text="查理·辛：假货"):
    """创建增强版封面"""
    
    # 提取视频帧
    frame = extract_video_frame(video_path, frame_time)
    if frame is None:
        print("使用默认背景...")
        frame = Image.new('RGB', (1920, 1080), color=(30, 50, 100))
    
    # 调整到标准封面尺寸
    width, height = 1920, 1080
    frame = frame.resize((width, height), Image.Resampling.LANCZOS)
    
    # 增强对比度和亮度
    enhancer = ImageEnhance.Contrast(frame)
    frame = enhancer.enhance(1.2)  # 增加对比度
    
    enhancer = ImageEnhance.Brightness(frame)
    frame = enhancer.enhance(0.8)  # 稍微降低亮度
    
    # 创建渐变叠加层
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # 创建从上到下的渐变
    for y in range(height):
        alpha = int(150 * (y / height))  # 上部透明，下部更暗
        overlay_draw.rectangle([0, y, width, y+1], fill=(0, 0, 0, alpha))
    
    frame = frame.convert('RGBA')
    frame = Image.alpha_composite(frame, overlay).convert('RGB')
    
    draw = ImageDraw.Draw(frame)
    
    # 字体设置
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 80)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 55)
        accent_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 40)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        accent_font = ImageFont.load_default()
    
    # 高级阴影效果
    def draw_text_with_glow(draw, text, position, font, fill_color, glow_color=(0, 0, 0)):
        x, y = position
        # 多层阴影创建发光效果
        for offset in [(6, 6), (4, 4), (2, 2)]:
            draw.text((x + offset[0], y + offset[1]), text, font=font, fill=glow_color)
        # 主文字
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # 主标题
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw_text_with_glow(
        draw, title_text, 
        ((width - title_width) // 2, 100),
        title_font, 
        (255, 255, 255)
    )
    
    # 副标题
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw_text_with_glow(
        draw, subtitle_text, 
        ((width - subtitle_width) // 2, 200),
        subtitle_font, 
        (255, 120, 120)
    )
    
    # 装饰边框 - 双层
    border_color1 = (255, 215, 0)  # 外层金色
    border_color2 = (255, 255, 255)  # 内层白色
    
    # 外层边框
    border_width = 12
    for i in range(4):
        draw.rectangle([15, 15, width-15, 15+border_width], fill=border_color1)
        draw.rectangle([15, height-15-border_width, width-15, height-15], fill=border_color1)
        draw.rectangle([15, 15, 15+border_width, height-15], fill=border_color1)
        draw.rectangle([width-15-border_width, 15, width-15, height-15], fill=border_color1)
    
    # 内层边框
    border_width = 4
    draw.rectangle([25, 25, width-25, 25+border_width], fill=border_color2)
    draw.rectangle([25, height-25-border_width, width-25, height-25], fill=border_color2)
    draw.rectangle([25, 25, 25+border_width, height-25], fill=border_color2)
    draw.rectangle([width-25-border_width, 25, width-25, height-25], fill=border_color2)
    
    # 添加标签和装饰元素
    tag_text = "🔥 独家揭秘 🔥"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=accent_font)
    tag_width = tag_bbox[2] - tag_bbox[0]
    
    # 标签背景（圆角效果）
    tag_x = (width - tag_width) // 2
    tag_y = 320
    draw.ellipse([tag_x - 30, tag_y - 15, tag_x + tag_width + 30, tag_y + 50], 
                fill=(255, 0, 0), outline=(255, 255, 255), width=3)
    
    # 标签文字
    draw.text((tag_x, tag_y), tag_text, font=accent_font, fill=(255, 255, 255))
    
    # 水印
    watermark = "董卓主演脱口秀 - 好莱坞内幕"
    watermark_bbox = draw.textbbox((0, 0), watermark, font=accent_font)
    watermark_width = watermark_bbox[2] - watermark_bbox[0]
    draw_text_with_glow(
        draw, watermark, 
        (width - watermark_width - 50, height - 80),
        accent_font, 
        (255, 255, 255)
    )
    
    return frame

def create_multiple_thumbnails():
    """创建多个不同时间点的封面供选择"""
    
    video_path = 'output/bilibili_hd_dual_2min37s.mp4'
    
    # 不同的时间点（秒）
    time_points = [15, 30, 45, 60, 75]
    titles = [
        "特朗普的哈里·温斯顿袖扣？",
        "特朗普的哈里·温斯顿袖扣？", 
        "好莱坞巨星爆料川普",
        "查理·辛：这是假货！",
        "川普袖扣真相大白"
    ]
    subtitles = [
        "查理·辛：假货",
        "查理·辛：假货",
        "袖扣竟然是假的",
        "哈里·温斯顿变地摊货",
        "好莱坞vs商界传奇"
    ]
    
    print("开始制作多个封面版本...")
    
    for i, time_point in enumerate(time_points):
        try:
            thumbnail = create_enhanced_thumbnail(
                video_path, 
                time_point, 
                titles[i], 
                subtitles[i]
            )
            
            filename = f'output/enhanced_thumbnail_{time_point}s.jpg'
            thumbnail.save(filename, 'JPEG', quality=95)
            print(f"封面 {i+1} 已保存: {filename}")
            
        except Exception as e:
            print(f"创建第 {i+1} 个封面时出错: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='创建自定义时间点的视频封面')
    parser.add_argument('--time', type=int, default=30, help='提取帧的时间点（秒）')
    parser.add_argument('--title', type=str, default="特朗普的哈里·温斯顿袖扣？", help='主标题')
    parser.add_argument('--subtitle', type=str, default="查理·辛：假货", help='副标题')
    parser.add_argument('--multiple', action='store_true', help='创建多个版本')
    
    args = parser.parse_args()
    
    os.makedirs('output', exist_ok=True)
    
    if args.multiple:
        create_multiple_thumbnails()
    else:
        video_path = 'output/bilibili_hd_dual_2min37s.mp4'
        thumbnail = create_enhanced_thumbnail(
            video_path, 
            args.time, 
            args.title, 
            args.subtitle
        )
        
        filename = f'output/custom_thumbnail_{args.time}s.jpg'
        thumbnail.save(filename, 'JPEG', quality=95)
        print(f"自定义封面已保存: {filename}")

if __name__ == "__main__":
    main() 