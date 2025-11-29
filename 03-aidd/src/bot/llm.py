import os
import sys
import time
from openai import OpenAI
from .config import get_settings

# Конфигурация
settings = get_settings()

def get_provider() -> str:
    provider = (settings.LLM_PROVIDER or "openrouter").lower()
    if provider not in {"openrouter", "openai"}:
        provider = "openrouter"
    return provider


def get_model() -> str:
    return settings.LLM_MODEL or "gpt-4o-mini"


def get_api_config() -> tuple[str, str | None]:
    """
    Возвращает (api_key, base_url). base_url=None означает использовать значение по умолчанию SDK.
    Поддерживаемые провайдеры: openrouter, openai.
    """
    provider = get_provider()
    if provider == "openai":
        key = settings.OPENAI_API_KEY
        if not key:
            raise ValueError("OPENAI_API_KEY is not set!")
        return key, None  # стандартный base_url клиента OpenAI
    # openrouter по умолчанию
    key = settings.OPENROUTER_API_KEY
    if not key:
        raise ValueError("OPENROUTER_API_KEY is not set!")
    return key, "https://openrouter.ai/api/v1"


def get_llm_runtime_info() -> dict:
    """
    Возвращает информацию о провайдере/модели/базовом URL и маскированном ключе
    для логирования (последние 6 символов ключа).
    """
    provider = get_provider()
    model = get_model()
    api_key, base_url = get_api_config()
    masked = ("***" + api_key[-6:]) if api_key and len(api_key) >= 6 else "***"
    return {
        "provider": provider,
        "model": model,
        "base_url": base_url or "<openai default>",
        "api_key_masked": masked,
    }


def generate_reply(system: str, history: list, user_text: str) -> str:
    """
    Генерирует ответ от LLM через OpenRouter (openai-compatible).
    system: системный промпт (строка)
    history: список сообщений формата {role, content}
    user_text: текст текущего пользователя
    """
    api_key, base_url = get_api_config()

    messages = [{
        "role": "system",
        "content": system
    }] + history + [{
        "role": "user",
        "content": user_text
    }]

    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    model = get_model()
    timeout_seconds = int(os.getenv("LLM_TIMEOUT", "15"))

    # Один ретрай при timeout/429
    attempts = 0
    max_attempts = 2
    last_error: Exception | None = None
    while attempts < max_attempts:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
                max_tokens=512,
                timeout=timeout_seconds,
            )
            return completion.choices[0].message.content or ""
        except Exception as e:
            text = str(e)
            # Простая диагностика: timeout/429 → ретрай один раз
            should_retry = ("timeout" in text.lower()) or (" 429" in text) or ("Too Many Requests" in text)
            attempts += 1
            last_error = e
            print(f"[LLM ERROR] attempt={attempts}/{max_attempts} model={model} error={text}", file=sys.stderr)
            if should_retry and attempts < max_attempts:
                time.sleep(0.8)
                continue
            break

    # Если не удалось — пробрасываем исключение наверх для вежливого ответа пользователю
    raise RuntimeError(str(last_error) if last_error else "LLM request failed")
