Here is a precise and self-contained draft of the **first section** of your documentation, focused on the **introduction and encoding prerequisites**, especially for someone unfamiliar with your previous discussions:

---

# 📘 Documentation: `LiT_Concat_Video_Perso_Planque.py`

## 1. Introduction

### 🎯 **Purpose**

This script automates the **concatenation of three MP4 video segments** into a single file:

* `video1.mp4` – a 5-minute intro, always the same.
* A **personalized** `video2.mp4` (\~20 seconds), unique per file.
* `video3.mp4` – a short 20-second outro, based on the same base clip with small per-person visual modifications.

It is designed to **process thousands of trios efficiently** with:

* No re-encoding (preserving original quality).
* Fast performance via FFmpeg and `.ts` format.
* Logging for traceability.

---

### ⚙️ **How It Works (High-Level)**

1. It checks the presence of expected directories and video components.
2. Each MP4 file is **converted into MPEG-TS format**, which is stream-friendly and concatenation-safe.
3. The resulting `.ts` files are listed in a temporary file and **concatenated using FFmpeg**.
4. The final `.mp4` file is saved in the output directory.
5. Temporary files are deleted.

---

## 2. Input File Requirements

For the script to work reliably without re-encoding, **input videos must follow strict encoding constraints**.

### ✅ **Mandatory Encoding Constraints**

All 3 input videos must:

* Be encoded with:

  * **Video codec**: `H.264 / AVC` (usually shown as `avc1`)
  * **Audio codec**: `AAC`
* Share the **same resolution**: `720x1260` (portrait).
* Share the **same frame rate**: `24 fps`.
* Have **compatible GOP structures**, ideally:

  * Start and end on **I-frames** for safe stream-copy concatenation.
  * Avoid **B-frames at the end** of clips.

---

### 🔍 **How to Check Encoding (Using `ffprobe`)**

To inspect the encoding of a video file, run:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,codec_type,width,height,avg_frame_rate -of default=noprint_wrappers=1 input.mp4
```

To check audio codec:

```bash
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,codec_type -of default=noprint_wrappers=1 input.mp4
```

**Example Output Should Look Like:**

```
codec_name=h264
codec_type=video
width=720
height=1260
avg_frame_rate=24/1
---
codec_name=aac
codec_type=audio
```

You can also get a full overview using:

```bash
ffprobe -hide_banner -i input.mp4
```

Look for:

* `Stream #0:0` → video: h264 (Main)
* `Stream #0:1` → audio: aac

---

### ❌ What Happens If Constraints Are Not Met?

If codecs, resolution, or framerate do not match:

* FFmpeg may **fail silently** or **produce corrupted output**.
* Concatenated files might have **glitches**, **skipped frames**, or **desynchronized audio**.

To fix this:

* Use FFmpeg to re-encode with aligned parameters (we can provide a command later if needed).

---
Great. Let's move on to the **detailed step-by-step explanation** of how `LiT_Concat_Video_Perso_Planque.py` works, including purpose and reasoning behind each block of code.

---

## 3. Step-by-Step Workflow

### 🧩 Step 1: **Setup and Initialization**

#### 🛠 Imports and Logging

```python
import os, subprocess, logging
from datetime import datetime
```

* Standard libraries are used (no third-party dependencies).
* A timestamped log file is created inside the `./logs/` directory.

```python
log_filename = f"./logs/concat_Launch_v2_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_Log.txt"
logging.basicConfig(...)
```

📌 **Why?**

* For debugging and audit purposes.
* Useful when processing large batches to identify failed or skipped files.

---

### 📁 Step 2: **Define Paths and Validate File Presence**

```python
video1_path = './input/Video1/video1.mp4'
video2_path = './input/Video2/'
video3_path = './input/Video3/video3.mp4'
ConcatVideo_path = './output'
temp_folder = './temp'
```

* `video1` and `video3` are reused for every trio.
* `video2` directory contains personalized clips.

```python
if not os.path.exists(...) ...
```

🧪 **Why?**

* Prevents the script from crashing midway due to missing input or output paths.
* Ensures early failure with clear logs.

---

### 🔁 Step 3: **Loop Over Personalized MP4s**

```python
video_files = os.listdir(video2_path)
mp4_files = [file for file in video_files if file.endswith(".mp4")]
```

* Collects all personalized MP4 files.
* For each one, creates an output concatenated file.

```python
if os.path.exists(output_path):
    continue
```

📌 **Why?**

* Avoids redundant processing of already-generated videos.

---

### 🔄 Step 4: **Convert MP4s to TS Format**

```python
def convert_to_ts(input_file, output_file):
    run_ffmpeg_command([
        "ffmpeg", "-i", input_file, "-c", "copy",
        "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", output_file, "-y"
    ])
```

📦 **Purpose of this step**:

* Converts each MP4 into a `.ts` (MPEG-TS) file without re-encoding.
* Adds necessary Annex B headers (`h264_mp4toannexb`) to make H.264 streams **safely concatenable**.

💡 **Why TS?**

* TS allows stream-based concatenation with fewer playback issues.
* MP4 structure (moov atoms, indexes) is not naturally concatenation-friendly.

---

### 📝 Step 5: **Create FFmpeg Input List for Concatenation**

```python
with open(input_list_file, "w") as f:
    f.write(f"file '{ts1_path}'\n")
    f.write(f"file '{ts2_path}'\n")
    f.write(f"file '{ts3_path}'\n")
```

📌 **Why?**

* FFmpeg expects a text file with paths for input when using `-f concat`.
* Absolute paths are used to avoid relative path resolution issues.

