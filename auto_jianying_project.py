#!/usr/bin/env python3
"""
自动剪映项目生成器
创建包含视频和弹幕的完整剪映项目文件
"""

import json
import os
import uuid
import time
from typing import Dict, List

class JianyingProjectGenerator:
    def __init__(self):
        self.project_id = str(uuid.uuid4())
        self.current_time = int(time.time() * 1000000)  # 微秒时间戳
        
    def create_project_structure(self, video_path: str, danmaku_file: str, 
                               output_dir: str = "output") -> str:
        """创建完整的剪映项目结构"""
        
        # 创建项目目录
        project_name = f"trump_video_with_danmaku_{int(time.time())}"
        project_dir = os.path.join(output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        # 获取视频信息
        import cv2
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = int((frame_count / fps) * 1000000) if fps > 0 else 180000000
        cap.release()
        
        # 读取弹幕数据
        with open(danmaku_file, 'r', encoding='utf-8') as f:
            danmaku_data = json.load(f)
        
        # 创建剪映项目JSON
        project_data = self._create_project_json(
            video_path, danmaku_data, duration, width, height, fps
        )
        
        # 保存项目文件
        project_file = os.path.join(project_dir, "draft_content.json")
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        
        # 创建说明文件
        self._create_instructions(project_dir, video_path, danmaku_file)
        
        print(f"✅ 剪映项目已创建: {project_dir}")
        print(f"📱 项目文件: {project_file}")
        
        return project_dir
    
    def _create_project_json(self, video_path: str, danmaku_data: Dict, 
                           duration: int, width: int, height: int, fps: float) -> Dict:
        """创建剪映项目的JSON结构"""
        
        # 基础项目结构
        project = {
            "content": {
                "canvas_config": {
                    "height": 1920,
                    "width": 1080,
                    "ratio": "9:16"
                },
                "color_space": 1,
                "fps": 30.0,
                "free_render_index": 0,
                "materials": {
                    "texts": [],
                    "videos": [
                        {
                            "id": str(uuid.uuid4()),
                            "path": video_path,
                            "type": "video",
                            "duration": duration,
                            "width": width,
                            "height": height,
                            "fps": fps
                        }
                    ],
                    "audios": [],
                    "effects": []
                },
                "tracks": []
            },
            "create_time": self.current_time,
            "draft_fold_path": "",
            "draft_id": self.project_id,
            "draft_name": "Trump Video with Danmaku",
            "draft_root_path": "",
            "duration": duration,
            "extra_info": "",
            "fps": 30.0,
            "id": self.project_id,
            "new_version": "12.8.0",
            "platform": "mac",
            "resolution": "1080*1920",
            "update_time": self.current_time,
            "version": 1
        }
        
        # 添加视频轨道
        video_track = {
            "attribute": 0,
            "flag": 0,
            "id": str(uuid.uuid4()),
            "segments": [
                {
                    "cartoon": False,
                    "clip": {
                        "alpha": 1.0,
                        "flip": {"horizontal": False, "vertical": False},
                        "rotation": 0.0,
                        "scale": {"x": 1.0, "y": 1.0},
                        "transform": {"x": 0.0, "y": 0.0}
                    },
                    "common_keyframes": [],
                    "enable_adjust": True,
                    "enable_color_curves": True,
                    "enable_color_match_adjust": False,
                    "enable_color_wheels": True,
                    "enable_lut": False,
                    "enable_smart_color_adjust": False,
                    "extra_material_refs": [],
                    "group_id": "",
                    "hdr_settings": None,
                    "id": str(uuid.uuid4()),
                    "intensifies_audio": False,
                    "is_placeholder": False,
                    "is_tone_modify": False,
                    "keyframe_refs": [],
                    "last_nonzero_volume": 1.0,
                    "material_id": project["content"]["materials"]["videos"][0]["id"],
                    "render_index": 0,
                    "reverse": False,
                    "source_timerange": {
                        "duration": duration,
                        "start": 0
                    },
                    "speed": 1.0,
                    "target_timerange": {
                        "duration": duration,
                        "start": 0
                    },
                    "template_id": "",
                    "template_scene": "default",
                    "track_attribute": 0,
                    "track_render_index": 0,
                    "uniform_scale": None,
                    "visible": True,
                    "volume": 1.0
                }
            ],
            "type": "video"
        }
        
        project["content"]["tracks"].append(video_track)
        
        # 添加弹幕轨道
        text_track = self._create_danmaku_track(danmaku_data)
        project["content"]["tracks"].append(text_track)
        
        return project
    
    def _create_danmaku_track(self, danmaku_data: Dict) -> Dict:
        """创建弹幕轨道"""
        
        text_segments = []
        
        for i, danmaku in enumerate(danmaku_data["danmaku_list"]):
            # 计算弹幕显示时长（3秒）
            start_time = danmaku["time"] * 1000  # 转为微秒
            duration = 3000000  # 3秒
            
            # 创建文本材料
            color_int = int(danmaku["color"]) if isinstance(danmaku["color"], str) else danmaku["color"]
            text_material = {
                "id": str(uuid.uuid4()),
                "type": "text",
                "text": danmaku["text"],
                "font_size": danmaku["fontsize"],
                "color": f"#{color_int:06x}",
                "alignment": "center"
            }
            
            # 创建文本片段
            text_segment = {
                "id": str(uuid.uuid4()),
                "material_id": text_material["id"],
                "target_timerange": {
                    "start": start_time,
                    "duration": duration
                },
                "source_timerange": {
                    "start": 0,
                    "duration": duration
                },
                "extra_material_refs": [],
                "animations": [
                    {
                        "id": str(uuid.uuid4()),
                        "type": "scroll_right" if danmaku["mode"] == 1 else "fade_in",
                        "duration": duration
                    }
                ],
                "render_index": i + 1,
                "visible": True
            }
            
            text_segments.append(text_segment)
        
        # 创建文本轨道
        text_track = {
            "attribute": 0,
            "flag": 0,
            "id": str(uuid.uuid4()),
            "segments": text_segments,
            "type": "text"
        }
        
        return text_track
    
    def _create_instructions(self, project_dir: str, video_path: str, danmaku_file: str):
        """创建使用说明"""
        
        instructions = f"""
# 🎬 剪映项目使用说明

## 📁 项目信息
- 项目名称: Trump Video with Danmaku
- 视频文件: {os.path.basename(video_path)}
- 弹幕文件: {os.path.basename(danmaku_file)}
- 创建时间: {time.strftime('%Y-%m-%d %H:%M:%S')}

## 📱 导入步骤

### 方法1: 直接导入项目文件
1. 打开剪映APP
2. 选择"导入项目"
3. 选择 draft_content.json 文件
4. 系统会自动加载视频和弹幕

### 方法2: 手动创建
1. 新建项目，导入视频文件
2. 添加文字效果
3. 逐个添加弹幕内容

## ⚙️ 项目设置
- 分辨率: 1080x1920 (竖屏)
- 帧率: 30fps
- 弹幕显示时长: 3秒
- 弹幕动画: 滚动/淡入效果

## 🎨 后期调整建议
1. 调整弹幕位置避免遮挡重要内容
2. 微调弹幕颜色和大小
3. 根据视频节奏调整弹幕时间
4. 添加背景音乐增强效果

## 📤 导出设置
- 推荐分辨率: 1080p
- 推荐格式: MP4
- 推荐码率: 高质量
"""
        
        with open(os.path.join(project_dir, "README.md"), 'w', encoding='utf-8') as f:
            f.write(instructions)


def main():
    """主函数"""
    generator = JianyingProjectGenerator()
    
    # 使用之前生成的文件
    video_path = "/Users/admin/IdeaProjects/video-processor/output/_jOTww0E0b4_Trump_seen_in_new_clip_released_by_filmmaker_following_Jan_6_committee_subpoena/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena.mp4"
    danmaku_file = "output/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena_jan6_special_danmaku.json"
    
    if os.path.exists(video_path) and os.path.exists(danmaku_file):
        project_dir = generator.create_project_structure(video_path, danmaku_file)
        
        print("\n🎉 项目创建完成！")
        print("\n📋 下一步操作:")
        print("1. 打开剪映APP")
        print("2. 选择'导入项目'")
        print(f"3. 导入 {project_dir}/draft_content.json")
        print("4. 调整弹幕效果")
        print("5. 导出完整视频")
        
    else:
        print("❌ 视频文件或弹幕文件不存在")
        print(f"视频路径: {video_path}")
        print(f"弹幕文件: {danmaku_file}")


if __name__ == "__main__":
    main() 