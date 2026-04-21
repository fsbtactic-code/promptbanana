#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_index.py - строит TF-IDF индекс из 50 Markdown файлов.
Запускать один раз, или при обновлении источников.

Использование:
    python build_index.py
    python build_index.py --sources ./sources --output ./index
"""

import os
import re
import sys
import json
import pickle
import argparse
from pathlib import Path

# Форсируем UTF-8 вывод в Windows-терминале
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# scikit-learn для TF-IDF
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
except ImportError:
    print("[ERR] Установите зависимости: pip install scikit-learn numpy")
    sys.exit(1)


# ──────────────────────────────────────────────
# Настройки чанкинга
# ──────────────────────────────────────────────
CHUNK_SIZE_WORDS = 400        # слов в чанке
CHUNK_OVERLAP_WORDS = 80      # слов перекрытия между чанками

# Файлы с особым режимом (большие транскрипты — берём только первые N слов)
LARGE_FILE_CAP = {
    "48-CLAUDE CODE- ПОЛНЫЙ КУРС 2026 (4+ ЧАСА).md": 15000,  # ~37 страниц
}


def clean_markdown(text: str) -> str:
    """Убирает Markdown-форматирование, оставляет чистый текст."""
    # Удалить код-блоки (сохранить первую строку — название языка)
    text = re.sub(r'```[^\n]*\n(.*?)```', lambda m: m.group(1)[:200], text, flags=re.DOTALL)
    # Удалить inline-код
    text = re.sub(r'`[^`]+`', '', text)
    # Заголовки → текст
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Ссылки → текст ссылки
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Изображения
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)
    # HTML-теги
    text = re.sub(r'<[^>]+>', '', text)
    # Таблицы — убрать разделители
    text = re.sub(r'\|[-:]+\|[-:| ]+\|', '', text)
    text = re.sub(r'\|', ' ', text)
    # Жирный/курсив
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
    # Списки — убрать маркеры
    text = re.sub(r'^[\s]*[-*+•]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)
    # Горизонтальные линии
    text = re.sub(r'^[-_*]{3,}\s*$', '', text, flags=re.MULTILINE)
    # Множественные пустые строки
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def split_into_chunks(text: str, source_file: str, source_name: str) -> list[dict]:
    """Делит текст на перекрывающиеся чанки по словам."""
    words = text.split()

    # Ограничение для больших файлов
    cap = LARGE_FILE_CAP.get(source_file)
    if cap and len(words) > cap:
        print(f"  [!] {source_file}: обрезан до {cap} слов (из {len(words)})")
        words = words[:cap]

    chunks = []
    start = 0
    chunk_idx = 0

    while start < len(words):
        end = min(start + CHUNK_SIZE_WORDS, len(words))
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)

        chunks.append({
            'id': f"{source_name}__chunk_{chunk_idx}",
            'source_file': source_file,
            'source_name': source_name,
            'chunk_idx': chunk_idx,
            'text': chunk_text,
            'word_start': start,
            'word_end': end,
        })

        chunk_idx += 1
        start += CHUNK_SIZE_WORDS - CHUNK_OVERLAP_WORDS

    return chunks


def build_index(sources_dir: Path, output_dir: Path):
    """Основная функция: читает MD → чистит → чанкует → индексирует."""
    output_dir.mkdir(parents=True, exist_ok=True)

    md_files = sorted(sources_dir.glob("*.md"))
    if not md_files:
        print(f"❌ Не найдено .md файлов в {sources_dir}")
        sys.exit(1)

    print(f"[OK] Найдено файлов: {len(md_files)}")
    print(f"[>>] Источники:      {sources_dir}")
    print(f"[>>] Индекс будет:   {output_dir}")
    print()

    all_chunks = []
    stats = []

    for md_file in md_files:
        file_name = md_file.name
        # Красивое имя: убрать номер в начале и расширение
        clean_name = re.sub(r'^\d+-', '', md_file.stem)

        try:
            text = md_file.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"  [ERR] Не удалось прочитать {file_name}: {e}")
            continue

        clean_text = clean_markdown(text)
        chunks = split_into_chunks(clean_text, file_name, clean_name)

        all_chunks.extend(chunks)
        stats.append({
            'file': file_name,
            'name': clean_name,
            'chars': len(text),
            'chunks': len(chunks),
        })
        print(f"  [+] {clean_name[:60]:<60} -> {len(chunks):>3} чанков")

    print(f"\nВсего чанков: {len(all_chunks)}")
    print("Строим TF-IDF индекс (подождите)...")

    # TF-IDF с поддержкой русского и английского
    vectorizer = TfidfVectorizer(
        analyzer='word',
        token_pattern=r'[а-яёА-ЯЁa-zA-Z]{2,}',  # рус + eng, мин 2 символа
        ngram_range=(1, 2),                        # уnigramы и bigramы
        max_df=0.90,                               # игнорировать слова в >90% чанков
        min_df=1,
        sublinear_tf=True,                         # log(TF) — сглаживание частот
        max_features=50_000,
    )

    corpus = [c['text'] for c in all_chunks]
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Сохраняем
    chunks_path = output_dir / 'chunks.pkl'
    index_path  = output_dir / 'index.pkl'
    meta_path   = output_dir / 'meta.json'

    with open(chunks_path, 'wb') as f:
        pickle.dump(all_chunks, f)

    with open(index_path, 'wb') as f:
        pickle.dump({'vectorizer': vectorizer, 'matrix': tfidf_matrix}, f)

    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump({
            'total_files': len(stats),
            'total_chunks': len(all_chunks),
            'sources': stats,
        }, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] Готово!")
    print(f"   Чанков:    {len(all_chunks)}")
    print(f"   Словарь:   {len(vectorizer.vocabulary_):,} токенов")
    print(f"   Индекс:    {index_path} ({index_path.stat().st_size / 1024:.0f} KB)")
    print(f"   Чанки:     {chunks_path}")
    print(f"   Мета:      {meta_path}")
    print()
    print('Теперь можно искать: python search.py "chain of thought"')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Строит TF-IDF индекс из Markdown файлов')
    parser.add_argument('--sources', default='./sources',
                        help='Папка с .md файлами (default: ./sources)')
    parser.add_argument('--output',  default='./index',
                        help='Папка для индекса (default: ./index)')
    args = parser.parse_args()

    build_index(Path(args.sources), Path(args.output))
