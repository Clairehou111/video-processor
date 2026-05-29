# Video Processor Design

## Purpose

`video-processor` is a desktop-oriented video production automation toolkit. It converts a source video into a structured publishing package containing final videos, subtitles, danmaku assets, thumbnails, upload text, metadata, and workflow state.

The design prioritizes practical creator workflows over a fully automated black box. Human translation and review remain explicit steps because subtitle style, cultural localization, and platform compliance need manual judgment.

## System Context

```text
YouTube URL or local video
        |
        v
Video acquisition
        |
        v
Audio/subtitle extraction
        |
        v
Translation prompt and manual Chinese SRT
        |
        v
ASS subtitle generation
        |
        v
FFmpeg rendering
        |
        v
Bilibili/Jianying publishing package
```

External dependencies:

- `yt-dlp` downloads source videos and metadata.
- `ffmpeg` extracts audio and renders final video files.
- `openai-whisper` performs English speech-to-text transcription.
- `opencv-python`, `pillow`, and `numpy` support frame extraction and thumbnail generation.
- Sider.AI or another external translator provides manual Chinese subtitle translation.
- Jianying/CapCut consumes generated danmaku or editing helper files.

## Architecture

The project is organized as a script-based pipeline. Each script owns one workflow or utility responsibility instead of sharing a large application framework.

```text
Workflow scripts
├── complete_bilibili_workflow.py
├── complete_video_automation.py
├── optimized_video_automation.py
└── auto_video_processor.py

Shared and helper scripts
├── subtitle_config.py
├── convert_srt_to_ass.py
├── generate_thumbnail_with_faces.py
├── create_jianying_danmaku.py
├── advanced_jianying_danmaku.py
├── check_status.py
└── cleanup_scripts.py

Generated state and artifacts
└── output/<project>/
```

## Core Components

### Video Acquisition

Responsible scripts:

- `complete_bilibili_workflow.py`
- `complete_video_automation.py`
- `optimized_video_automation.py`

Responsibilities:

- Accept a YouTube URL.
- Select high-quality video and audio formats.
- Download the source video into a project directory.
- Save metadata required for title, description, and project tracking.
- Optionally process only a segment of the source video.

Design notes:

- The optimized workflow adds retry and caching behavior for unstable downloads.
- The complete workflow favors a single guided run from URL to publishing package.

### Transcription

Responsible scripts:

- `complete_bilibili_workflow.py`
- `complete_video_automation.py`
- `optimized_video_automation.py`

Responsibilities:

- Extract audio from the source video when needed.
- Run Whisper transcription.
- Write English subtitles as SRT.
- Preserve subtitle timing for later translation and rendering.

Design notes:

- Whisper model loading is a runtime concern and may download model files on first run.
- The generated English SRT is treated as the timing source of truth.

### Translation Handoff

Responsible scripts:

- `complete_bilibili_workflow.py`
- `complete_video_automation.py`
- `optimized_video_automation.py`

Responsibilities:

- Generate `translation_prompt.txt`.
- Instruct the user to create `subtitles/chinese_translation.srt`.
- Pause or mark state as `waiting_translation`.
- Resume rendering only after the Chinese subtitle file exists.

Design notes:

- Translation is intentionally manual to preserve tone, humor, and cultural adaptation.
- The Chinese SRT should keep the English SRT timing structure unless retiming is deliberate.

### Subtitle Styling

Responsible scripts:

- `subtitle_config.py`
- `convert_srt_to_ass.py`
- workflow scripts that create ASS files

Responsibilities:

- Define Chinese, English, and watermark styling.
- Convert subtitle timing and text into ASS events.
- Maintain a consistent bilingual layout.

Current style contract:

- Chinese: PingFang SC, 22px.
- English: Arial, 18px.
- Watermark: `董卓主演脱口秀`.
- Output: ASS subtitles rendered by FFmpeg.

### Video Rendering

Responsible scripts:

- `complete_bilibili_workflow.py`
- `complete_video_automation.py`
- `optimized_video_automation.py`
- `auto_video_processor.py`

Responsibilities:

- Render bilingual and Chinese-only video variants.
- Burn ASS or SRT subtitles into the video stream.
- Preserve or copy audio when possible.
- Write final videos under `final/` or a processed output directory.

Design notes:

- FFmpeg is the rendering boundary.
- Rendering failures are usually caused by invalid paths, invalid subtitle syntax, missing fonts, missing FFmpeg, or insufficient disk space.

