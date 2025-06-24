#!/usr/bin/env python3
"""
视频封面制作脚本
为查理·辛讲述川普假铂金袖扣的故事制作封面
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail():
    """创建视频封面"""
    
    # 封面尺寸 (16:9 比例，适合B站和各大平台)
    width, height = 1920, 1080
    
    # 创建渐变背景
    img = Image.new('RGB', (width, height), color='white')
    
    # 创建渐变背景 (从深蓝到浅蓝)
    for y in range(height):
        # 计算渐变色
        ratio = y / height
        r = int(20 + (100 - 20) * ratio)
        g = int(40 + (150 - 40) * ratio)  
        b = int(80 + (200 - 80) * ratio)
        
        # 绘制渐变线条
        for x in range(width):
            img.putpixel((x, y), (r, g, b))
    
    draw = ImageDraw.Draw(img)
    
    # 尝试加载中文字体
    try:
        # macOS 系统中文字体
        title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 80)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 50)
        accent_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 40)
    except:
        try:
            # 备用字体
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 80)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 50)
            accent_font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode.ttf", 40)
        except:
            # 默认字体
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            accent_font = ImageFont.load_default()
    
    # 添加阴影效果的文字函数
    def draw_text_with_shadow(draw, text, position, font, fill_color, shadow_color, shadow_offset=(3, 3)):
        x, y = position
        # 绘制阴影
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color)
        # 绘制主文字
        draw.text((x, y), text, font=font, fill=fill_color)
    
    # 主标题 - 突出重点
    main_title = "查理·辛揭露川普"
    main_title_bbox = draw.textbbox((0, 0), main_title, font=title_font)
    main_title_width = main_title_bbox[2] - main_title_bbox[0]
    draw_text_with_shadow(
        draw, main_title, 
        ((width - main_title_width) // 2, 200),
        title_font, 
        (255, 255, 255), 
        (0, 0, 0)
    )
    
    # 副标题 - 吸引眼球的关键词
    subtitle = "假铂金袖扣的真相"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw_text_with_shadow(
        draw, subtitle, 
        ((width - subtitle_width) // 2, 300),
        subtitle_font, 
        (255, 255, 100), 
        (0, 0, 0)
    )
    
    # 引人注目的标签
    tagline = "好莱坞巨星亲述"
    tagline_bbox = draw.textbbox((0, 0), tagline, font=accent_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    draw_text_with_shadow(
        draw, tagline, 
        ((width - tagline_width) // 2, 400),
        accent_font, 
        (200, 200, 200), 
        (0, 0, 0)
    )
    
    # 添加装饰性元素 - 金色边框
    border_width = 10
    # 上边框
    draw.rectangle([50, 50, width-50, 50+border_width], fill=(255, 215, 0))
    # 下边框  
    draw.rectangle([50, height-50-border_width, width-50, height-50], fill=(255, 215, 0))
    # 左边框
    draw.rectangle([50, 50, 50+border_width, height-50], fill=(255, 215, 0))
    # 右边框
    draw.rectangle([width-50-border_width, 50, width-50, height-50], fill=(255, 215, 0))
    
    # 添加水印
    watermark = "董卓主演脱口秀"
    watermark_bbox = draw.textbbox((0, 0), watermark, font=accent_font)
    watermark_width = watermark_bbox[2] - watermark_bbox[0]
    draw_text_with_shadow(
        draw, watermark, 
        (width - watermark_width - 80, height - 100),
        accent_font, 
        (255, 255, 255), 
        (0, 0, 0)
    )
    
    # 添加关键词标签
    keywords = ["真实故事", "独家爆料", "必看"]
    keyword_y = 700
    total_keywords_width = sum([draw.textbbox((0, 0), kw, font=accent_font)[2] - draw.textbbox((0, 0), kw, font=accent_font)[0] for kw in keywords]) + 60
    start_x = (width - total_keywords_width) // 2
    
    for i, keyword in enumerate(keywords):
        # 绘制标签背景
        kw_bbox = draw.textbbox((0, 0), keyword, font=accent_font)
        kw_width = kw_bbox[2] - kw_bbox[0]
        kw_height = kw_bbox[3] - kw_bbox[1]
        
        # 背景圆角矩形
        tag_x = start_x + i * (kw_width + 30)
        draw.rectangle([tag_x - 10, keyword_y - 10, tag_x + kw_width + 10, keyword_y + kw_height + 10], 
                      fill=(255, 0, 0), outline=(255, 255, 255), width=2)
        
        # 标签文字
        draw.text((tag_x, keyword_y), keyword, font=accent_font, fill=(255, 255, 255))
    
    return img

def main():
    """主函数"""
    print("开始制作视频封面...")
    
    # 创建封面
    thumbnail = create_thumbnail()
    
    # 确保输出目录存在
    os.makedirs('output', exist_ok=True)
    
    # 保存封面
    thumbnail_path = 'output/video_thumbnail.jpg'
    thumbnail.save(thumbnail_path, 'JPEG', quality=95)
    
    print(f"封面已保存到: {thumbnail_path}")
    
    # 也创建一个PNG版本
    png_path = 'output/video_thumbnail.png'
    thumbnail.save(png_path, 'PNG')
    print(f"PNG版本已保存到: {png_path}")
    
    # 显示封面信息
    print(f"封面尺寸: {thumbnail.size}")
    print("封面制作完成！")

if __name__ == "__main__":
    main() 