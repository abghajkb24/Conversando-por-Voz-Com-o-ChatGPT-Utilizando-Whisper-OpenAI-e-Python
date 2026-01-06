import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def transcribe_audio(file_path: str) -> dict:
    """
    Transcribe an audio file using OpenAI Whisper API (whisper-1).
    Returns a dict with keys: text, language (if available).
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY não configurada.")

    with open(file_path, "rb") as f:
        # Using OpenAI's transcription endpoint
        # This example calls openai.Audio.transcribe (interface may vary conforme versão da lib)
        try:
            resp = openai.Audio.transcribe("whisper-1", f)
        except AttributeError:
            # fallback older/newer clients may use different naming
            resp = openai.api_requestor.request("post", "/v1/audio/transcriptions", files={"file": f}, data={"model":"whisper-1"})
        # 'text' key is expected
        text = resp.get("text") if isinstance(resp, dict) else getattr(resp, "text", "")
        language = None
        # Some responses include language metadata
        if isinstance(resp, dict):
            language = resp.get("language")
        return {"text": text or "", "language": language}