### Publishing Assets

Responsible scripts:

- `generate_thumbnail_with_faces.py`
- `complete_bilibili_workflow.py`
- `create_jianying_danmaku.py`
- `advanced_jianying_danmaku.py`
- `auto_jianying_project.py`

Responsibilities:

- Generate Bilibili thumbnail images.
- Generate upload titles, descriptions, tags, summaries, and checklists.
- Generate danmaku timelines and Jianying helper assets.
- Keep platform-specific outputs next to the final video package.

Design notes:

- Bilibili and Jianying assets are generated as files, not uploaded automatically.
- This keeps review and publishing under user control.

### Project State

Responsible scripts:

- `complete_video_automation.py`
- `optimized_video_automation.py`
- `check_status.py`
- `cleanup_scripts.py`

Responsibilities:

- Store project state in JSON files.
- List active and completed projects.
- Resume projects waiting for translation.
- Clean or archive generated artifacts.

Typical state values:

- `waiting_translation`: source video and English subtitles exist, Chinese translation is missing.
- `completed`: final video and publishing artifacts have been generated.

## Data Model

### Project Directory

Each video project is stored under `output/` using a title-derived name plus timestamp.

```text
output/<safe_title>_<YYYYMMDD_HHMMSS>/
```

### Key Artifacts

```text
<source>.mp4                     # Downloaded or copied source video
subtitles/<source>_english.srt   # Whisper transcription
subtitles/chinese_translation.srt # Manual Chinese translation
subtitles/bilingual.ass          # Render-ready bilingual subtitle file
subtitles/chinese.ass            # Render-ready Chinese-only subtitle file
final/<source>_bilingual.mp4     # Final bilingual video
final/<source>_chinese.mp4       # Final Chinese-only video
translation_prompt.txt           # Translation prompt
automation_state.json            # Resume state
bilibili_metadata.json           # Upload metadata
bilibili_upload_content.md       # Human-readable upload copy
workflow_summary.md              # Processing summary
```

## Main Execution Paths

### Complete One-Shot Flow

```text
complete_bilibili_workflow.py
  -> create project directory
  -> download source video
  -> transcribe English SRT
  -> generate translation prompt
  -> wait for Chinese SRT
  -> render bilingual and Chinese videos
  -> create thumbnail
  -> create upload content
  -> create workflow summary
```

### Resumable Flow

```text
complete_video_automation.py
  -> start project
  -> write automation_state.json
  -> stop at waiting_translation
  -> --finalize or --continue
  -> render final package
  -> mark completed
```

### Optimized Flow

```text
optimized_video_automation.py
  -> download with retry/cache behavior
  -> optionally process video segment
  -> transcribe with cached Whisper model
  -> wait for translation
  -> finalize latest project
```

### Local Video Flow

```text
auto_video_processor.py
  -> accept local file or batch scan output/
  -> find related subtitles where available
  -> generate dual subtitles and danmaku
  -> render Bilibili-style outputs
```

## Error Handling Strategy

- Validate required input paths before processing.
- Stop early when downloads, transcription, or subtitle generation fails.
- Store intermediate files so a later run can continue instead of restarting.
- Keep final rendering separate from translation so failed finalization can be retried.
- Print clear status messages for manual workflows.

## Operational Constraints

- The system assumes local desktop execution, not a server runtime.
- FFmpeg and fonts are environment dependencies.
- Network-dependent steps can fail because of YouTube, connectivity, or `yt-dlp` changes.
- Large source and rendered videos can consume significant disk space.
- Manual translation remains outside the automation boundary.

## Extension Points

- Add a shared project model module to reduce repeated JSON and path handling.
- Add a CLI wrapper with subcommands for download, transcribe, translate, render, and package.
- Add automated validation for SRT timing and ASS syntax before rendering.
- Add configurable subtitle styles instead of hardcoded creator defaults.
- Add platform-specific publishing profiles for Bilibili, YouTube Shorts, TikTok, or Xiaohongshu.
- Add automated tests around subtitle conversion and project state transitions.

## Design Tradeoffs

- Script-based organization keeps workflows easy to run and modify, but creates some duplicated logic.
- Manual translation slows the pipeline, but improves localization quality and reduces content risk.
- Burning subtitles into videos improves platform compatibility, but requires full video re-rendering.
- File-based state is simple and inspectable, but does not provide concurrent job control.
