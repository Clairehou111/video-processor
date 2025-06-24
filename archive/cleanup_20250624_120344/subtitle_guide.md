# 中文字幕使用指南

本项目生成的中文字幕为SRT格式，可以在各种播放器中使用。以下是详细的使用方法：

## 📺 常用播放器字幕使用方法

### 1. VLC播放器 (推荐)
**步骤：**
1. 打开VLC播放器
2. 打开视频文件 (`*_with_watermark.mp4`)
3. 菜单栏 → 字幕 → 添加字幕文件
4. 选择对应的 `*_chinese.srt` 文件
5. 字幕会自动显示

**快捷键：**
- `V` - 切换字幕显示/隐藏
- `H` - 延迟字幕
- `G` - 提前字幕

### 2. macOS QuickTime Player
**步骤：**
1. 确保SRT文件与视频文件在同一目录
2. 将SRT文件重命名为与视频文件相同的名称（保持.srt扩展名）
3. 用QuickTime打开视频，字幕会自动加载

**示例：**
```
视频文件: video_with_watermark.mp4
字幕文件: video_with_watermark.srt
```

### 3. Windows Media Player
**步骤：**
1. 确保SRT文件与视频文件在同一目录，且文件名相同
2. 安装字幕插件（如DirectVobSub）
3. 播放视频时字幕会自动显示

### 4. PotPlayer (Windows)
**步骤：**
1. 播放视频
2. 右键 → 字幕 → 选择字幕
3. 选择SRT文件

### 5. IINA (macOS)
**步骤：**
1. 播放视频
2. 右键 → 字幕 → 选择字幕文件
3. 选择SRT文件

### 6. 在线播放器
如果您想在网页中播放带字幕的视频，可以：
1. 将视频上传到支持字幕的平台（如YouTube、Vimeo）
2. 上传对应的SRT字幕文件

## 🛠️ 字幕文件格式说明

生成的SRT文件格式如下：
```
1
00:00:00,000 --> 00:00:03,160
[英文] Now, I have to say, a slightly surprised appears more

2
00:00:03,160 --> 00:00:04,960
convinced 到 你 在 it, because he, 我 don't know if 你 know,

3
00:00:04,960 --> 00:00:07,360
[英文] he's a big Donald Trump supporter.
```

**格式说明：**
- 第一行：字幕序号
- 第二行：时间码（开始时间 --> 结束时间）
- 第三行：字幕文本
- 空行：分隔每个字幕段

## 📝 字幕编辑和改进

### 手动编辑字幕
您可以用任何文本编辑器打开SRT文件进行编辑：
```bash
# macOS/Linux
nano output/video_chinese.srt
vim output/video_chinese.srt

# 或使用图形界面编辑器
open -a TextEdit output/video_chinese.srt
```

### 专业字幕编辑软件
- **Subtitle Edit** (免费) - Windows/Linux
- **Aegisub** (免费) - 跨平台
- **Subtitle Workshop** (免费) - Windows

### 改进翻译质量
当前项目使用简单词典翻译，建议：
1. 使用专业翻译软件重新翻译
2. 人工校对和润色
3. 考虑上下文和语境

## 🔧 常见问题解决

### 字幕不显示
1. 确保字幕文件名正确
2. 检查字幕编码是否为UTF-8
3. 尝试重新命名字幕文件与视频文件名一致

### 字幕时间不同步
1. 使用播放器的字幕延迟功能
2. 用字幕编辑软件调整时间码

### 字幕乱码
1. 确保SRT文件保存为UTF-8编码
2. 使用支持UTF-8的播放器

## 📱 移动设备字幕

### iOS设备
- **VLC for Mobile** - 支持外挂字幕
- **Infuse** - 自动识别同名SRT文件

### Android设备
- **MX Player** - 支持多种字幕格式
- **VLC for Android** - 功能强大的播放器

## 💡 提示和技巧

1. **文件命名**: 保持视频和字幕文件名一致，便于自动加载
2. **备份**: 保留原始SRT文件，便于后续编辑
3. **格式转换**: 可以将SRT转换为其他字幕格式（ASS、VTT等）
4. **多语言**: 可以生成多个语言版本的字幕文件

## 🚀 进阶功能

如果您想要更高级的字幕功能，可以考虑：
1. 集成在线翻译API提高翻译质量
2. 添加字幕样式设置（颜色、字体、位置）
3. 支持双语字幕显示
4. 自动字幕时间校正 