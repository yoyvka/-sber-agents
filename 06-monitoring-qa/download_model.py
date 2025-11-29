"""Скрипт для предварительной загрузки HuggingFace модели"""
import logging
import os
from sentence_transformers import SentenceTransformer
from huggingface_hub import snapshot_download

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODEL_NAME = "intfloat/multilingual-e5-base"

# Увеличиваем timeout для загрузки
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '600'  # 10 минут
os.environ['HF_HUB_DOWNLOAD_STREAM_TIMEOUT'] = '600'

logger.info(f"Загружаю модель {MODEL_NAME}...")
logger.info("Это может занять несколько минут, модель весит ~420MB...")
logger.info("Timeout установлен на 10 минут")

try:
    # Сначала попробуем скачать через snapshot_download с увеличенным timeout
    logger.info("Начинаю загрузку через HuggingFace Hub...")
    snapshot_download(
        repo_id=MODEL_NAME,
        cache_dir=None,  # Используем кэш по умолчанию
        resume_download=True,
        local_files_only=False
    )
    logger.info("Модель скачана, загружаю в SentenceTransformer...")
    
    # Теперь загружаем через SentenceTransformer (из кэша)
    model = SentenceTransformer(MODEL_NAME)
    logger.info(f"✅ Модель {MODEL_NAME} успешно загружена и сохранена в кэш!")
    logger.info(f"Размерность embeddings: {model.get_sentence_embedding_dimension()}")
except Exception as e:
    logger.error(f"❌ Ошибка при загрузке модели: {e}")
    logger.info("Рекомендация: Попробуйте позже, когда интернет-соединение будет стабильнее")
    logger.info("Или используйте более легкую модель, например: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    raise

logger.info("Модель готова к использованию!")

