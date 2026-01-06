import os
import openai
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
DEFAULT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")  # ajuste conforme disponível

def chat_with_gpt(user_text: str, user_lang: str = None, session_id: str = None) -> str:
    """
    Send transcription to ChatGPT and return the assistant reply as plain text.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY não configurada.")

    system_prompt = "Você é um assistente útil. Responda no mesmo idioma da entrada do usuário."
    if user_lang:
        system_prompt = f"Você é um assistente útil. Responda em '{user_lang}' quando apropriado."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text}
    ]

    # ChatCompletion API
    resp = openai.ChatCompletion.create(
        model=DEFAULT_MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=800
    )
    # Parse response
    choice = resp["choices"][0]
    content = choice["message"]["content"].strip()
    return content