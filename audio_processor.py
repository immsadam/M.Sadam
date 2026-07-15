# ============================================
# Audio Processor
# Extract duration dari MP3/WAV files
# ============================================

import os
from pathlib import Path
from pydub import AudioSegment
import json

class AudioProcessor:
    def __init__(self):
        self.supported_formats = ['.mp3', '.wav', '.m4a', '.flac']
    
    def get_duration(self, audio_file):
        """
        Ambil durasi file audio dalam detik
        
        Args:
            audio_file (str): Path ke file audio
            
        Returns:
            float: Durasi dalam detik
        """
        try:
            audio_file = Path(audio_file)
            if not audio_file.exists():
                raise FileNotFoundError(f"File tidak ditemukan: {audio_file}")
            
            # Detect format
            format_type = audio_file.suffix.lower().replace('.', '')
            
            # Load audio
            audio = AudioSegment.from_file(str(audio_file), format=format_type)
            duration_seconds = len(audio) / 1000  # Convert milliseconds to seconds
            
            print(f"[AUDIO] Durasi lagu: {duration_seconds:.2f} detik ({duration_seconds/60:.2f} menit)")
            return duration_seconds
        
        except Exception as e:
            print(f"[ERROR] Gagal membaca audio: {e}")
            return None
    
    def calculate_frames_needed(self, duration_seconds, fps=24, target_frame_count=12):
        """
        Hitung jumlah frame yang dibutuhkan untuk maksimal 12 video
        
        Args:
            duration_seconds (float): Durasi audio
            fps (int): Frame per second (default 24)
            target_frame_count (int): Target jumlah video (max 12)
            
        Returns:
            dict: Informasi frame calculation
        """
        total_frames = int(duration_seconds * fps)
        frames_per_video = max(1, total_frames // target_frame_count)
        
        result = {
            'duration_seconds': duration_seconds,
            'total_frames': total_frames,
            'fps': fps,
            'frames_per_video': frames_per_video,
            'actual_video_count': min(target_frame_count, (total_frames // frames_per_video) if frames_per_video > 0 else 1),
            'duration_per_video': frames_per_video / fps
        }
        
        print(f"[AUDIO] Total frames: {total_frames}")
        print(f"[AUDIO] Frames per video: {frames_per_video}")
        print(f"[AUDIO] Jumlah video yang akan dibuat: {result['actual_video_count']}")
        print(f"[AUDIO] Durasi per video: {result['duration_per_video']:.2f} detik")
        
        return result

if __name__ == "__main__":
    processor = AudioProcessor()
    # Test
    test_file = "test_audio.mp3"
    if os.path.exists(test_file):
        duration = processor.get_duration(test_file)
        processor.calculate_frames_needed(duration)
