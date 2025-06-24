# 视频处理自动化系统 (Video Processing Automation System)

专为B站内容创作者设计的全自动视频处理工具，支持YouTube视频下载、智能字幕生成、AI翻译和专业视频制作。

## 🎯 核心功能

### 📹 视频处理
- **YouTube视频下载**: 支持多种质量选择，自动获取最佳格式
- **智能字幕提取**: 使用OpenAI Whisper模型，准确识别英文语音
- **AI翻译集成**: 支持Sider.AI等翻译服务，生成高质量中文翻译
- **双语字幕生成**: 自动生成中英双语字幕，支持ASS格式精确控制

### 🎨 视觉效果
- **专业字幕样式**: [白色字幕配置，中文22px，英文18px][[memory:585619162882853566]]
- **品牌水印**: [自动添加"董卓主演脱口秀"水印，右上角定位][[memory:585619162882853566]]
- **智能缩略图**: 自动生成吸引人的视频封面
- **弹幕效果**: 支持剪映弹幕导入，增强互动体验

### 📺 B站优化
- **内容风格适配**: 自动生成B站风格的标题和描述
- **标签优化**: 智能推荐热门标签
- **上传指导**: 提供完整的B站上传策略

## 🚀 快速开始

### 1. 环境设置
```bash
# 克隆项目
git clone https://github.com/Clairehou111/video-processor.git
cd video-processor

# 运行安装脚本
chmod +x setup.sh
./setup.sh
```

### 2. 一键处理视频
```bash
# 激活虚拟环境
source venv/bin/activate

# 运行主工作流程
python complete_bilibili_workflow.py
```

### 3. 输入YouTube链接
程序会提示输入YouTube视频链接，然后自动完成：
- 视频下载和质量优化
- 英文字幕提取
- 翻译提示生成
- 双语视频制作
- B站上传内容生成

## 📁 项目结构

```
video-processor/
├── complete_bilibili_workflow.py    # 🎯 主工作流程
├── subtitle_config.py               # ⚙️ 字幕配置模块
├── improved_subtitle_recognition.py # 🎤 语音识别
├── convert_srt_to_ass.py            # 📝 字幕格式转换
├── generate_thumbnail_with_faces.py # 🖼️ 缩略图生成
├── archive/                         # 📦 历史版本存档
├── output/                          # 📤 输出文件目录
└── requirements.txt                 # 📋 依赖列表
```

## 🎨 字幕配置标准

项目采用经过验证的最佳字幕配置：

- **中文字幕**: PingFang SC, 22px, 顶部显示 (MarginV=60)
- **英文字幕**: Arial, 18px, 底部显示 (MarginV=20)  
- **颜色编码**: 统一使用白色 `&Hffffff`
- **水印样式**: 右上角 "董卓主演脱口秀", 24px

## 🔧 高级功能

### 视频分段处理
```python
# 处理特定时间段
python complete_bilibili_workflow.py --start 0:45 --end 10:21
```

### 批量处理
```python
# 批量处理多个视频
python auto_video_processor.py
```

### 剪映集成
```python
# 生成剪映弹幕项目
python create_jianying_danmaku.py
```

## 📊 输出文件说明

每个处理的视频都会在 `output/` 目录下创建独立文件夹：

```
output/Video_Project_YYYYMMDD_HHMMSS/
├── final/
│   ├── *_bilingual.mp4           # 双语版本
│   └── *_chinese.mp4             # 中文版本
├── subtitles/
│   ├── bilingual.ass             # 双语字幕
│   ├── chinese.ass               # 中文字幕
│   └── *_english.srt             # 原始英文字幕
├── bilibili_thumbnail.jpg        # B站封面
├── bilibili_upload_content.md    # 上传内容
└── workflow_summary.md           # 处理摘要
```

## 🎯 B站上传优化

系统自动生成B站风格的内容：

- **吸引力标题**: 融合热点话题和情感元素
- **B站语言**: 使用"兄弟们"、"老铁们"等B站用户熟悉的表达
- **互动引导**: 包含点赞、投币、收藏引导
- **标签推荐**: 基于内容智能推荐热门标签

## 💡 使用技巧

1. **首次使用**: 推荐先用短视频测试完整流程
2. **翻译质量**: 使用Sider.AI等专业翻译服务获得最佳效果
3. **视频长度**: 建议处理10-15分钟的视频段落
4. **存储空间**: 确保有足够空间存储处理后的视频文件

## 🔍 故障排除

### 常见问题
- **字幕同步问题**: 检查时间戳转换配置
- **视频质量**: 调整FFmpeg编码参数
- **翻译准确性**: 使用专业翻译服务替代自动翻译

### 技术支持
- 查看 `COMPLETE_WORKFLOW_GUIDE.md` 获取详细说明
- 检查 `archive/` 目录中的历史版本
- 参考项目Wiki获取更多帮助

## 📈 版本历史

- **v2.0**: 完整B站工作流程，优化字幕配置
- **v1.5**: 添加双语字幕支持，改进翻译流程  
- **v1.0**: 基础视频处理和字幕生成功能

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目。请确保：
- 遵循现有代码风格
- 添加适当的测试
- 更新相关文档

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

**专为内容创作者打造，让视频制作更简单！** 🎬✨
