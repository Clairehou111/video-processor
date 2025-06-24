#!/usr/bin/env python3
"""
剪映弹幕生成器
用于生成预埋弹幕，增强视频观看体验
"""

import json
import random
import os
from typing import List, Dict, Tuple
from datetime import timedelta

class JianyingDanmakuGenerator:
    def __init__(self):
        self.danmaku_templates = {
            "political_comedy": [
                "哈哈哈哈太真实了",
                "这节目太敢说了",
                "川普：我不是，我没有",
                "Daily Show永远的神",
                "美式政治讽刺天花板",
                "翻译太到位了",
                "up主品味不错",
                "这期笑死我了",
                "政治喜剧就得这样",
                "经典川普表情包",
                "老美的相声",
                "这翻译绝了",
                "节目效果拉满",
                "美国脱口秀天花板",
                "笑不活了"
            ],
            "reactions": [
                "😂😂😂",
                "笑死",
                "真的假的",
                "离谱",
                "绷不住了",
                "太搞笑了",
                "经典",
                "神评",
                "哈哈哈",
                "这也行？",
                "服了",
                "6666",
                "牛啊",
                "太真实",
                "笑了"
            ],
            "engagement": [
                "求更新",
                "up主加油",
                "三连走起",
                "收藏了",
                "转发给朋友",
                "等下期",
                "节目名字是什么",
                "有资源吗",
                "在哪看原版",
                "求字幕文件",
                "up主辛苦了",
                "这期质量很高",
                "期待下期",
                "已关注",
                "求更多这类视频"
            ]
        }
        
        self.danmaku_styles = {
            "scroll": {"type": 1, "color": "16777215", "size": 25},  # 滚动弹幕
            "top": {"type": 5, "color": "16777215", "size": 25},     # 顶部弹幕
            "bottom": {"type": 4, "color": "16777215", "size": 25},  # 底部弹幕
            "colorful": {"type": 1, "color": "16711680", "size": 25}, # 彩色弹幕
        }

    def generate_danmaku_data(self, video_duration_seconds: int, 
                            density: str = "medium",
                            style_distribution: Dict[str, float] = None) -> List[Dict]:
        """
        生成弹幕数据
        
        Args:
            video_duration_seconds: 视频时长（秒）
            density: 弹幕密度 ("low", "medium", "high")
            style_distribution: 弹幕类型分布
        """
        if style_distribution is None:
            style_distribution = {
                "political_comedy": 0.4,
                "reactions": 0.4,
                "engagement": 0.2
            }
        
        # 根据密度确定弹幕数量
        density_multiplier = {"low": 0.5, "medium": 1.0, "high": 1.5}
        base_count = int(video_duration_seconds / 10)  # 每10秒基础弹幕数
        total_danmaku = int(base_count * density_multiplier.get(density, 1.0))
        
        danmaku_list = []
        
        for i in range(total_danmaku):
            # 随机选择弹幕类型
            rand = random.random()
            cumulative = 0
            selected_type = "reactions"
            
            for danmaku_type, probability in style_distribution.items():
                cumulative += probability
                if rand <= cumulative:
                    selected_type = danmaku_type
                    break
            
            # 随机选择弹幕内容
            content = random.choice(self.danmaku_templates[selected_type])
            
            # 随机时间点（避免开头和结尾）
            time_offset = random.uniform(5, video_duration_seconds - 5)
            
            # 随机弹幕样式
            style_name = random.choice(list(self.danmaku_styles.keys()))
            style = self.danmaku_styles[style_name].copy()
            
            # 为重要内容使用特殊样式
            if selected_type == "political_comedy":
                if random.random() < 0.3:  # 30%概率使用彩色
                    style = self.danmaku_styles["colorful"].copy()
            
            danmaku_item = {
                "time": time_offset,
                "text": content,
                "type": style["type"],
                "color": style["color"],
                "size": style["size"],
                "category": selected_type
            }
            
            danmaku_list.append(danmaku_item)
        
        # 按时间排序
        danmaku_list.sort(key=lambda x: x["time"])
        return danmaku_list

    def create_jianying_danmaku_file(self, danmaku_data: List[Dict], 
                                   output_path: str) -> str:
        """
        创建剪映弹幕文件
        """
        jianying_danmaku = {
            "danmaku_list": []
        }
        
        for item in danmaku_data:
            jianying_item = {
                "time": int(item["time"] * 1000),  # 转为毫秒
                "text": item["text"],
                "mode": item["type"],
                "color": item["color"],
                "fontsize": item["size"],
                "border": 1,
                "opacity": 1.0
            }
            jianying_danmaku["danmaku_list"].append(jianying_item)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(jianying_danmaku, f, ensure_ascii=False, indent=2)
        
        return output_path

    def create_bilibili_danmaku_file(self, danmaku_data: List[Dict], 
                                   output_path: str) -> str:
        """
        创建B站弹幕格式文件（用于参考或其他用途）
        """
        bilibili_danmaku = []
        
        for item in danmaku_data:
            # B站弹幕格式: 时间,模式,字号,颜色,时间戳,弹幕池,用户ID,弹幕ID
            danmaku_line = f"{item['time']:.2f},{item['type']},{item['size']},{item['color']},0,0,0,0"
            bilibili_danmaku.append(f"<d p=\"{danmaku_line}\">{item['text']}</d>")
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<i>
<chatserver>chat.bilibili.com</chatserver>
<chatid>0</chatid>
<mission>0</mission>
<maxlimit>8000</maxlimit>
<state>0</state>
<real_name>0</real_name>
<source>k-v</source>
{''.join(bilibili_danmaku)}
</i>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        return output_path

    def create_smart_danmaku_for_video(self, video_path: str, 
                                     subtitle_file: str = None,
                                     output_dir: str = "output") -> Tuple[str, str]:
        """
        为特定视频智能生成弹幕
        """
        import cv2
        
        # 获取视频时长
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 120
        cap.release()
        
        print(f"视频时长: {duration:.1f}秒")
        
        # 如果有字幕文件，在关键时间点增加弹幕
        key_moments = []
        if subtitle_file and os.path.exists(subtitle_file):
            key_moments = self._extract_key_moments_from_subtitles(subtitle_file)
        
        # 生成基础弹幕
        danmaku_data = self.generate_danmaku_data(
            int(duration), 
            density="medium",
            style_distribution={
                "political_comedy": 0.5,
                "reactions": 0.35,
                "engagement": 0.15
            }
        )
        
        # 在关键时刻添加特定弹幕
        for moment in key_moments:
            special_danmaku = {
                "time": moment["time"],
                "text": moment["suggested_danmaku"],
                "type": 1,
                "color": "16711680",  # 红色
                "size": 30,
                "category": "key_moment"
            }
            danmaku_data.append(special_danmaku)
        
        # 重新排序
        danmaku_data.sort(key=lambda x: x["time"])
        
        # 创建输出文件
        os.makedirs(output_dir, exist_ok=True)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        
        jianying_file = os.path.join(output_dir, f"{video_name}_jianying_danmaku.json")
        bilibili_file = os.path.join(output_dir, f"{video_name}_bilibili_danmaku.xml")
        
        self.create_jianying_danmaku_file(danmaku_data, jianying_file)
        self.create_bilibili_danmaku_file(danmaku_data, bilibili_file)
        
        # 生成预览文件
        preview_file = os.path.join(output_dir, f"{video_name}_danmaku_preview.txt")
        self._create_preview_file(danmaku_data, preview_file)
        
        return jianying_file, bilibili_file

    def _extract_key_moments_from_subtitles(self, subtitle_file: str) -> List[Dict]:
        """
        从字幕文件提取关键时刻
        """
        key_moments = []
        
        try:
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单的关键词检测
            keywords = ["trump", "川普", "president", "总统", "政治", "election", "选举"]
            laugh_keywords = ["laugh", "funny", "joke", "笑", "搞笑", "玩笑"]
            
            # 这里可以添加更复杂的NLP分析
            # 目前使用简单的关键词匹配
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in keywords):
                    # 估算时间（这里需要更精确的SRT解析）
                    estimated_time = (i / len(lines)) * 120  # 假设总时长120秒
                    key_moments.append({
                        "time": estimated_time,
                        "suggested_danmaku": random.choice([
                            "重点来了！", "这就是经典", "笑死了", "太真实", "神评论"
                        ])
                    })
        
        except Exception as e:
            print(f"字幕分析出错: {e}")
        
        return key_moments

    def _create_preview_file(self, danmaku_data: List[Dict], output_path: str):
        """
        创建弹幕预览文件
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("弹幕预览\n")
            f.write("=" * 50 + "\n\n")
            
            for item in danmaku_data:
                time_str = f"{int(item['time']//60):02d}:{int(item['time']%60):02d}"
                f.write(f"[{time_str}] {item['text']} (类型: {item.get('category', 'unknown')})\n")
            
            f.write(f"\n总计: {len(danmaku_data)} 条弹幕\n")


def main():
    """
    主函数 - 演示用法
    """
    generator = JianyingDanmakuGenerator()
    
    # 检查是否有视频文件
    output_dir = "output"
    video_files = []
    
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            if file.endswith(('.mp4', '.avi', '.mov')):
                video_files.append(os.path.join(output_dir, file))
    
    if video_files:
        # 为找到的第一个视频生成弹幕
        video_path = video_files[0]
        print(f"为视频生成弹幕: {video_path}")
        
        # 查找对应的字幕文件
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        subtitle_files = [
            os.path.join(output_dir, f"{video_name}_chinese.srt"),
            os.path.join(output_dir, f"{video_name}_english.srt"),
        ]
        
        subtitle_file = None
        for srt_file in subtitle_files:
            if os.path.exists(srt_file):
                subtitle_file = srt_file
                break
        
        jianying_file, bilibili_file = generator.create_smart_danmaku_for_video(
            video_path, subtitle_file, output_dir
        )
        
        print(f"\n✅ 弹幕文件生成完成!")
        print(f"剪映弹幕文件: {jianying_file}")
        print(f"B站弹幕文件: {bilibili_file}")
        print(f"预览文件: {os.path.join(output_dir, f'{video_name}_danmaku_preview.txt')}")
        
    else:
        # 演示模式 - 生成示例弹幕
        print("演示模式: 生成示例弹幕文件")
        
        sample_danmaku = generator.generate_danmaku_data(
            video_duration_seconds=180,  # 3分钟视频
            density="medium"
        )
        
        os.makedirs(output_dir, exist_ok=True)
        jianying_file = os.path.join(output_dir, "sample_jianying_danmaku.json")
        bilibili_file = os.path.join(output_dir, "sample_bilibili_danmaku.xml")
        
        generator.create_jianying_danmaku_file(sample_danmaku, jianying_file)
        generator.create_bilibili_danmaku_file(sample_danmaku, bilibili_file)
        
        print(f"✅ 示例弹幕文件生成完成!")
        print(f"剪映弹幕文件: {jianying_file}")
        print(f"B站弹幕文件: {bilibili_file}")

    print("\n📝 使用说明:")
    print("1. 在剪映中导入视频后，选择'弹幕'功能")
    print("2. 选择'导入弹幕文件'，导入生成的JSON文件")
    print("3. 可以手动调整弹幕位置、颜色和时间")
    print("4. 预埋弹幕会让视频看起来更有互动感!")


if __name__ == "__main__":
    main() 