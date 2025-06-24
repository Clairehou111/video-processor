#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站视频封面生成器
基于PIL库制作专业的视频封面
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_bilibili_thumbnail(output_path="thumbnail.jpg"):
    """生成B站视频封面"""
    print("🎨 开始生成B站视频封面...")
    
    # 创建画布 (1920x1080, B站推荐尺寸)
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color='#1a1a2e')  # 深蓝背景
    draw = ImageDraw.Draw(img)
    
    # 渐变背景效果
    create_gradient_background(img, draw, width, height)
    
    # 添加主标题
    add_main_title(img, draw, width, height)
    
    # 添加副标题
    add_subtitle(img, draw, width, height)
    
    # 添加装饰元素
    add_decorative_elements(img, draw, width, height)
    
    # 添加节目标识
    add_show_branding(img, draw, width, height)
    
    # 保存封面
    img.save(output_path, 'JPEG', quality=95)
    print(f"✅ 封面已生成: {output_path}")
    
    return output_path

def create_gradient_background(img, draw, width, height):
    """创建渐变背景"""
    # 红蓝对比渐变 (政治色彩)
    for y in range(height):
        # 从深蓝到深红的渐变
        blue_ratio = 1 - (y / height)
        red_ratio = y / height
        
        r = int(26 + red_ratio * 100)    # 26 -> 126
        g = int(26 + blue_ratio * 20)    # 26 -> 46  
        b = int(46 + blue_ratio * 100)   # 46 -> 146
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        draw.line([(0, y), (width, y)], fill=color)

def add_main_title(img, draw, width, height):
    """添加主标题: 被爆破了"""
    try:
        # 尝试使用系统字体
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",  # macOS
            "/System/Library/Fonts/Hiragino Sans GB.ttc",  # macOS备用
            "C:/Windows/Fonts/simhei.ttf",  # Windows
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"  # Linux
        ]
        
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 120)
                break
        
        if font is None:
            font = ImageFont.load_default()
        
    except:
        font = ImageFont.load_default()
    
    # 主标题文字
    main_text = "被爆破了"
    
    # 获取文字尺寸
    bbox = draw.textbbox((0, 0), main_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 计算位置 (偏左上)
    x = width // 6
    y = height // 4
    
    # 添加阴影效果
    shadow_offset = 5
    draw.text((x + shadow_offset, y + shadow_offset), main_text, 
              font=font, fill='#000000')
    
    # 添加主文字 (红色)
    draw.text((x, y), main_text, font=font, fill='#ff4444')

def add_subtitle(img, draw, width, height):
    """添加副标题"""
    try:
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
        ]
        
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 60)
                break
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    subtitle = "连人口都不知道还想开战？"
    
    # 计算位置 (主标题下方)
    x = width // 6
    y = height // 4 + 160
    
    # 添加阴影
    draw.text((x + 3, y + 3), subtitle, font=font, fill='#000000')
    # 主文字 (白色)
    draw.text((x, y), subtitle, font=font, fill='#ffffff')

def add_decorative_elements(img, draw, width, height):
    """添加装饰元素"""
    # 爆炸效果圆圈
    explosion_centers = [
        (width * 0.8, height * 0.3),
        (width * 0.85, height * 0.6),
        (width * 0.75, height * 0.7)
    ]
    
    for center in explosion_centers:
        x, y = center
        # 多层圆圈营造爆炸效果
        for i, radius in enumerate([40, 30, 20, 10]):
            alpha = 100 - i * 20
            color = f'#ff{alpha:02x}{alpha:02x}'
            
            # 绘制圆圈
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        outline=color, width=3)
    
    # 添加一些线条效果
    for i in range(5):
        start_x = width * 0.7 + i * 20
        start_y = height * 0.2
        end_x = start_x + 100
        end_y = start_y + 150
        
        draw.line([(start_x, start_y), (end_x, end_y)], 
                 fill='#ffff44', width=3)

def add_show_branding(img, draw, width, height):
    """添加节目标识"""
    try:
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc", 
            "C:/Windows/Fonts/simhei.ttf",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
        ]
        
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 40)
                break
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Daily Show精选标识
    branding_text = "Daily Show精选"
    
    # 位置 (右下角)
    x = width - 300
    y = height - 100
    
    # 背景框
    bbox = draw.textbbox((x, y), branding_text, font=font)
    padding = 10
    draw.rectangle([bbox[0]-padding, bbox[1]-padding, 
                   bbox[2]+padding, bbox[3]+padding], 
                  fill='#000000', outline='#ffffff', width=2)
    
    # 文字
    draw.text((x, y), branding_text, font=font, fill='#ffffff')
    
    # 董卓主演脱口秀水印 (右上角)
    watermark = "董卓主演脱口秀"
    wm_x = width - 280
    wm_y = 30
    
    draw.text((wm_x + 2, wm_y + 2), watermark, font=font, fill='#000000')
    draw.text((wm_x, wm_y), watermark, font=font, fill='#ffffff')

def create_character_placeholder(img, draw, width, height):
    """创建人物占位符 (因为我们没有实际照片)"""
    # Ted Cruz 占位符 (左侧)
    ted_x, ted_y = width // 4, height // 2
    ted_width, ted_height = 200, 300
    
    # 绘制人物轮廓
    draw.rectangle([ted_x, ted_y, ted_x + ted_width, ted_y + ted_height],
                  outline='#ffffff', width=3)
    
    # 添加标签
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 30)
    except:
        font = ImageFont.load_default()
    
    draw.text((ted_x, ted_y - 40), "Ted Cruz", font=font, fill='#ffffff')
    draw.text((ted_x, ted_y - 10), "😅", font=font, fill='#ffffff')
    
    # Tucker Carlson 占位符 (右侧)
    tucker_x = width - width // 4 - ted_width
    tucker_y = height // 2
    
    draw.rectangle([tucker_x, tucker_y, tucker_x + ted_width, tucker_y + ted_height],
                  outline='#ffffff', width=3)
    
    draw.text((tucker_x, tucker_y - 40), "Tucker Carlson", font=font, fill='#ffffff')
    draw.text((tucker_x, tucker_y - 10), "🤔", font=font, fill='#ffffff')

def main():
    """主函数"""
    print("🎨 B站封面生成器")
    print("="*40)
    
    # 确保输出目录存在
    project_dir = "output/Ted_Cruz_&_Tucker_Carlson_Battle_Over_Iran_While_T_20250623_172209"
    if not os.path.exists(project_dir):
        os.makedirs(project_dir, exist_ok=True)
    
    output_path = f"{project_dir}/bilibili_thumbnail.jpg"
    
    # 生成封面
    create_bilibili_thumbnail(output_path)
    
    print(f"\n📁 封面已保存到: {output_path}")
    print("📏 尺寸: 1920x1080")
    print("📊 格式: JPEG (高质量)")
    print("🎯 适用于B站上传")
    
    print("\n💡 使用建议:")
    print("1. 可以用图片编辑软件进一步优化")
    print("2. 添加实际人物照片会更有吸引力")
    print("3. 根据需要调整颜色和文字")

if __name__ == "__main__":
    main() 