import os
import base64
import tempfile
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()
DEFAULT_LANG = os.getenv("TTS_DEFAULT_LANG", "pt")

# Map some BCP-47 codes to gTTS language codes (gTTS uses 2-letter)
LANG_MAP = {
    "pt": "pt",
    "pt-BR": "pt",
    "en": "en",
    "en-US": "en",
    "es": "es",
    "es-ES": "es",
}

def _map_lang(lang_hint: str):
    if not lang_hint:
        return DEFAULT_LANG
    return LANG_MAP.get(lang_hint, lang_hint.split("-")[0])

def synthesize_tts(text: str, lang_hint: str = None) -> str:
    """
    Synthesize text to mp3 using gTTS and return base64-encoded MP3 bytes.
    """
    lang = _map_lang(lang_hint)
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.write_to_fp(tmp)
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        b = f.read()
    try:
        os.remove(tmp_path)
    except:
        pass
    return base64.b64encode(b).decode("utf-8")