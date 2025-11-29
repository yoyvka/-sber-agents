"""Тест подключения бота к Ollama на облачном сервере"""
import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

async def test_connection():
    client = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
    
    print("=" * 60)
    print("Проверка подключения к Ollama на облачном сервере")
    print("=" * 60)
    print(f"Base URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"Model: {os.getenv('MODEL_TEXT')}")
    print()
    
    try:
        # Тест 1: Проверка доступности API
        print("1. Проверка доступности API...")
        models = await client.models.list()
        print(f"   ✅ API доступен. Найдено моделей: {len(models.data)}")
        for model in models.data:
            print(f"      - {model.id}")
        print()
        
        # Тест 2: Простой запрос
        print("2. Тест простого запроса...")
        response = await client.chat.completions.create(
            model=os.getenv("MODEL_TEXT"),
            messages=[{"role": "user", "content": "Ответь одним словом: работает?"}],
            max_tokens=5
        )
        answer = response.choices[0].message.content
        print(f"   ✅ Получен ответ: {answer}")
        print()
        
        # Тест 3: Запрос с JSON mode
        print("3. Тест запроса с JSON mode...")
        response = await client.chat.completions.create(
            model=os.getenv("MODEL_TEXT"),
            messages=[{"role": "user", "content": "Ответь в формате JSON: {\"answer\": \"тест\", \"transactions\": []}"}],
            response_format={"type": "json_object"},
            max_tokens=50
        )
        answer = response.choices[0].message.content
        print(f"   ✅ Получен JSON ответ (длина: {len(answer)} символов)")
        print(f"   Первые 100 символов: {answer[:100]}")
        print()
        
        print("=" * 60)
        print("✅ Все тесты пройдены! Бот может работать с Ollama.")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_connection())
    exit(0 if result else 1)

