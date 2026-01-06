# Voz <-> ChatGPT (Whisper + ChatGPT + gTTS) — Exemplo funcional

Este repositório é um esqueleto funcional de uma API que:
- recebe áudio (wav/mp3/m4a),
- transcreve usando Whisper (OpenAI),
- envia a transcrição ao ChatGPT,
- sintetiza a resposta com gTTS (Google Text-to-Speech),
- retorna transcrição, resposta e áudio em base64.

Aviso: este projeto é um exemplo educativo. Ajuste limites, segurança e registros antes de produção.

## Arquivos principais
- app/main.py — API FastAPI
- app/asr.py — integração com Whisper (OpenAI)
- app/chat.py — cliente ChatGPT
- app/tts.py — wrapper gTTS
- app/utils.py — helpers (conversão de áudio)
- tests/ — testes com pytest
- requirements.txt — dependências
- Dockerfile / docker-compose.yml

## Requisitos
- Python 3.10+
- ffmpeg instalado no sistema (ou via Docker)
- Chave de API OpenAI

## Variáveis de ambiente
Crie um arquivo `.env` (ou exporte) com:
- OPENAI_API_KEY=seu_token_openai
- OPENAI_CHAT_MODEL=gpt-4o-mini  # opcional, default definido no código
- TTS_DEFAULT_LANG=pt  # default para gTTS (pt, en, es, ...)

Arquivo de exemplo: `.env.example` neste repositório.

## Instalação local (recomendado para desenvolvimento)
1. Crie venv e instale dependências:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Instale ffmpeg (sistema). No Debian/Ubuntu:
   sudo apt update && sudo apt install -y ffmpeg

3. Rode a API:
   export OPENAI_API_KEY="sk-..."
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. Exemplo curl:
   curl -X POST "http://localhost:8000/api/v1/converse" \
     -F "audio=@./samples/sample_pt.mp3" \
     -F "language=pt"

## Docker
Construir e subir:
   docker compose up --build

## Uso da API
POST /api/v1/converse
- multipart/form-data:
  - `audio` — arquivo
  - `language` (opcional) — hint de idioma ex: `pt`, `en`, `es`
  - `session_id` (opcional)

Resposta JSON:
{
  "transcription": "...",
  "language": "pt",
  "chat_response": "...",
  "tts_audio_base64": "....",
  "tts_audio_format": "mp3"
}

## Testes
pytest

## Observações
- O código usa a API de transcrição da OpenAI (modelo `whisper-1`). Se preferir o pacote local de Whisper, substitua `app/asr.py`.
- gTTS pode exigir internet. Para TTS robusto/produção, considere Google Cloud TTS ou outro serviço pago.
- Não comite chaves de API.
