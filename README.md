# YouTube视频处理工具

这是一个Python工具，可以从YouTube下载英文视频，生成中文字幕，并添加水印。

## 功能特点

1. **YouTube视频下载**: 使用yt-dlp下载指定质量的YouTube视频
2. **语音识别**: 使用OpenAI Whisper模型提取视频中的英文语音
3. **中文翻译**: 使用内置词典进行基础英中翻译（可扩展为在线翻译API）
4. **水印添加**: 在视频上添加自定义文字水印
5. **字幕嵌入**: 将中文字幕直接嵌入到视频中
6. **SRT字幕文件**: 同时生成独立的SRT字幕文件

## 快速开始

### 1. 运行安装脚本
```bash
chmod +x setup.sh
./setup.sh
```

### 2. 手动安装（如果安装脚本失败）
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install yt-dlp opencv-python moviepy pillow numpy requests
pip install git+https://github.com/openai/whisper.git
```

## 使用方法

### 方式1: 演示模式（推荐第一次使用）
```bash
source venv/bin/activate
python demo.py
```

### 方式2: 完整功能脚本
```bash
source venv/bin/activate
python video_processor.py
```

### 方式3: 快速测试
```bash
source venv/bin/activate
python quick_test.py
```

### 方式4: 直接调用API
```python
from video_processor import VideoProcessor

processor = VideoProcessor()
result = processor.process_video(
    youtube_url="https://www.youtube.com/watch?v=VIDEO_ID",
    watermark_text="我的水印",
    quality="720p"
)
```

## 输出文件

所有处理后的文件都会保存在 `output/` 目录下：
- 原始下载的视频
- 处理后的视频（带字幕和水印）
- SRT格式的中文字幕文件
- 水印图片文件

## 配置选项

- **视频质量**: 支持 `480p`, `720p`, `1080p` 等
- **Whisper模型**: 支持 `tiny`, `base`, `small`, `medium`, `large`
- **水印位置**: 默认在右上角，可修改代码调整
- **字幕样式**: 可修改字体大小、颜色、描边等

## 翻译功能说明

当前版本使用内置词典进行基础翻译。对于更准确的翻译，建议：

1. **在线翻译API**: 集成Google翻译、百度翻译或其他服务
2. **AI翻译模型**: 使用本地翻译模型
3. **手动编辑**: 处理后手动编辑SRT文件

可以修改 `translate_to_chinese_simple` 函数来集成更好的翻译服务。

## 项目结构

```
video-processor/
├── video_processor.py    # 主要处理脚本
├── demo.py              # 演示脚本
├── quick_test.py        # 快速测试脚本
├── setup.sh             # 安装脚本
├── requirements.txt     # 依赖列表
├── README.md           # 项目说明
├── venv/               # 虚拟环境
└── output/             # 输出目录
```

## 注意事项

1. 首次运行会下载Whisper模型，可能需要一些时间
2. 视频处理时间取决于视频长度和电脑性能
3. 需要稳定的网络连接来下载视频
4. 请确保有足够的磁盘空间存储视频文件
5. 当前翻译功能较基础，建议用于简单内容

## 故障排除

### 常见问题

1. **依赖安装失败**: 
   - 确保使用Python 3.8+
   - 尝试手动安装各个依赖

2. **YouTube下载失败**:
   - 检查网络连接
   - 确认视频URL是否有效
   - 某些地区可能需要VPN

3. **Whisper模型下载慢**:
   - 首次使用会自动下载模型
   - 可以手动下载模型文件

4. **视频处理失败**:
   - 检查视频格式是否支持
   - 确保有足够的内存和存储空间

### 获取帮助

如果遇到问题，请检查：
1. 控制台输出的错误信息
2. 虚拟环境是否正确激活
3. 所有依赖是否成功安装

## 系统要求

- Python 3.8+
- macOS/Linux/Windows
- 至少2GB可用内存
- 稳定的网络连接
- 足够的磁盘空间（取决于视频大小）

## 扩展功能

项目设计允许轻松扩展：
- 集成更好的翻译API
- 添加更多视频效果
- 支持批量处理
- 添加GUI界面
- 支持更多视频源 