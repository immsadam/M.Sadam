# ============================================
# ComfyUI Runner
# Send prompts ke ComfyUI dan generate videos
# ============================================

import requests
import json
import time
import subprocess
from pathlib import Path
from config import COMFYUI_URL, OUTPUT_DIR, INPUT_DIR

class ComfyUIRunner:
    def __init__(self):
        self.comfyui_url = COMFYUI_URL
        self.output_dir = OUTPUT_DIR
        self.input_dir = INPUT_DIR
        self.check_comfyui_connection()
    
    def check_comfyui_connection(self):
        """Periksa koneksi ke ComfyUI"""
        try:
            response = requests.get(f"{self.comfyui_url}/api/status", timeout=5)
            if response.status_code == 200:
                print(f"[COMFYUI] ✅ Terhubung ke ComfyUI di {self.comfyui_url}")
                return True
            else:
                print(f"[COMFYUI] ❌ ComfyUI tidak merespons dengan baik")
                return False
        except:
            print(f"[COMFYUI] ❌ Gagal terhubung ke ComfyUI di {self.comfyui_url}")
            print(f"[COMFYUI] Pastikan ComfyUI sudah running di port 8188")
            return False
    
    def generate_video_from_prompt(self, prompt_text, video_index, character_name, song_title, duration_per_video):
        """
        Kirim prompt ke ComfyUI untuk generate video
        
        Args:
            prompt_text (str): Deskripsi scene untuk generation
            video_index (int): Nomor video (1-12)
            character_name (str): Nama karakter
            song_title (str): Judul lagu
            duration_per_video (float): Durasi video per scene
            
        Returns:
            str: Path ke video yang di-generate
        """
        print(f"[COMFYUI] Generating video {video_index}...")
        print(f"[COMFYUI] Prompt: {prompt_text[:80]}...")
        
        # Buat workflow JSON untuk ComfyUI
        workflow = self.create_workflow(
            prompt_text,
            video_index,
            character_name,
            duration_per_video
        )
        
        try:
            # Send ke ComfyUI
            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json=workflow,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"[COMFYUI] ✅ Video {video_index} generation started")
                print(f"[COMFYUI] Output akan disimpan di: {self.output_dir}")
                return True
            else:
                print(f"[COMFYUI] ❌ Error: {response.status_code}")
                print(f"[COMFYUI] Response: {response.text}")
                return False
        
        except Exception as e:
            print(f"[COMFYUI] ❌ Exception: {e}")
            return False
    
    def create_workflow(self, prompt_text, video_index, character_name, duration):
        """
        Create ComfyUI workflow JSON
        Ini adalah template dasar - Anda perlu customize sesuai setup ComfyUI Anda
        
        Args:
            prompt_text (str): Prompt untuk generation
            video_index (int): Index video
            character_name (str): Nama karakter
            duration (float): Durasi video
            
        Returns:
            dict: ComfyUI workflow
        """
        # Template workflow - CUSTOMIZE SESUAI KEBUTUHAN ANDA
        workflow = {
            "1": {
                "inputs": {
                    "ckpt_name": "sd15_model.safetensors"  # Model yang Anda gunakan
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "2": {
                "inputs": {
                    "text": prompt_text,
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "3": {
                "inputs": {
                    "text": "bad quality, low quality",
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "4": {
                "inputs": {
                    "seed": video_index,
                    "steps": 20,
                    "cfg": 7.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["1", 0],
                    "positive": ["2", 0],
                    "negative": ["3", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "5": {
                "inputs": {
                    "width": 512,
                    "height": 512,
                    "length": int(duration * 30),  # 30 fps
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "samples": ["4", 0],
                    "vae": ["1", 2]
                },
                "class_type": "VAEDecode"
            },
            "7": {
                "inputs": {
                    "filename_prefix": f"{character_name}_{video_index:02d}",
                    "images": ["6", 0]
                },
                "class_type": "SaveImage"
            }
        }
        
        return workflow
    
    def merge_videos(self, video_paths, output_filename, audio_file):
        """
        Merge multiple videos menjadi satu dengan audio
        Menggunakan ffmpeg
        
        Args:
            video_paths (list): List path ke video files
            output_filename (str): Nama file output
            audio_file (str): Path ke file audio (MP3/WAV)
            
        Returns:
            str: Path ke merged video
        """
        output_path = self.output_dir / output_filename
        
        # Create concat file list for ffmpeg
        concat_file = self.output_dir / "concat_list.txt"
        with open(concat_file, 'w') as f:
            for video_path in video_paths:
                f.write(f"file '{video_path}'\n")
        
        # Merge dengan ffmpeg
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-i', str(audio_file),
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            str(output_path),
            '-y'  # Overwrite output
        ]
        
        try:
            print(f"[FFMPEG] Merging videos...")
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"[FFMPEG] ✅ Final video created: {output_path}")
            return str(output_path)
        
        except Exception as e:
            print(f"[FFMPEG] ❌ Error merging videos: {e}")
            return None

if __name__ == "__main__":
    runner = ComfyUIRunner()
    # Test workflow creation
    workflow = runner.create_workflow(
        "A beautiful scene with Markus walking in the city",
        1,
        "Markus",
        2.5
    )
    print(json.dumps(workflow, indent=2))
