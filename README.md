# 🎬 AI Character Story Video Generator

## Overview

Sistem otomatis untuk generate video dengan cerita berkelanjutan berdasarkan:
1. **Karakter** yang Anda pilih
2. **Lagu** yang Anda suka
3. **Audio file** (MP3/WAV) untuk durasi

### Flow Sistem

```
┌─────────────────┐
│   USER INPUT    │
│ Nama + Lagu +   │
│    Audio File   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AUDIO PROCESSOR│ ← Extract durasi & frame count
└────────┬───��────┘
         │
         ▼
┌─────────────────┐
│    OLLAMA       │ ← Generate cerita berkelanjutan
│ (Story Gen)     │   + 12 ComfyUI prompts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    COMFYUI      │ ← Generate 12 video frames
│  (Video Gen)    │   sesuai durasi audio
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   OUTPUT VIDEO  │ ← Final video dengan audio
└─────────────────┘
```

## Requirements

### Software yang wajib install:

1. **Python 3.8+**
   - Download: https://www.python.org/
   - Pastikan "Add to PATH" saat install

2. **Ollama**
   - Download: https://ollama.ai
   - Setelah install, buka terminal:
     ```bash
     ollama pull mistral
     ```
   - Jalankan: `ollama serve`

3. **ComfyUI**
   - Sudah ada di: `C:\Users\mucha\AppData\Local\Comfy-Desktop\`
   - Pastikan running di port 8188

4. **FFmpeg** (untuk merge video + audio)
   - Download: https://ffmpeg.org/download.html
   - Atau: `pip install ffmpeg-python`

### Folder Structure

```
F:\YOUTUBE\01.YOUTUBE DATA\Sutradara_AI
├── run.bat                    ← JALANKAN INI
├── main.py
├── config.py
├── character_manager.py
├── audio_processor.py
├── ollama_story_generator.py
├── comfyui_runner.py
├── requirements.txt
├── data/
│   └── characters.json       (Auto-created)
└── README.md
```

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg (Windows)

```bash
pip install ffmpeg-python
```

Atau download dari: https://ffmpeg.org/download.html

### 3. Pastikan Services Running

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - ComfyUI:**
Buka ComfyUI dari Comfy Desktop

## Cara Menggunakan

### 1. Double-click `run.bat`

```
╔════════════════════════════════════════════════════════╗
║    🎬 AI CHARACTER STORY VIDEO GENERATOR 🎬           ║
╚════════════════════════════════════════════════════════╝
```

### 2. Masukkan Data

**Input 1: Nama Karakter**
```
👤 Nama Karakter: Markus
```

**Input 2: Judul Lagu**
```
🎵 Judul Lagu: Melancholy City
```

**Input 3: Audio File**
```
🎧 Drag & drop file MP3/WAV atau ketik path file:
   C:\Users\mucha\Music\song.mp3
```

### 3. Tunggu Proses

Sistem akan:
- ✅ Extract durasi audio
- ✅ Generate story dengan Ollama
- ✅ Generate 12 prompts untuk ComfyUI
- ✅ Send ke ComfyUI untuk video generation
- ✅ Simpan ke database karakter

### 4. Output

Video akan disimpan di:
```
C:\Users\mucha\AppData\Local\Comfy-Desktop\ComfyUI-Shared\output\output_video\
```

## Fitur Utama

### ✨ Cerita Berkelanjutan

Setiap kali Anda input karakter yang sama, cerita akan berlanjut dari cerita sebelumnya:

```
Session 1: Markus, Lagu "Sad"    → Story A
Session 2: Markus, Lagu "Happy"  → Story B (melanjutkan Story A)
Session 3: Markus, Lagu "Epic"   → Story C (melanjutkan Story B)
```

### 📊 Character Database

Semua cerita disimpan di: `data/characters.json`

Contoh isi:
```json
{
  "Markus": {
    "name": "Markus",
    "created_at": "2024-01-15T10:30:00",
    "stories": [
      {
        "id": 1,
        "song_title": "Sad Rain",
        "story": "Markus berjalan di bawah hujan...",
        "prompts": [...],
        "duration": 45.5,
        "video_count": 12
      }
    ],
    "total_videos": 12
  }
}
```

### 🎨 ComfyUI Integration

Gambar-gambar dari ComfyUI:
- Dipilih dari 12 pose Markus yang berbeda
- Generated dengan prompt spesifik
- Disesuaikan dengan durasi audio
- Bisa di-slow motion otomatis

## Configuration

Edit `config.py` untuk customize:

```python
# Paths
INPUT_DIR = r'C:\Users\mucha\AppData\Local\Comfy-Desktop\ComfyUI-Shared\input\input_karakter'
OUTPUT_DIR = r'C:\Users\mucha\AppData\Local\Comfy-Desktop\ComfyUI-Shared\output\output_video'

# Ollama
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"

# ComfyUI
COMFYUI_URL = "http://localhost:8188"
MAX_VIDEOS = 12  # Maksimal jumlah video per scene

