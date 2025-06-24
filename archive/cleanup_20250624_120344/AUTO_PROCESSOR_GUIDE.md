# 🤖 自动化视频处理器使用指南

## 🎯 功能概述
一键自动处理视频，输出B站就绪的完整版本，包含：
- ✅ 双语字幕（英文+中文）
- ✅ 智能弹幕生成
- ✅ HD水印（右上角）
- ✅ B站优化编码

## 🚀 使用方法

### 方法1：指定视频文件
```bash
python auto_video_processor.py <视频文件路径>
```

### 方法2：交互式选择
```bash
python auto_video_processor.py
```
会自动扫描output目录下的所有视频文件，让你选择要处理的视频。

### 方法3：批量处理
```bash
python auto_video_processor.py --batch
```
自动处理所有未处理的视频文件。

## 📋 处理流程

1. **🔍 自动检测** - 扫描并匹配字幕文件
2. **📝 生成双语字幕** - 合并英文和中文字幕
3. **🎭 智能弹幕** - 根据视频时长自动生成政治评论弹幕
4. **🎬 视频合成** - 添加字幕、弹幕、水印
5. **📤 输出结果** - 生成B站版本和完整版本

## 📁 输出结构

每个视频会创建独立的项目文件夹：
```
output/
├── VideoName_processed/
│   ├── original_VideoName.mp4          # 原视频备份
│   ├── english_subtitles.srt           # 英文字幕
│   ├── chinese_subtitles.srt           # 中文字幕  
│   ├── dual_subtitles.srt              # 双语字幕
│   ├── danmaku.json                    # 弹幕数据
│   ├── danmaku.ass                     # 弹幕ASS格式
│   ├── VideoName_bilibili_ready.mp4    # 🎯 B站版本 (推荐上传)
│   └── VideoName_complete.mp4          # 完整版本 (含预置弹幕)
```

## ⚡ 快速开始

### 示例1：处理Trump Jan 6视频
```bash
# 自动处理
python auto_video_processor.py "output/trump_jan6_complete_project/Trump seen in new clip released by filmmaker following Jan 6 committee subpoena.mp4"

# 输出
🎬 开始处理视频: Trump seen in new clip released by filmmaker following Jan 6 committee subpoena.mp4
⏱️  视频时长: 67.7秒  
🔍 查找字幕文件...
✅ 字幕文件已找到
📝 生成双语字幕...
🎭 生成智能弹幕...
🎬 生成B站版本...
🎬 生成完整版本...

🎉 处理完成！
📁 项目目录: output/Trump_seen_in_new_clip_released_by_filmmaker_following_Jan_6_committee_subpoena_processed
📺 B站版本: Trump seen in new clip released by filmmaker following Jan 6 committee subpoena_bilibili_ready.mp4 (2.6MB)
🎬 完整版本: Trump seen in new clip released by filmmaker following Jan 6 committee subpoena_complete.mp4
```

## 🔧 自动化特性

### 🔍 智能字幕匹配
自动查找匹配的英文和中文字幕文件：
- 支持多种命名格式：`*english*.srt`, `*chinese*.srt`, `*sider*.srt`
- 自动复制到项目目录
- 优先使用Sider翻译的高质量字幕

### 🎭 智能弹幕生成
根据视频时长自动生成适量弹幕：
- 短视频（<30s）：3-4条弹幕
- 中等视频（30-120s）：4-6条弹幕  
- 长视频（>120s）：6-8条弹幕

### 🎨 专业编码设置
- **视频编码**：H.264 High Profile, CRF 20
- **音频编码**：AAC 128kbps
- **字幕样式**：18px白字黑边，最佳可读性
- **水印位置**：右上角，20px边距

## 📊 输出质量对比

| 参数 | 自动处理版本 | 手动处理 |
|------|-------------|----------|
| **处理时间** | 1-2分钟 | 10-15分钟 |
| **质量一致性** | ✅ 标准化 | ❓ 可能不一致 |
| **文件管理** | ✅ 自动整理 | ❌ 需手动管理 |
| **批量处理** | ✅ 支持 | ❌ 逐个处理 |

## 🎯 适用场景

### ✅ 最适合
- 政治评论视频
- 双语字幕需求
- 批量视频处理
- B站上传准备

### ⚠️ 注意事项
- 需要预先准备好英文和中文字幕文件
- 确保`bilibili_hd_watermark.png`水印文件存在
- 视频文件应在output目录及其子目录中

## 🔧 故障排除

### 问题1：未找到字幕文件
**解决方案**：
1. 确保字幕文件在output目录下
2. 检查文件命名是否包含`english`、`chinese`或`sider`关键词
3. 手动复制字幕文件到正确位置

### 问题2：水印文件缺失
**解决方案**：
```bash
# 确保水印文件存在
ls output/bilibili_hd_watermark.png
```

### 问题3：FFmpeg错误
**解决方案**：
1. 确保FFmpeg已安装且在PATH中
2. 检查视频文件是否损坏
3. 确保有足够的磁盘空间

## 💡 使用技巧

### 技巧1：自定义弹幕
编辑脚本中的`political_templates`数组来自定义弹幕内容。

### 技巧2：批量处理
将所有需要处理的视频放在output目录下，使用`--batch`参数一次性处理。

### 技巧3：快速预览
处理完成后，B站版本直接可上传，完整版本可用于效果预览。

---

## 📞 支持

如有问题，请检查：
1. 视频文件格式是否支持（mp4, avi, mov, mkv）
2. 字幕文件编码是否为UTF-8
3. FFmpeg是否正确安装

**现在你只需要一条命令就能处理任何视频！** 🎉 