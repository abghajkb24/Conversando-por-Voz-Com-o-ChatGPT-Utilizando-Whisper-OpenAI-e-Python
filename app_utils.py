import os
from pydub import AudioSegment
import tempfile

def convert_to_wav_16k(src_path: str) -> str:
    """
    Convert input audio to WAV PCM 16k mono (whisper-friendly).
    Returns path to converted file (temporary).
    """
    dest = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    dest.close()
    audio = AudioSegment.from_file(src_path)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(dest.name, format="wav")
    return dest.name