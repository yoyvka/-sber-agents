"""Тестовый скрипт для проверки работы с Ollama"""
import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

async def test_ollama_connection():
    """Тестирует подключение к Ollama и работу моделей"""
    client = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
    
    print("=" * 60)
    print("Тест подключения к Ollama")
    print("=" * 60)
    print(f"Base URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"Model Text: {os.getenv('MODEL_TEXT')}")
    print(f"Model Image: {os.getenv('MODEL_IMAGE')}")
    print()
    
    # Тест 1: Проверка доступности API
    print("1. Проверка доступности API...")
    try:
        models = await client.models.list()
        print(f"   ✅ API доступен. Найдено моделей: {len(models.data)}")
        for model in models.data:
            print(f"      - {model.id}")
    except Exception as e:
        print(f"   ❌ Ошибка подключения: {e}")
        return False
    print()
    
    # Тест 2: Тестовый запрос текстовой модели
    print("2. Тест текстовой модели...")
    try:
        response = await client.chat.completions.create(
            model=os.getenv("MODEL_TEXT"),
            messages=[
                {"role": "user", "content": "Привет! Ответь одним словом: работает?"}
            ],
            max_tokens=10
        )
        answer = response.choices[0].message.content
        print(f"   ✅ Модель ответила: {answer}")
    except Exception as e:
        print(f"   ❌ Ошибка при запросе к текстовой модели: {e}")
        return False
    print()
    
    # Тест 3: Проверка структурированного ответа
    print("3. Тест структурированного ответа (JSON schema)...")
    try:
        response = await client.chat.completions.create(
            model=os.getenv("MODEL_TEXT"),
            messages=[
                {"role": "user", "content": "Я потратил 500 рублей на продукты сегодня"}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "test_response",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "answer": {"type": "string"},
                            "transactions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "amount": {"type": "number"},
                                        "type": {"type": "string", "enum": ["income", "expense"]},
                                        "category": {"type": "string"},
                                        "date": {"type": "string"}
                                    }
                                }
                            }
                        },
                        "required": ["answer", "transactions"]
                    },
                    "strict": True
                }
            }
        )
        answer = response.choices[0].message.content
        print(f"   ✅ Получен структурированный ответ (длина: {len(answer)} символов)")
        print(f"   Первые 200 символов: {answer[:200]}...")
    except Exception as e:
        print(f"   ❌ Ошибка при запросе структурированного ответа: {e}")
        return False
    print()
    
    print("=" * 60)
    print("✅ Все тесты пройдены успешно!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    result = asyncio.run(test_ollama_connection())
    exit(0 if result else 1)

