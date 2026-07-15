# ============================================
# Ollama Story Generator
# Generate cerita berkelanjutan + prompt ComfyUI
# ============================================

import requests
import json
from config import OLLAMA_URL, OLLAMA_MODEL, MAX_VIDEOS
from character_manager import CharacterManager

class OllamaStoryGenerator:
    def __init__(self):
        self.ollama_url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.char_manager = CharacterManager()
        self.check_ollama_connection()
    
    def check_ollama_connection(self):
        """Periksa koneksi ke Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"[OLLAMA] ✅ Terhubung ke Ollama di {self.ollama_url}")
                return True
            else:
                print(f"[OLLAMA] ❌ Ollama tidak merespons dengan baik")
                return False
        except:
            print(f"[OLLAMA] ❌ Gagal terhubung ke Ollama di {self.ollama_url}")
            print(f"[OLLAMA] Pastikan Ollama sudah running: ollama serve")
            return False
    
    def generate_story(self, character_name, song_title, duration, last_story=None):
        """
        Generate cerita berkelanjutan dengan Ollama
        
        Args:
            character_name (str): Nama karakter
            song_title (str): Judul lagu
            duration (float): Durasi audio dalam detik
            last_story (dict): Story terakhir untuk kontinuitas
            
        Returns:
            str: Generated story
        """
        # Build prompt
        if last_story:
            continuation_hint = f"\nCerita sebelumnya: {last_story['story'][:500]}..."
        else:
            continuation_hint = ""
        
        prompt = f"""Buatkan cerita pendek yang menarik untuk karakter bernama '{character_name}' yang mendengarkan lagu berjudul '{song_title}'. 

Ketentuan:
1. Cerita harus berkontinu dan berhubungan dengan lagu
2. Cerita harus menggambarkan gerakan, latar belakang, dan adegan yang sesuai dengan musik
3. Cerita harus bisa dibagi menjadi maksimal {MAX_VIDEOS} adegan visual yang berbeda
4. Setiap adegan harus memiliki durasi sekitar {duration/MAX_VIDEOS:.1f} detik
5. Gunakan bahasa Indonesia yang natural dan menarik{continuation_hint}

Buat cerita yang kaya dengan visual dan gerak karakter:"""
        
        print(f"[OLLAMA] Generating story untuk {character_name}...")
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                story = result.get('response', '').strip()
                print(f"[OLLAMA] ✅ Story generated successfully")
                return story
            else:
                print(f"[OLLAMA] ❌ Error: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"[OLLAMA] ❌ Exception: {e}")
            return None
    
    def generate_comfyui_prompts(self, story_text, character_name, duration):
        """
        Generate ComfyUI prompts dari story
        Pisahkan cerita menjadi maksimal 12 scene
        
        Args:
            story_text (str): Generated story
            character_name (str): Nama karakter
            duration (float): Durasi audio
            
        Returns:
            list: List of prompts untuk ComfyUI
        """
        prompt = f"""Analisis cerita berikut dan buatkan {MAX_VIDEOS} prompt visual yang detail untuk AI image generator (ComfyUI).
Setiap prompt harus menggambarkan SATU adegan dengan detail tentang:
- Latar belakang (background)
- Posisi dan gerakan karakter '{character_name}'
- Mood/atmosfer
- Warna dominan
- Detail lainnya yang relevan

Cerita:
{story_text}

Buat {MAX_VIDEOS} prompt (nomeri 1-{MAX_VIDEOS}) yang bisa di-generate menjadi gambar bergerak dengan durasi total {duration:.0f} detik.
Setiap prompt harus dalam bahasa Inggris dan detail untuk AI image generation.

Format output:
1. [PROMPT 1 untuk scene pertama]
2. [PROMPT 2 untuk scene kedua]
... dst"""
        
        print(f"[OLLAMA] Generating ComfyUI prompts...")
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.8
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                prompts_text = result.get('response', '').strip()
                prompts = self.parse_prompts(prompts_text)
                print(f"[OLLAMA] ✅ {len(prompts)} prompts generated")
                return prompts
            else:
                print(f"[OLLAMA] ❌ Error: {response.status_code}")
                return []
        
        except Exception as e:
            print(f"[OLLAMA] ❌ Exception: {e}")
            return []
    
    def parse_prompts(self, prompts_text):
        """
        Parse prompts dari output Ollama
        """
        prompts = []
        lines = prompts_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering
                if '. ' in line:
                    prompt = line.split('. ', 1)[1]
                elif '- ' in line:
                    prompt = line.split('- ', 1)[1]
                else:
                    prompt = line
                
                if prompt:
                    prompts.append(prompt)
        
        # Ensure max MAX_VIDEOS prompts
        return prompts[:MAX_VIDEOS]

if __name__ == "__main__":
    gen = OllamaStoryGenerator()
    test_story = "Markus berjalan di tengah kota yang ramai dengan musik mengalun indah."
    prompts = gen.generate_comfyui_prompts(test_story, "Markus", 30)
    print(json.dumps(prompts, indent=2, ensure_ascii=False))
