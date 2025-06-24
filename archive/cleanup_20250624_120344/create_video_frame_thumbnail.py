#!/usr/bin/env python3
"""
基于视频帧的封面制作脚本
从查理·辛视频中提取帧画面并添加文案
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import cv2
import os
import numpy as np

def extract_video_frame(video_path, frame_time=30):
    """从视频中提取指定时间的帧"""
    cap = cv2.VideoCapture(video_path)
    
    # 设置到指定时间（秒）
    cap.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)
    
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        # 转换颜色空间从BGR到RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 转换为PIL Image
        pil_image = Image.fromarray(frame_rgb)
        return pil_image
    else:
        return None

def create_thumbnail_with_video_frame():
    """创建基于视频帧的封面"""
    
    # 使用bilibili HD版本视频
    video_path = 'output/bilibili_hd_dual_2min37s.mp4'
    
    # 提取视频帧（选择查理·辛在讲话的时刻，大约30秒处）
    frame = extract_video_frame(video_path, frame_time=30)
    if frame is None:
        print("无法提取视频帧，使用备用视频...")
        # 备用视频
        video_path = 'output/tiktok_version_2min37s.mp4'
        frame = extract_video_frame(video_path, frame_time=30)
        
    if frame is None:
        print("无法提取视频帧，创建纯色背景...")
        frame = Image.new('RGB', (1920, 1080), color=(30, 50, 100))
    
    # 调整到标准封面尺寸
    width, height = 1920, 1080
    frame = frame.resize((width, height), Image.Resampling.LANCZOS)
    
    # 创建半透明叠加层来确保文字可读性
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 120))
    frame = frame.convert('RGBA')
    frame = Image.alpha_composite(frame, overlay).convert('RGB')
    
    draw = ImageDraw.Draw(frame)
    
    # 尝试加载中文字体
    try:
        # macOS 系统中文字体
        title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 48)
        accent_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
    except:
        try:
            # 备用字体
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 72)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 48)
            accent_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 36)
        except:
            # 默认字体
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            accent_font = ImageFont.load_default()
    
    # 添加阴影效果的文字函数
    def draw_text_with_shadow(draw, text, position, font, fill_color, shadow_color, shadow_offset=(4, 4)):
        x, y = position
        # 绘制阴影
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color)
        # 绘制主文字
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # 主标题：特朗普的哈里·温斯顿袖扣？
    main_title = "特朗普的哈里·温斯顿袖扣？"
    main_title_bbox = draw.textbbox((0, 0), main_title, font=title_font)
    main_title_width = main_title_bbox[2] - main_title_bbox[0]
    draw_text_with_shadow(
        draw, main_title, 
        ((width - main_title_width) // 2, 150),
        title_font, 
        (255, 255, 255), 
        (0, 0, 0),
        shadow_offset=(5, 5)
    )
    
    # 副标题：查理·辛：假货
    subtitle = "查理·辛：假货"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw_text_with_shadow(
        draw, subtitle, 
        ((width - subtitle_width) // 2, 250),
        subtitle_font, 
        (255, 100, 100), 
        (0, 0, 0),
        shadow_offset=(4, 4)
    )
    
    # 添加装饰性边框
    border_width = 8
    border_color = (255, 215, 0)  # 金色
    
    # 上边框
    draw.rectangle([20, 20, width-20, 20+border_width], fill=border_color)
    # 下边框  
    draw.rectangle([20, height-20-border_width, width-20, height-20], fill=border_color)
    # 左边框
    draw.rectangle([20, 20, 20+border_width, height-20], fill=border_color)
    # 右边框
    draw.rectangle([width-20-border_width, 20, width-20, height-20], fill=border_color)
    
    # 添加水印
    watermark = "董卓主演脱口秀"
    watermark_bbox = draw.textbbox((0, 0), watermark, font=accent_font)
    watermark_width = watermark_bbox[2] - watermark_bbox[0]
    draw_text_with_shadow(
        draw, watermark, 
        (width - watermark_width - 50, height - 80),
        accent_font, 
        (255, 255, 255), 
        (0, 0, 0),
        shadow_offset=(2, 2)
    )
    
    # 添加标签
    tag_text = "好莱坞巨星揭秘"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=accent_font)
    tag_width = tag_bbox[2] - tag_bbox[0]
    tag_height = tag_bbox[3] - tag_bbox[1]
    
    # 标签背景
    tag_x = 50
    tag_y = height - 150
    draw.rectangle([tag_x - 15, tag_y - 10, tag_x + tag_width + 15, tag_y + tag_height + 10], 
                  fill=(255, 0, 0), outline=(255, 255, 255), width=3)
    
    # 标签文字
    draw.text((tag_x, tag_y), tag_text, font=accent_font, fill=(255, 255, 255))
    
    return frame

def create_tiktok_thumbnail_with_frame():
    """创建TikTok竖屏版本的封面"""
    
    # 使用TikTok版本视频
    video_path = 'output/tiktok_version_2min37s.mp4'
    
    # 提取视频帧
    frame = extract_video_frame(video_path, frame_time=30)
    if frame is None:
        print("无法提取TikTok视频帧，创建纯色背景...")
        frame = Image.new('RGB', (1080, 1920), color=(30, 50, 100))
    
    # 调整到TikTok尺寸
    width, height = 1080, 1920
    frame = frame.resize((width, height), Image.Resampling.LANCZOS)
    
    # 创建半透明叠加层
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 100))
    frame = frame.convert('RGBA')
    frame = Image.alpha_composite(frame, overlay).convert('RGB')
    
    draw = ImageDraw.Draw(frame)
    
    # 字体设置
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 60)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 45)
        accent_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 32)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        accent_font = ImageFont.load_default()
    
    # 添加阴影效果的文字函数
    def draw_text_with_shadow(draw, text, position, font, fill_color, shadow_color, shadow_offset=(3, 3)):
        x, y = position
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color)
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # 分行显示文案
    title_line1 = "特朗普的哈里·温斯顿"
    title_line2 = "袖扣？"
    subtitle_line1 = "查理·辛："
    subtitle_line2 = "假货"
    
    # 第一行
    bbox1 = draw.textbbox((0, 0), title_line1, font=title_font)
    width1 = bbox1[2] - bbox1[0]
    draw_text_with_shadow(draw, title_line1, ((width - width1) // 2, 200), 
                         title_font, (255, 255, 255), (0, 0, 0))
    
    # 第二行
    bbox2 = draw.textbbox((0, 0), title_line2, font=title_font)
    width2 = bbox2[2] - bbox2[0]
    draw_text_with_shadow(draw, title_line2, ((width - width2) // 2, 280), 
                         title_font, (255, 255, 255), (0, 0, 0))
    
    # 副标题第一行
    bbox3 = draw.textbbox((0, 0), subtitle_line1, font=subtitle_font)
    width3 = bbox3[2] - bbox3[0]
    draw_text_with_shadow(draw, subtitle_line1, ((width - width3) // 2, 400), 
                         subtitle_font, (255, 255, 100), (0, 0, 0))
    
    # 副标题第二行
    bbox4 = draw.textbbox((0, 0), subtitle_line2, font=subtitle_font)
    width4 = bbox4[2] - bbox4[0]
    draw_text_with_shadow(draw, subtitle_line2, ((width - width4) // 2, 460), 
                         subtitle_font, (255, 100, 100), (0, 0, 0))
    
    # 边框
    border_width = 6
    draw.rectangle([15, 15, width-15, 15+border_width], fill=(255, 215, 0))
    draw.rectangle([15, height-15-border_width, width-15, height-15], fill=(255, 215, 0))
    draw.rectangle([15, 15, 15+border_width, height-15], fill=(255, 215, 0))
    draw.rectangle([width-15-border_width, 15, width-15, height-15], fill=(255, 215, 0))
    
    # 水印
    watermark = "@董卓主演脱口秀"
    wb_bbox = draw.textbbox((0, 0), watermark, font=accent_font)
    wb_width = wb_bbox[2] - wb_bbox[0]
    draw_text_with_shadow(draw, watermark, ((width - wb_width) // 2, height - 100), 
                         accent_font, (255, 255, 255), (0, 0, 0))
    
    return frame

def main():
    """主函数"""
    print("开始制作基于视频帧的封面...")
    
    # 确保输出目录存在
    os.makedirs('output', exist_ok=True)
    
    # 创建横屏封面
    try:
        thumbnail = create_thumbnail_with_video_frame()
        thumbnail_path = 'output/video_frame_thumbnail.jpg'
        thumbnail.save(thumbnail_path, 'JPEG', quality=95)
        print(f"横屏封面已保存到: {thumbnail_path}")
        
        # PNG版本
        png_path = 'output/video_frame_thumbnail.png'
        thumbnail.save(png_path, 'PNG')
        print(f"PNG版本已保存到: {png_path}")
        
    except Exception as e:
        print(f"创建横屏封面时出错: {e}")
    
    # 创建竖屏封面
    try:
        tiktok_thumbnail = create_tiktok_thumbnail_with_frame()
        tiktok_path = 'output/tiktok_frame_thumbnail.jpg'
        tiktok_thumbnail.save(tiktok_path, 'JPEG', quality=95)
        print(f"TikTok竖屏封面已保存到: {tiktok_path}")
        
        # PNG版本
        tiktok_png = 'output/tiktok_frame_thumbnail.png'
        tiktok_thumbnail.save(tiktok_png, 'PNG')
        print(f"TikTok PNG版本已保存到: {tiktok_png}")
        
    except Exception as e:
        print(f"创建竖屏封面时出错: {e}")
    
    print("基于视频帧的封面制作完成！")

if __name__ == "__main__":
    main() 