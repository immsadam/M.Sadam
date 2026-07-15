# ============================================
# Main Application
# AI Character Story Video Generator
# Flow: Input > Audio > Ollama > ComfyUI
# ============================================

import os
import sys
from pathlib import Path
from config import INPUT_DIR, OUTPUT_DIR, BASE_DIR
from character_manager import CharacterManager
from audio_processor import AudioProcessor
from ollama_story_generator import OllamaStoryGenerator
from comfyui_runner import ComfyUIRunner

def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print aplikasi header"""
    print("\n" + "="*60)
    print(" 🎬 AI CHARACTER STORY VIDEO GENERATOR 🎬")
    print("="*60)
    print(" Input: Karakter + Lagu + Audio")
    print(" Process: Ollama → ComfyUI")
    print(" Output: Video dengan durasi sesuai musik")
    print("="*60 + "\n")

def get_user_input():
    """
    Minta input dari user:
    1. Nama karakter
    2. Judul lagu
    3. File audio (drag & drop)
    """
    print("\n[INPUT] Masukkan data berikut:\n")
    
    # 1. Nama Karakter
    character_name = input("👤 Nama Karakter: ").strip()
    if not character_name:
        print("[ERROR] Nama karakter tidak boleh kosong!")
        return None
    
    # 2. Judul Lagu
    song_title = input("🎵 Judul Lagu: ").strip()
    if not song_title:
        print("[ERROR] Judul lagu tidak boleh kosong!")
        return None
    
    # 3. File Audio (drag & drop atau path)
    print("\n🎧 Drag & drop file MP3/WAV atau ketik path file:")
    audio_path = input("   ").strip()
    
    # Remove quotes jika user copy dari file explorer
    audio_path = audio_path.strip('"').strip("'")
    
    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"[ERROR] File tidak ditemukan: {audio_path}")
        return None
    
    if audio_file.suffix.lower() not in ['.mp3', '.wav', '.m4a', '.flac']:
        print(f"[ERROR] Format audio tidak didukung. Gunakan MP3 atau WAV")
        return None
    
    return {
        'character_name': character_name,
        'song_title': song_title,
        'audio_path': str(audio_file)
    }

def main():
    """Main application flow"""
    clear_screen()
    print_header()
    
    # Check if output directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get user input
    user_input = get_user_input()
    if not user_input:
        print("\n[ABORT] Input tidak valid. Program dihentikan.")
        input("\nTekan ENTER untuk menutup...")
        return
    
    character_name = user_input['character_name']
    song_title = user_input['song_title']
    audio_path = user_input['audio_path']
    
    print(f"\n[INFO] Data yang diterima:")
    print(f"  - Karakter: {character_name}")
    print(f"  - Lagu: {song_title}")
    print(f"  - File: {audio_path}\n")
    
    # ========== STEP 1: Initialize managers ==========
    print("[STEP 1] Initializing systems...")
    try:
        char_manager = CharacterManager()
        audio_processor = AudioProcessor()
        story_gen = OllamaStoryGenerator()
        video_gen = ComfyUIRunner()
        print("[STEP 1] ✅ All systems initialized\n")
    except Exception as e:
        print(f"[ERROR] Gagal initialize systems: {e}")
        input("\nTekan ENTER untuk menutup...")
        return
    
    # ========== STEP 2: Process audio ==========
    print("[STEP 2] Processing audio...")
    duration = audio_processor.get_duration(audio_path)
    if duration is None:
        print("[ERROR] Gagal membaca durasi audio")
        input("\nTekan ENTER untuk menutup...")
        return
    
    frame_info = audio_processor.calculate_frames_needed(duration)
    print("[STEP 2] ✅ Audio processed\n")
    
    # ========== STEP 3: Generate story dengan Ollama ==========
    print("[STEP 3] Generating story dengan Ollama...")
    
    # Check if character exists and get last story for continuity
    char_manager.add_character(character_name)
    last_story = char_manager.get_last_story(character_name)
    
    story = story_gen.generate_story(
        character_name,
        song_title,
        duration,
        last_story
    )
    
    if not story:
        print("[ERROR] Gagal generate story")
        input("\nTekan ENTER untuk menutup...")
        return
    
    print(f"\n[STORY] Generated story (preview):\n{story[:300]}...\n")
    print("[STEP 3] ✅ Story generated\n")
    
    # ========== STEP 4: Generate ComfyUI prompts ==========
    print("[STEP 4] Generating ComfyUI prompts...")
    prompts = story_gen.generate_comfyui_prompts(
        story,
        character_name,
        duration
    )
    
    if not prompts:
        print("[ERROR] Gagal generate prompts")
        input("\nTekan ENTER untuk menutup...")
        return
    
    print(f"[PROMPTS] Generated {len(prompts)} prompts:")
    for i, prompt in enumerate(prompts, 1):
        print(f"  {i}. {prompt[:60]}...")
    print()
    print("[STEP 4] ✅ Prompts generated\n")
    
    # ========== STEP 5: Send to ComfyUI ==========
    print("[STEP 5] Sending to ComfyUI for video generation...")
    
    video_count = 0
    for i, prompt in enumerate(prompts, 1):
        duration_per_video = frame_info['duration_per_video']
        
        success = video_gen.generate_video_from_prompt(
            prompt,
            i,
            character_name,
            song_title,
            duration_per_video
        )
        
        if success:
            video_count += 1
        
        # Small delay between requests
        import time
        time.sleep(0.5)
    
    print(f"[STEP 5] ✅ {video_count} video generation tasks sent\n")
    
    # ========== STEP 6: Save to character database ==========
    print("[STEP 6] Saving to character database...")
    char_manager.add_story(
        character_name,
        song_title,
        story,
        prompts,
        duration
    )
    print("[STEP 6] ✅ Saved\n")
    
    # ========== COMPLETION ==========
    print("\n" + "="*60)
    print(" ✅ PROCESS COMPLETE!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"  - Karakter: {character_name}")
    print(f"  - Lagu: {song_title}")
    print(f"  - Durasi: {duration:.2f} detik")
    print(f"  - Video yang dibuat: {video_count}")
    print(f"  - Output dir: {OUTPUT_DIR}")
    print(f"  - Character database: {char_manager.db_file}")
    print(f"\n💡 Next steps:")
    print(f"  1. Tunggu ComfyUI selesai generate video")
    print(f"  2. Video akan disimpan di folder output")
    print(f"  3. Jalankan program lagi untuk cerita karakter yang sama (kontinuitas)")
    print("\n" + "="*60 + "\n")
    
    input("Tekan ENTER untuk menutup...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Program dihentikan oleh user")
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nProgram closed.")
