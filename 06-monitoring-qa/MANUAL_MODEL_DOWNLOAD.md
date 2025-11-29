# Инструкция по ручной загрузке модели intfloat/multilingual-e5-base

## Шаг 1: Определите путь к кэшу HuggingFace

На Windows кэш обычно находится в:
```
C:\Users\<ваше_имя_пользователя>\.cache\huggingface\hub\models--intfloat--multilingual-e5-base
```

## Шаг 2: Скачайте необходимые файлы модели

Откройте в браузере страницу модели:
**https://huggingface.co/intfloat/multilingual-e5-base/tree/main**

Скачайте следующие файлы (нажмите на файл, затем кнопку "Download"):

### Обязательные файлы:
1. **config.json** - конфигурация модели
2. **model.safetensors** - веса модели (~420MB, самый большой файл)
3. **tokenizer.json** - токенизатор
4. **tokenizer_config.json** - конфигурация токенизатора
5. **sentencepiece.bpe.model** - модель токенизации

### Дополнительные файлы (для sentence-transformers):
6. **modules.json** - конфигурация модулей (если есть)
7. **1_Pooling/config.json** - конфигурация pooling слоя (если есть)
8. **2_Dense/config.json** - конфигурация dense слоя (если есть)

## Шаг 3: Создайте структуру директорий

Создайте следующую структуру в кэше:

```
C:\Users\<ваше_имя_пользователя>\.cache\huggingface\hub\
└── models--intfloat--multilingual-e5-base\
    └── snapshots\
        └── <commit_hash>\
            ├── config.json
            ├── model.safetensors
            ├── tokenizer.json
            ├── tokenizer_config.json
            ├── sentencepiece.bpe.model
            ├── modules.json (если есть)
            └── 1_Pooling\
                └── config.json (если есть)
```

## Шаг 4: Получите commit hash

Запустите команду для получения commit hash:
```powershell
uv run python -c "from huggingface_hub import model_info; info = model_info('intfloat/multilingual-e5-base'); print(info.sha)"
```

Или найдите его на странице модели в разделе "Files and versions" - он будет в URL, например: `835193815a3936a24a0ee7dc9e3d48c1fbb19c55`

## Шаг 5: Поместите файлы в правильную директорию

1. Создайте директорию: `C:\Users\<ваше_имя_пользователя>\.cache\huggingface\hub\models--intfloat--multilingual-e5-base\snapshots\<commit_hash>\`
2. Поместите все скачанные файлы в эту директорию

## Шаг 6: Создайте файл refs/main (опционально)

Создайте файл `refs/main` в директории `models--intfloat--multilingual-e5-base\` со следующим содержимым:
```
<commit_hash>
```

## Альтернативный способ: Используйте Git LFS

Если у вас установлен Git с LFS, можно клонировать репозиторий:

```powershell
cd C:\Users\<ваше_имя_пользователя>\.cache\huggingface\hub
git lfs install
git clone https://huggingface.co/intfloat/multilingual-e5-base models--intfloat--multilingual-e5-base
```

Затем переименуйте `main` в `snapshots/<commit_hash>`.

## Проверка

После ручной загрузки проверьте, что модель загружается:

```powershell
uv run python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('intfloat/multilingual-e5-base'); print('Модель загружена успешно!')"
```

