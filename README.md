# Video Processor

Python automation toolkit for turning YouTube or local videos into Bilibili-ready publishing packages. The project focuses on video download, speech-to-text subtitles, Sider-assisted Chinese translation, ASS subtitle rendering, danmaku assets, thumbnails, and upload copy.

## What It Does

- Downloads high-quality source videos with `yt-dlp`.
- Extracts English subtitles with OpenAI Whisper.
- Generates translation prompts for manual Sider.AI translation.
- Produces bilingual and Chinese-only videos with FFmpeg-rendered subtitles.
- Creates Bilibili thumbnails, upload metadata, summaries, and checklists.
- Generates danmaku and Jianying/CapCut helper assets for editing workflows.
- Supports local video post-processing when the source video already exists.

## Repository Layout

```text
video-processor/
├── complete_bilibili_workflow.py      # End-to-end URL to Bilibili package flow
├── complete_video_automation.py       # Stateful interactive workflow with resume support
├── optimized_video_automation.py      # Retry/cache/segment optimized workflow
├── auto_video_processor.py            # Local video processor
├── subtitle_config.py                 # Shared subtitle and watermark style config
├── convert_srt_to_ass.py              # Bilingual SRT to ASS conversion helper
├── create_jianying_danmaku.py         # Jianying/CapCut danmaku generation
├── advanced_jianying_danmaku.py       # Advanced danmaku generator
├── generate_thumbnail_with_faces.py   # Bilibili thumbnail generator
├── cleanup_scripts.py                 # Archive and cleanup utility
├── check_status.py                    # Project status checker
├── output/                            # Generated project packages
├── COMPLETE_WORKFLOW_GUIDE.md         # Chinese detailed Bilibili workflow guide
├── PROJECT_STRUCTURE_GUIDE.md         # Chinese output structure guide
└── UP主自动化工具使用指南.md            # Chinese creator workflow guide
```

## Requirements

- Python 3.8+
- FFmpeg available on `PATH`
- macOS fonts such as PingFang SC for the current subtitle style defaults
- Network access for YouTube downloads and first-time model downloads
- Python packages from `requirements.txt`

Install dependencies:

```bash
cd /Users/clairehou/IdeaProjects/video-processor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Install FFmpeg if needed:

```bash
brew install ffmpeg
```

## Main Workflows

### 1. Full Bilibili Package

Use this when starting from a YouTube URL and you want the complete output package.

```bash
python complete_bilibili_workflow.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

The script:

1. Creates a timestamped project directory under `output/`.
2. Downloads the source video.
3. Extracts English SRT subtitles with Whisper.
4. Generates `translation_prompt.txt`.
5. Waits for `subtitles/chinese_translation.srt`.
6. Generates bilingual and Chinese-only final videos.
7. Generates thumbnail, upload copy, and workflow summary.

### 2. Stateful Interactive Workflow

Use this when you want resumable projects and explicit translation handoff.

```bash
python complete_video_automation.py
python complete_video_automation.py --list
python complete_video_automation.py --finalize
python complete_video_automation.py --continue output/<project_dir>
```

Project state is saved in each project directory as `automation_state.json`. Projects waiting for translation remain in `waiting_translation` until `chinese_translation.srt` is added and the finalize command runs.

### 3. Optimized Workflow

Use this for longer videos or unreliable network conditions.

```bash
python optimized_video_automation.py
python optimized_video_automation.py --finalize
```

This workflow adds retry behavior, cached video information, optional segment processing, and a cached Whisper model.

### 4. Local Video Processing

Use this when a video file already exists locally.

```bash
python auto_video_processor.py /path/to/video.mp4
python auto_video_processor.py --batch
```

The local processor searches for matching subtitles, builds dual subtitles and danmaku data, then renders processed outputs for Bilibili-style publishing.

## Translation Handoff

Most workflows intentionally keep Chinese translation as a manual step:

1. Open `translation_prompt.txt`.
2. Use Sider.AI or another translation tool to create Chinese SRT text.
3. Save the result as `subtitles/chinese_translation.srt`.
4. Run the workflow finalization command.

The finalization step expects valid SRT timing and numbering. Keep timestamps unchanged unless you are intentionally retiming the video.

## Output Structure

A typical project package looks like this:

```text
output/Video_Project_YYYYMMDD_HHMMSS/
├── <source_video>.mp4
├── subtitles/
│   ├── <video>_english.srt
│   ├── chinese_translation.srt
│   ├── bilingual.ass
│   └── chinese.ass
├── final/
│   ├── <video>_bilingual.mp4
│   └── <video>_chinese.mp4
├── temp/
├── automation_state.json
├── bilibili_metadata.json
├── bilibili_thumbnail.jpg
├── bilibili_upload_content.md
├── translation_prompt.txt
└── workflow_summary.md
```

## Subtitle Standards

Current shared defaults are defined in `subtitle_config.py`:

- Chinese subtitles: PingFang SC, 22px, white text, black outline.
- English subtitles: Arial, 18px, white text, black outline.
- Watermark: `董卓主演脱口秀`, positioned in the upper-right corner.
- Bilingual layout: Chinese above English, both bottom-aligned with separate margins.

## Supporting Utilities

- `convert_srt_to_ass.py` converts an existing bilingual SRT file to ASS.
- `generate_thumbnail_with_faces.py` creates enhanced Bilibili thumbnails.
- `create_jianying_danmaku.py` and `advanced_jianying_danmaku.py` generate Jianying/CapCut danmaku assets.
- `preview_danmaku_effects.py` previews danmaku styles.
- `check_status.py` reports current project processing state.
- `cleanup_scripts.py` archives or cleans generated artifacts.
- `quick_test.py` runs a small interactive smoke test against available output videos.

## Operational Notes

- Generated videos can be large; monitor disk usage under `output/`.
- Whisper downloads models on first use and may require significant CPU time.
- YouTube download quality depends on availability, network conditions, and `yt-dlp` support.
- FFmpeg rendering is CPU-intensive and may take several minutes per video.
- Some older or topic-specific scripts are kept as workflow examples and may contain hardcoded sample paths.

## Existing Chinese Guides

- `COMPLETE_WORKFLOW_GUIDE.md` documents the full Bilibili processing pipeline.
- `PROJECT_STRUCTURE_GUIDE.md` documents project output structure and state files.
- `UP主自动化工具使用指南.md` documents creator-oriented prompt and danmaku workflows.
- `剪映弹幕使用指南.md` documents Jianying/CapCut danmaku usage.
