# ============================================
# Configuration Settings
# AI Character Story Video Generator
# ============================================

import os
from pathlib import Path

# ========== PATHS ==========
BASE_DIR = Path(r'F:\YOUTUBE\01.YOUTUBE DATA\Sutradara_AI')
INPUT_DIR = Path(r'C:\Users\mucha\AppData\Local\Comfy-Desktop\ComfyUI-Shared\input\input_karakter')
OUTPUT_DIR = Path(r'C:\Users\mucha\AppData\Local\Comfy-Desktop\ComfyUI-Shared\output\output_video')

# ========== OLLAMA SETTINGS ==========
OLLAMA_URL = "http://localhost:11434"  # Default Ollama URL
OLLAMA_MODEL = "mistral"  # atau "neural-chat"

# ========== COMFYUI SETTINGS ==========
COMFYUI_URL = "http://localhost:8188"  # Default ComfyUI URL
MAX_VIDEOS = 12  # Maksimal video yang bisa dibuat

# ========== CHARACTER POSES ==========
# 12 pose Markus yang berbeda dari folder input
CHARACTER_POSES = [
    "pose_1",
    "pose_2",
    "pose_3",
    "pose_4",
    "pose_5",
    "pose_6",
    "pose_7",
    "pose_8",
    "pose_9",
    "pose_10",
    "pose_11",
    "pose_12"
]

# ========== CHARACTER DATABASE ==========
CHARACTER_DB_FILE = BASE_DIR / "data" / "characters.json"

print(f"[CONFIG] Input Dir: {INPUT_DIR}")
print(f"[CONFIG] Output Dir: {OUTPUT_DIR}")
print(f"[CONFIG] Ollama: {OLLAMA_URL}/{OLLAMA_MODEL}")
print(f"[CONFIG] ComfyUI: {COMFYUI_URL}")
