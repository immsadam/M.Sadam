# ============================================
# Character Manager
# Manage character stories dan history
# ============================================

import json
from pathlib import Path
from datetime import datetime
from config import CHARACTER_DB_FILE

class CharacterManager:
    def __init__(self):
        self.db_file = CHARACTER_DB_FILE
        self.ensure_db_exists()
        self.characters = self.load_database()
    
    def ensure_db_exists(self):
        """Pastikan folder dan file database ada"""
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_file.exists():
            self.db_file.write_text(json.dumps({}, indent=2))
            print(f"[DB] Database baru dibuat: {self.db_file}")
    
    def load_database(self):
        """Load database karakter dari JSON"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_database(self):
        """Simpan database karakter ke JSON"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.characters, f, indent=2, ensure_ascii=False)
        print(f"[DB] Database disimpan")
    
    def add_character(self, character_name):
        """Tambah karakter baru atau kembalikan yang ada"""
        if character_name not in self.characters:
            self.characters[character_name] = {
                'name': character_name,
                'created_at': datetime.now().isoformat(),
                'stories': [],
                'total_videos': 0
            }
            self.save_database()
            print(f"[CHAR] Karakter baru ditambahkan: {character_name}")
        else:
            print(f"[CHAR] Karakter sudah ada: {character_name}")
        
        return self.characters[character_name]
    
    def add_story(self, character_name, song_title, story_text, prompts, duration):
        """Tambah story baru untuk karakter"""
        if character_name not in self.characters:
            self.add_character(character_name)
        
        story = {
            'id': len(self.characters[character_name]['stories']) + 1,
            'song_title': song_title,
            'story': story_text,
            'prompts': prompts,
            'duration': duration,
            'created_at': datetime.now().isoformat(),
            'video_count': len(prompts) if prompts else 0
        }
        
        self.characters[character_name]['stories'].append(story)
        self.characters[character_name]['total_videos'] += story['video_count']
        self.save_database()
        
        print(f"[CHAR] Story ditambahkan untuk {character_name}: {song_title}")
        return story
    
    def get_character_history(self, character_name):
        """Ambil history cerita karakter"""
        if character_name in self.characters:
            return self.characters[character_name]['stories']
        return []
    
    def get_last_story(self, character_name):
        """Ambil story terakhir dari karakter (untuk kontinuitas cerita)"""
        if character_name in self.characters:
            stories = self.characters[character_name]['stories']
            if stories:
                return stories[-1]
        return None
    
    def list_all_characters(self):
        """List semua karakter yang ada"""
        return list(self.characters.keys())

if __name__ == "__main__":
    manager = CharacterManager()
    # Test
    manager.add_character("Markus")
    print(manager.list_all_characters())
