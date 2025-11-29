"""Скрипт для запуска evaluation"""
import logging
import sys
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / "src"))

from evaluation import evaluate_dataset
from config import config
import indexer
import rag

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def init_rag():
    """Инициализация RAG перед evaluation"""
    print("Initializing RAG system...")
    rag.vector_store = await indexer.reindex_all()
    if rag.vector_store:
        rag.initialize_retriever()
        stats = rag.get_vector_store_stats()
        print(f"RAG initialized: {stats['count']} documents indexed")
    else:
        raise ValueError("Failed to initialize vector store")

if __name__ == "__main__":
    import asyncio
    
    if not config.LANGSMITH_API_KEY:
        print("ERROR: LANGSMITH_API_KEY not set in .env")
        sys.exit(1)
    
    # Инициализируем RAG
    asyncio.run(init_rag())
    
    dataset_name = config.LANGSMITH_DATASET
    print(f"Starting evaluation for dataset: {dataset_name}")
    
    try:
        result = evaluate_dataset(dataset_name)
        
        print("\n" + "=" * 60)
        print("Evaluation Results")
        print("=" * 60)
        print(f"Dataset: {result['dataset_name']}")
        print(f"Examples processed: {result['num_examples']}")
        print("\nRAGAS Metrics:")
        for metric, score in result['metrics'].items():
            print(f"  {metric}: {score:.3f}")
        print("=" * 60)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

