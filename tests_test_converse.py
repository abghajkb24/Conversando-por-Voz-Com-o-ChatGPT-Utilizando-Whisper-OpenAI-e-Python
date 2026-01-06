import pytest
from fastapi.testclient import TestClient
from app.main import app
import base64
from unittest.mock import patch, MagicMock
import io

client = TestClient(app)

# Small silent wav (1s) generated for tests (header-only minimal valid wav)
SILENT_WAV_BYTES = b'RIFF$\x00\x00\x00WAVEfmt '  # not a full valid file; for real tests include fixtures

@pytest.fixture
def sample_wav_file(tmp_path):
    p = tmp_path / "sample.wav"
    # Create a short valid WAV using pydub would be better; here we just create placeholder bytes
    p.write_bytes(SILENT_WAV_BYTES)
    return p

def test_converse_happy_path(monkeypatch, sample_wav_file):
    # Mock asr.transcribe_audio
    monkeypatch.setattr("app.asr.transcribe_audio", lambda path: {"text": "Olá, como vai?", "language": "pt"})
    # Mock chat
    monkeypatch.setattr("app.chat.chat_with_gpt", lambda text, lang, session: "Estou bem, obrigado.")
    # Mock tts
    monkeypatch.setattr("app.tts.synthesize_tts", lambda text, lang: base64.b64encode(b"mp3bytes").decode("utf-8"))

    with open(sample_wav_file, "rb") as f:
        files = {"audio": ("sample.wav", f, "audio/wav")}
        resp = client.post("/api/v1/converse", files=files)
    assert resp.status_code == 200
    j = resp.json()
    assert j["transcription"] == "Olá, como vai?"
    assert j["language"] == "pt"
    assert "Estou bem" in j["chat_response"]
    assert isinstance(j["tts_audio_base64"], str)