---

### 🎬 Step 6: **Concatenate Using FFmpeg**

```python
run_ffmpeg_command([
    "ffmpeg", "-f", "concat", "-safe", "0", "-fflags", "+genpts",
    "-i", input_list_file, "-c", "copy", "-bsf:a", "aac_adtstoasc",
    "-y", output_path
])
```

🔍 **Explanation**:

* `-f concat`: Tells FFmpeg to read a list of input files.
* `-safe 0`: Allows unsafe file paths (like absolute paths).
* `-fflags +genpts`: Re-generates timestamps for smoother playback.
* `-c copy`: No re-encoding; fast and lossless.
* `-bsf:a aac_adtstoasc`: Fixes AAC bitstream for MP4 container.

📌 **Why this exact sequence?**

* This combination ensures speed, compatibility, and clean playback.

---

### 🧹 Step 7: **Clean Up Temporary Files**

```python
os.remove(ts1_path)
os.remove(ts2_path)
os.remove(ts3_path)
os.remove(input_list_file)
```

📌 **Why?**

* Keeps the `./temp` folder clean.
* Avoids clutter and future read/write conflicts.

---

## ✅ 4. Summary of Pre-Requisites

| Requirement                   | Why It Matters                                         |
| ----------------------------- | ------------------------------------------------------ |
| FFmpeg installed              | All video operations rely on it.                       |
| Input video format: H.264/AAC | Required for stream-copy compatibility in `.ts` files. |
| Matching resolution & fps     | Avoids audio/video drift or playback errors.           |
| No B-frames at segment ends   | Reduces decoding artifacts after concat.               |
| Python 3.x                    | Runs the script and manages file I/O and logs.         |
| Directory structure           | Expected input/output folders must exist beforehand.   |

---

Would you like me to continue with sections on known limitations, debugging tips, and future improvements?
Perfect — let’s complete the documentation with sections on **limitations**, **debugging tips**, and **future improvements**. These are essential for helping a new developer understand edge cases and extend the project if needed.

---

## ⚠️ 5. Known Limitations & Edge Cases

### ❗ 1. **Input Incompatibility**

If any input video does **not** meet encoding constraints (e.g., mismatched resolution, wrong codec), FFmpeg will:

* Either fail outright with an error, or
* Produce an unplayable or glitchy output.

📌 **Recommendation**: Always validate inputs using `ffprobe`.

---

### ❗ 2. **Hidden Frame Issues (e.g., B-frames at Segment Boundaries)**

* If a clip ends on a **B-frame** or does not start with an **I-frame**, playback artifacts can appear after concatenation.
* Since the script does **not re-encode**, it cannot fix these at runtime.

📌 **Recommendation**: Ensure clean GOP structures when preparing the videos.

---

### ❗ 3. **No Parallelization**

* The script currently processes one file at a time, which can be slow over thousands of files.

📌 **Workaround**: You can manually run the script in multiple terminals on different video subsets — or future improvements can introduce multiprocessing.

---

### ❗ 4. **Error Handling Is Centralized**

* One failure stops the entire script (e.g., if FFmpeg crashes on a bad input).
* Logs are available for debugging, but the batch continues only if you restart it.

📌 **Recommendation**: Add try/except blocks per iteration if you want to continue despite failures.

---

## 🧪 6. Debugging & Quality Control Tips

### 🧾 Check Output Video Info

To inspect the output file’s encoding:

```bash
ffprobe -i ./output/bodycam_example.mp4
```

Ensure:

* `codec_name=h264` for video
* `codec_name=aac` for audio
* `avg_frame_rate=24/1`
* No dropped frames or warnings

---

### 🔍 View TS Intermediate Files

If you suspect that one `.ts` segment is malformed:

```bash
ffplay ./temp/intermediate_2.ts
```

This lets you debug whether the error comes from the personalization clip or from the concatenation logic.

---

### 🪵 Read the Log

Each script run generates a log like:

```
./logs/concat_Launch_v2_2025_05_09_14_35_12_Log.txt
```

Look for:

* `[INFO] Processing completed successfully`
* `[ERROR] FFmpeg command failed` with detailed stderr output

---

### 🛠 Fixing Bad Inputs

To re-encode a bad input video and force proper structure:

```bash
ffmpeg -i bad_input.mp4 -c:v libx264 -preset fast -crf 18 -g 24 -c:a aac -b:a 128k fixed_input.mp4
```

This ensures:

* H.264 + AAC
* Keyframes every second (`-g 24`)
* Compatible audio stream

---

## 🚀 7. Future Improvements

### 🧵 1. Multiprocessing Support

Use Python’s `multiprocessing.Pool` to run batches in parallel, especially useful with SSD storage and multiple cores.

### 🧪 2. Input Validator

Add a helper script or flag that:

* Runs `ffprobe` on all inputs
* Confirms resolution, framerate, and codecs before concatenation



## 📎 8. Appendix: CLI Cheat Sheet

| Task                           | Command Example                                                        |
| ------------------------------ | ---------------------------------------------------------------------- |
| Inspect video encoding         | `ffprobe -hide_banner -i input.mp4`                                    |
| Play .ts intermediate file     | `ffplay ./temp/intermediate_2.ts`                                      |
| Manually concatenate .ts files | `ffmpeg -f concat -i input_list.txt -c copy output.mp4`                |
| Re-encode for compatibility    | `ffmpeg -i input.mp4 -c:v libx264 -g 24 -c:a aac -b:a 128k output.mp4` |

---
