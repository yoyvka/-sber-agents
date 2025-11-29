import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from .llm import generate_reply, get_llm_runtime_info
from .config import get_settings

# Конфигурация
settings = get_settings()

# Логи
logging.basicConfig(level=getattr(logging, (settings.LOG_LEVEL or "INFO").upper(), logging.INFO))

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
HISTORY_MAX_MESSAGES = settings.HISTORY_MAX_MESSAGES

# Память диалога в оперативке: user_id -> list[dict(role, content)]
user_history: dict[int, list[dict]] = {}

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    # Логируем, с какими параметрами запускается LLM
    try:
        info = get_llm_runtime_info()
        print(
            f"LLM startup -> provider={info['provider']} | model={info['model']} | "
            f"base_url={info['base_url']} | key={info['api_key_masked']}"
        )
    except Exception as e:
        print(f"[LLM startup info error]: {e}")

    @dp.message(Command("start"))
    async def start_handler(message: types.Message):
        await message.answer("Привет! Я бот. Напишите сообщение или /help")

    @dp.message(Command("help"))
    async def help_handler(message: types.Message):
        await message.answer("/reset — сбросить контекст диалога")

    @dp.message(Command("reset"))
    async def reset_handler(message: types.Message):
        uid = message.from_user.id if message.from_user else None
        if uid is not None and uid in user_history:
            user_history.pop(uid, None)
        await message.answer("Контекст очищен.")

    @dp.message(Command("fail"))
    async def fail_handler(message: types.Message):
        """Эмулирует сбой LLM: подменяем модель на невалидную и проверяем ответ."""
        prev_model = os.getenv("LLM_MODEL")
        os.environ["LLM_MODEL"] = "__invalid_model__"
        try:
            # Пустая история, простой текст
            _ = generate_reply("Тест сбоя", [], "Проверка ошибки")
            await message.answer("Ожидалась ошибка, но модель вернула ответ.")
        except Exception as e:
            await message.answer("Извините, возникла временная ошибка. Попробуйте ещё раз чуть позже.")
            print(f"[BOT ERROR /fail] error={e}")
        finally:
            if prev_model is not None:
                os.environ["LLM_MODEL"] = prev_model
            else:
                os.environ.pop("LLM_MODEL", None)

    @dp.message()
    async def dialog_handler(message: types.Message):
        system = "Ты финансовый советник. Отвечай понятно и профессионально."
        user_text = message.text
        uid = message.from_user.id if message.from_user else None

        # История пользователя
        history = user_history.get(uid or 0, [])
        # Тримминг истории до лимита (оставляем последние HISTORY_MAX_MESSAGES)
        if len(history) > HISTORY_MAX_MESSAGES:
            history = history[-HISTORY_MAX_MESSAGES:]

        try:
            reply = generate_reply(system, history, user_text)
        except Exception as e:
            # Вежливое сообщение для пользователя + логируем ошибку в консоль
            await message.answer("Извините, возникла временная ошибка. Попробуйте ещё раз чуть позже.")
            print(f"[BOT ERROR] user={uid} error={e}")
            return
        if reply and reply.strip():
            await message.answer(reply)
            # Обновляем историю: добавляем реплики user и assistant
            updated = history + [
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": reply},
            ]
            # Снова триммим и сохраняем
            if len(updated) > HISTORY_MAX_MESSAGES:
                updated = updated[-HISTORY_MAX_MESSAGES:]
            if uid is not None:
                user_history[uid] = updated

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


