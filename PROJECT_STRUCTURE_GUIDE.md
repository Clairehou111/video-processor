# 视频处理项目目录结构指南

## 📁 整体目录架构

```
video-processor/
├── output/                          # 主输出目录
│   ├── 视频标题1_20240623_143022/   # 项目目录1（带时间戳）
│   ├── 视频标题2_20240623_150815/   # 项目目录2
│   └── ...
├── complete_video_automation.py     # 主自动化脚本
├── COMPLETE_TRANSLATION_GUIDE.md   # 翻译指南
└── 其他脚本文件...
```

## 🎯 单个项目目录结构

每个视频处理项目都有独立的目录，包含完整的处理文件：

```
Ted_Cruz_Tucker_Carlson_Battle_20240623_143022/
├── 📹 原始视频文件
│   └── Ted Cruz & Tucker Carlson Battle Over Iran While Trump Enters His Decorating Era ｜ The Daily Show.mp4
├── 📂 subtitles/                    # 字幕文件目录
│   ├── 📝 *_english.srt            # 英文字幕（Whisper提取）
│   └── 📝 chinese_translation.srt   # 中文翻译字幕
├── 📂 final/                        # 最终输出目录
│   └── 🎬 *_bilingual_final.mp4    # 最终双语视频
├── 📖 translation_prompt.txt        # 翻译提示词
├── ⚙️ automation_state.json        # 处理状态文件
└── ⚙️ bilibili_metadata.json       # B站上传元数据
```

## 📋 文件详细说明

### 🎬 视频文件
- **原始视频**: 从YouTube下载的高质量视频（VP9/H.264格式）
- **最终视频**: 添加双语字幕和水印的成品视频

### 📝 字幕文件目录 (`subtitles/`)
- **英文字幕**: Whisper自动提取的英文SRT字幕
- **中文翻译**: 人工翻译的中文SRT字幕
- **命名规范**: `视频名_语言.srt`

### 📖 翻译提示词 (`translation_prompt.txt`)
包含：
- 专业翻译指南
- 所有英文字幕内容
- 格式要求和示例
- 下一步操作指导

### ⚙️ 状态文件 (`automation_state.json`)
```json
{
  "video_path": "项目目录/视频文件.mp4",
  "video_title": "视频标题",
  "english_srt": "subtitles/英文字幕.srt",
  "translation_file": "subtitles/chinese_translation.srt",
  "project_dir": "完整项目路径",
  "status": "waiting_translation"  // 或 "completed"
}
```

### ⚙️ B站元数据 (`bilibili_metadata.json`)
包含上传B站所需的所有信息：
- 优化的标题
- 相关标签
- 分类信息
- 详细简介

## 🔄 工作流程与目录

### 阶段1: 项目初始化
```bash
python complete_video_automation.py
```
1. **创建项目目录**: 基于视频标题+时间戳
2. **下载视频**: 保存到项目根目录
3. **提取字幕**: 保存到 `subtitles/` 目录
4. **生成提示词**: 保存翻译指导文件

### 阶段2: 翻译阶段
**人工操作**:
1. 阅读 `translation_prompt.txt`
2. 完成翻译并保存到 `subtitles/chinese_translation.srt`

### 阶段3: 视频生成
```bash
python complete_video_automation.py --finalize
```
1. **读取状态**: 从 `automation_state.json`
2. **烧制视频**: 生成到 `final/` 目录
3. **生成元数据**: B站上传信息

## 🛠️ 项目管理命令

### 列出所有项目
```bash
python complete_video_automation.py --list
```
显示所有项目的状态和进度

### 继续指定项目
```bash
python complete_video_automation.py --continue output/项目目录名
```
完成指定项目的处理

### 自动继续最新项目
```bash
python complete_video_automation.py --finalize
```
自动找到最新的未完成项目并继续

## 📊 目录优势

### 1. 项目隔离
- 每个视频独立目录，避免文件混乱
- 支持同时处理多个视频项目
- 便于项目归档和管理

### 2. 状态管理
- 每个项目有独立的状态文件
- 支持中断恢复和批量处理
- 清晰的进度追踪

### 3. 文件组织
- 逻辑清晰的目录结构
- 便于查找和维护
- 支持版本控制和备份

### 4. 扩展性
- 易于添加新的处理步骤
- 支持自定义输出格式
- 便于集成到其他工具链

## 🔍 项目状态说明

### waiting_translation
- 视频已下载，字幕已提取
- 等待人工翻译完成
- 需要运行 `--finalize` 完成处理

### completed
- 所有处理步骤已完成
- 最终视频已生成
- 可以直接上传到平台

## 💡 最佳实践

### 目录命名
- 自动生成安全的目录名（去除特殊字符）
- 包含时间戳避免重复
- 限制长度便于管理

### 文件管理
- 定期清理过期项目
- 备份重要的翻译文件
- 使用版本控制管理脚本

### 工作流程
- 批量下载多个视频
- 集中完成翻译工作
- 批量生成最终视频

---

这种目录结构设计确保了每个视频项目的完整性和可追踪性，大大提高了批量处理的效率和项目管理的便利性。 