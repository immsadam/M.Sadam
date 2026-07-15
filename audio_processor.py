# ============================================
# Audio Processor (Fixed for Python 3.13)
# Extract duration dari MP3/WAV files
# Using wave module (built-in, no pydub needed)
# ============================================

import os
from pathlib import Path
import wave

class AudioProcessor:
    def __init__(self):
        self.supported_formats = ['.mp3', '.wav', '.m4a', '.flac']
    
    def get_duration_wav(self, audio_file):
        """
        Get duration dari WAV file
        
        Args:
            audio_file (str): Path ke file WAV
            
        Returns:
            float: Durasi dalam detik
        """
        try:
            with wave.open(str(audio_file), 'rb') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
                return duration
        except Exception as e:
            print(f"[ERROR] Gagal membaca WAV: {e}")
            return None
    
    def get_duration_mp3(self, audio_file):
        """
        Get duration dari MP3 file
        Fallback ke librosa jika tersedia
        
        Args:
            audio_file (str): Path ke file MP3
            
        Returns:
            float: Durasi dalam detik
        """
        try:
            # Try librosa first
            import librosa
            audio_data, sr = librosa.load(str(audio_file), sr=None)
            duration = librosa.get_duration(y=audio_data, sr=sr)
            return duration
        except ImportError:
            try:
                # Try with subprocess + ffprobe
                import subprocess
                
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
                     '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1', 
                     str(audio_file)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    return float(result.stdout.strip())
            except:
                pass
            
            # Fallback: estimate based on file size
            print(f"[WARNING] Using file size estimation for MP3 (not accurate)")
            file_size = os.path.getsize(audio_file)
            # Rough estimate: 128 kbps = 16 KB/s
            estimated_duration = file_size / 16000
            return estimated_duration
    
    def get_duration(self, audio_file):
        """
        Ambil durasi file audio dalam detik
        Support MP3, WAV, M4A, FLAC
        
        Args:
            audio_file (str): Path ke file audio
            
        Returns:
            float: Durasi dalam detik
        """
        try:
            audio_file = Path(audio_file)
            if not audio_file.exists():
                raise FileNotFoundError(f"File tidak ditemukan: {audio_file}")
            
            # Get file extension
            file_ext = audio_file.suffix.lower()
            
            if file_ext == '.wav':
                duration = self.get_duration_wav(audio_file)
            elif file_ext == '.mp3':
                duration = self.get_duration_mp3(audio_file)
            elif file_ext in ['.m4a', '.flac']:
                # Try librosa or ffprobe
                duration = self.get_duration_mp3(audio_file)
            else:
                raise ValueError(f"Format tidak didukung: {file_ext}")
            
            if duration is None:
                raise ValueError("Gagal extract durasi")
            
            print(f"[AUDIO] ✅ Durasi lagu: {duration:.2f} detik ({duration/60:.2f} menit)")
            return duration
        
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
    
    # Test dengan file lokal
    test_files = [
        "test_audio.wav",
        "test_audio.mp3",
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n[TEST] Testing {test_file}...")
            duration = processor.get_duration(test_file)
            if duration:
                processor.calculate_frames_needed(duration)
