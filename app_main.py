from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import tempfile
import shutil
import os

from .asr import transcribe_audio
from .chat import chat_with_gpt
from .tts import synthesize_tts
from .utils import convert_to_wav_16k

app = FastAPI(title="Whisper + ChatGPT + gTTS")

class ConverseResponse(BaseModel):
    transcription: str
    language: Optional[str]
    chat_response: str
    tts_audio_base64: str
    tts_audio_format: str = "mp3"

@app.post("/api/v1/converse", response_model=ConverseResponse)
async def converse(
    audio: UploadFile = File(...),
    language: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None),
):
    # Validate content-type
    if not audio.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="Arquivo enviado não é um áudio válido.")

    # Save uploaded file to a temporary location
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio.filename)[1]) as tmp:
            contents = await audio.read()
            tmp.write(contents)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {e}")

    try:
        # Convert to standard wav 16k mono if necessary
        wav_path = convert_to_wav_16k(tmp_path)

        # Transcribe using Whisper (OpenAI)
        asr_result = transcribe_audio(wav_path)
        transcription = asr_result.get("text", "").strip()
        detected_lang = asr_result.get("language") or language

        # ChatGPT response (system prompt to reply in user language)
        chat_resp = chat_with_gpt(transcription, detected_lang, session_id)

        # TTS synthesis
        tts_b64 = synthesize_tts(chat_resp, detected_lang)

        return JSONResponse({
            "transcription": transcription,
            "language": detected_lang,
            "chat_response": chat_resp,
            "tts_audio_base64": tts_b64,
            "tts_audio_format": "mp3"
        })
    finally:
        # Cleanup files
        try:
            os.remove(tmp_path)
        except:
            pass
        try:
            if 'wav_path' in locals() and os.path.exists(wav_path):
                os.remove(wav_path)
        except:
            pass