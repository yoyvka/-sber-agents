"""Скрипт для проверки и подготовки кэша для ручной загрузки модели"""
import os
from pathlib import Path
from huggingface_hub.utils import HfFolder

MODEL_NAME = "intfloat/multilingual-e5-base"
COMMIT_HASH = "835193815a3936a24a0ee7dc9e3d48c1fbb19c55"

# Определяем путь к кэшу
cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
model_cache_dir = os.path.join(cache_dir, "models--intfloat--multilingual-e5-base")
snapshots_dir = os.path.join(model_cache_dir, "snapshots")
commit_dir = os.path.join(snapshots_dir, COMMIT_HASH)

print("=" * 60)
print("Настройка кэша для ручной загрузки модели")
print("=" * 60)
print(f"\nМодель: {MODEL_NAME}")
print(f"Commit hash: {COMMIT_HASH}")
print(f"\nПуть к кэшу: {cache_dir}")
print(f"Директория модели: {model_cache_dir}")
print(f"Директория для файлов: {commit_dir}")
print("\n" + "=" * 60)

# Создаем структуру директорий
print("\nСоздаю структуру директорий...")
os.makedirs(commit_dir, exist_ok=True)
print(f"[OK] Создана директория: {commit_dir}")

# Создаем файл refs/main
refs_dir = os.path.join(model_cache_dir, "refs")
os.makedirs(refs_dir, exist_ok=True)
refs_file = os.path.join(refs_dir, "main")
with open(refs_file, 'w') as f:
    f.write(COMMIT_HASH)
print(f"[OK] Создан файл: {refs_file}")

print("\n" + "=" * 60)
print("Следующие шаги:")
print("=" * 60)
print("\n1. Откройте в браузере:")
print("   https://huggingface.co/intfloat/multilingual-e5-base/tree/main")
print("\n2. Скачайте следующие файлы в директорию:")
print(f"   {commit_dir}")
print("\n   Обязательные файлы:")
print("   - config.json")
print("   - model.safetensors (~420MB)")
print("   - tokenizer.json")
print("   - tokenizer_config.json")
print("   - sentencepiece.bpe.model")
print("\n3. После загрузки всех файлов запустите:")
print("   uv run python -c \"from sentence_transformers import SentenceTransformer;")
print("   model = SentenceTransformer('intfloat/multilingual-e5-base');")
print("   print('[OK] Модель загружена успешно!')\"")
print("\n" + "=" * 60)

