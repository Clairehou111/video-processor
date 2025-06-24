#!/bin/bash

echo "=== YouTube视频处理工具安装脚本 ==="

# 检查Python3是否存在
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未找到，请先安装 Python 3.8+"
    exit 1
fi

echo "✅ Python3 已找到: $(python3 --version)"

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🚀 激活虚拟环境..."
source venv/bin/activate

# 安装基础依赖
echo "📥 安装基础依赖..."
pip install yt-dlp opencv-python moviepy pillow numpy requests

# 从GitHub安装Whisper
echo "🎤 安装Whisper语音识别..."
pip install git+https://github.com/openai/whisper.git

# 安装翻译库
echo "🌐 安装翻译库..."
pip install googletrans==3.1.0a0

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法："
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 运行主程序: python video_processor.py"
echo "3. 或运行测试: python quick_test.py"
echo "" 