# Character Poses
CHARACTER_POSES = ["pose_1", "pose_2", ..., "pose_12"]
```

## Troubleshooting

### ❌ "Failed to connect to Ollama"

**Solusi:**
1. Pastikan Ollama sudah install
2. Jalankan: `ollama serve` di terminal
3. Test: Buka browser ke `http://localhost:11434`

### ❌ "Failed to connect to ComfyUI"

**Solusi:**
1. Buka ComfyUI dari Comfy Desktop
2. Pastikan running di port 8188
3. Test: Buka browser ke `http://localhost:8188`

### ❌ "File not found: audio.mp3"

**Solusi:**
1. Pastikan path file benar (gunakan absolute path)
2. File harus format MP3, WAV, M4A, atau FLAC
3. Jangan ada spasi di akhir path

### ❌ "FFmpeg not found"

**Solusi:**
```bash
pip install ffmpeg-python
```

Atau download manual: https://ffmpeg.org/download.html

## Contoh Workflow

### Skenario 1: Create New Character

```
Session 1:
- Input: Markus, "Midnight City", song.mp3
- Output: 12 video + cerita baru
- Database: Create character "Markus"
```

### Skenario 2: Continue Character Story

```
Session 2:
- Input: Markus, "Sunset Dreams", song2.mp3
- Ollama automatically continues from Session 1
- Output: 12 video baru + cerita berkontinuasi
- Database: Add story ke Markus (total 2 story)
```

### Skenario 3: Multiple Characters

```
Session 1: Markus + Song A
Session 2: Luna + Song B
Session 3: Markus + Song C (Markus story continues)
Session 4: Luna + Song D (Luna story continues)
```

## Tips & Tricks

### 💡 Best Practices

1. **Audio Duration**
   - Optimal: 30-120 detik
   - Minimal: 10 detik (1 video per frame)
   - Maximal: 600 detik (12 video per frame)

2. **Song Selection**
   - Pilih lagu dengan mood yang konsisten
   - Lagu dengan narasi jelas → cerita lebih baik
   - Musik instrumental → visual-focused

3. **Character Consistency**
   - Semakin sering generate untuk karakter yang sama
   - Semakin kompleks cerita yang dibuat
   - Database akan terus berkembang

4. **Video Quality**
   - ComfyUI settings di config dapat di-adjust
   - Resolution: 512x512 (standard), 768x768 (high), 1024x1024 (ultra)
   - Semakin tinggi resolution = semakin lama generate

## File Structure Details

### `main.py`
- Entry point aplikasi
- Orchestrate semua module
- Handle user input

### `character_manager.py`
- Manage database karakter
- Load/save character stories
- Track character history

### `audio_processor.py`
- Extract durasi audio
- Calculate frame count
- Process MP3/WAV files

### `ollama_story_generator.py`
- Connect ke Ollama API
- Generate story berkelanjutan
- Create ComfyUI prompts

### `comfyui_runner.py`
- Connect ke ComfyUI API
- Create workflow JSON
- Merge video + audio (FFmpeg)

### `config.py`
- Centralized configuration
- Path settings
- API endpoints
- Model names

## Advanced Usage

### Custom Ollama Model

```python
# config.py
OLLAMA_MODEL = "neural-chat"  # atau model lainnya
```

Download model:
```bash
ollama pull neural-chat
```

### Custom ComfyUI Workflow

Edit `comfyui_runner.py` → `create_workflow()` method untuk custom workflow.

### Batch Processing

Buat file `batch.py`:
```python
from main import main

characters = ["Markus", "Luna", "Alex"]
songs = ["song1.mp3", "song2.mp3", "song3.mp3"]

for char in characters:
    for song in songs:
        # Modify user input
        main(char, song)
```

## Performance

### Typical Processing Time

| Step | Duration | Depends On |
|------|----------|-------------|
| Audio Processing | < 1s | File size |
| Ollama Story Gen | 30-120s | Model size + prompt |
| Ollama Prompt Gen | 30-60s | Prompt complexity |
| ComfyUI Gen (12x) | 5-30 min | GPU + resolution |
| Total | ~10-40 min | All factors |

### System Requirements

**Minimum:**
- CPU: Intel i5 / AMD Ryzen 5
- RAM: 8GB
- Disk: 20GB free space

**Recommended:**
- CPU: Intel i7 / AMD Ryzen 7
- RAM: 16GB+
- Disk: 50GB+ free space
- GPU: NVIDIA RTX 3060+ (untuk faster generation)

## License & Credits

- **Ollama**: Open-source LLM runner
- **ComfyUI**: Node-based UI for Stable Diffusion
- **FFmpeg**: Multimedia framework

## Support

Buat issue atau hubungi developer untuk bantuan:
- 📧 Email: contact@example.com
- 💬 Discord: [Link]
- 🐙 GitHub: [Link]

---

**Last Updated:** 2024-01-15
**Version:** 1.0.0
