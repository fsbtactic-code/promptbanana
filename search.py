#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search.py - поиск по индексу промпт-инжиниринговых материалов.

Использование (CLI):
    python search.py "chain of thought"
    python search.py "few-shot prompting" --top 3
    python search.py "промпт инжиниринг 2026" --top 5
    python search.py --list-sources

Использование из Claude Code:
    Вызывается автоматически из CLAUDE.md скилла.
"""

import os
import sys
import pickle
import argparse
import json
import textwrap
from pathlib import Path

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    print("[ERR] Установите: pip install scikit-learn numpy")
    sys.exit(1)

# Пути — относительно этого скрипта
BASE_DIR   = Path(__file__).parent
INDEX_DIR  = BASE_DIR / 'index'
INDEX_PATH = INDEX_DIR / 'index.pkl'
CHUNKS_PATH= INDEX_DIR / 'chunks.pkl'
META_PATH  = INDEX_DIR / 'meta.json'

# Форматирование вывода
SEPARATOR = "─" * 72
CHUNK_PREVIEW_WORDS = 120   # сколько слов показать в preview


def load_index():
    """Загружает индекс и чанки из pickle."""
    if not INDEX_PATH.exists():
        print("[ERR] Индекс не найден. Запустите сначала: python build_index.py")
        sys.exit(1)

    with open(INDEX_PATH, 'rb') as f:
        data = pickle.load(f)
    with open(CHUNKS_PATH, 'rb') as f:
        chunks = pickle.load(f)

    return data['vectorizer'], data['matrix'], chunks


def search(query: str, top_n: int = 5, min_score: float = 0.01) -> list[dict]:
    """
    Ищет по запросу, возвращает топ-N релевантных чанков.

    Args:
        query: поисковый запрос (рус/eng)
        top_n: сколько результатов вернуть
        min_score: минимальный cosine score для включения

    Returns:
        Список dict с полями: source_name, source_file, text, score, chunk_idx
    """
    vectorizer, matrix, chunks = load_index()

    # Векторизуем запрос
    query_vec = vectorizer.transform([query])

    # Cosine similarity запроса со всеми чанками
    scores = cosine_similarity(query_vec, matrix).flatten()

    # Топ N по score
    top_indices = np.argsort(scores)[::-1][:top_n * 3]  # берём с запасом

    results = []
    seen_sources = {}  # дедупликация — не более 2 чанков с одного источника

    for idx in top_indices:
        score = float(scores[idx])
        if score < min_score:
            break

        chunk = chunks[idx]
        src = chunk['source_file']

        # Лимит 2 чанка с одного файла (чтобы не монополизировал)
        if seen_sources.get(src, 0) >= 2:
            continue
        seen_sources[src] = seen_sources.get(src, 0) + 1

        results.append({
            **chunk,
            'score': round(score, 4),
        })

        if len(results) >= top_n:
            break

    return results


def format_result(result: dict, rank: int) -> str:
    """Форматирует один результат для вывода."""
    words = result['text'].split()
    preview = ' '.join(words[:CHUNK_PREVIEW_WORDS])
    if len(words) > CHUNK_PREVIEW_WORDS:
        preview += '...'

    # Перенос длинных строк
    wrapped = textwrap.fill(preview, width=70, subsequent_indent='   ')

    score_pct = int(result['score'] * 100)
    score_bar = '#' * (score_pct // 5)
    score_bar = score_bar[:10].ljust(10, '.')

    lines = [
        f"#{rank}  [DOC] {result['source_name'][:65]}",
        f"   Релевантность: [{score_bar}] {result['score']:.3f}",
        f"   Файл: {result['source_file']}  (чанк {result['chunk_idx']})",
        f"",
        f"   {wrapped}",
    ]
    return '\n'.join(lines)


def list_sources():
    """Выводит список всех источников из мета-файла."""
    if not META_PATH.exists():
        print("[ERR] meta.json не найден. Запустите python build_index.py")
        sys.exit(1)

    with open(META_PATH, encoding='utf-8') as f:
        meta = json.load(f)

    print(f"\n[LIB] Библиотека промпт-инжиниринга ({meta['total_files']} источников, {meta['total_chunks']} чанков)\n")
    print(f"{'#':<4} {'Чанков':>6}  {'Источник'}")
    print(SEPARATOR)

    for i, src in enumerate(meta['sources'], 1):
        name = src['name'][:60]
        kb = src['chars'] // 1024
        print(f"{i:<4} {src['chunks']:>6}  {name}  ({kb} KB)")

    print(SEPARATOR)
    print(f"Итого: {meta['total_files']} файлов, {meta['total_chunks']} чанков")


def main():
    parser = argparse.ArgumentParser(
        description='🔍 Поиск по базе промпт-инжиниринговых материалов',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python search.py "chain of thought"
  python search.py "few-shot prompting claude" --top 3
  python search.py "промпт инжиниринг 2026"
  python search.py --list-sources
  python search.py "vector database evaluation" --json
        """
    )
    parser.add_argument('query', nargs='?', default=None,
                        help='Поисковый запрос')
    parser.add_argument('--top', '-n', type=int, default=5,
                        help='Количество результатов (default: 5)')
    parser.add_argument('--min-score', type=float, default=0.01,
                        help='Минимальный score (default: 0.01)')
    parser.add_argument('--list-sources', '-l', action='store_true',
                        help='Показать все источники в базе')
    parser.add_argument('--json', action='store_true',
                        help='Вывод в JSON (для программной обработки)')
    parser.add_argument('--index-dir', default=None,
                        help='Путь к папке с индексом (default: ./index)')

    args = parser.parse_args()

    # Переопределяем пути если указан --index-dir
    if args.index_dir:
        global INDEX_DIR, INDEX_PATH, CHUNKS_PATH, META_PATH
        INDEX_DIR   = Path(args.index_dir)
        INDEX_PATH  = INDEX_DIR / 'index.pkl'
        CHUNKS_PATH = INDEX_DIR / 'chunks.pkl'
        META_PATH   = INDEX_DIR / 'meta.json'

    if args.list_sources:
        list_sources()
        return

    if not args.query:
        parser.print_help()
        return

    # -- Поиск --
    results = search(args.query, top_n=args.top, min_score=args.min_score)

    if args.json:
        # Машиночитаемый вывод
        output = {
            'query': args.query,
            'total': len(results),
            'results': [
                {
                    'rank': i + 1,
                    'source': r['source_name'],
                    'file': r['source_file'],
                    'score': r['score'],
                    'text': r['text'][:800],
                }
                for i, r in enumerate(results)
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    # Человекочитаемый вывод
    print(f"\n[SEARCH] Запрос: \"{args.query}\"")
    print(f"   Найдено: {len(results)} релевантных фрагментов\n")
    print(SEPARATOR)

    if not results:
        print("[!] Ничего не найдено. Попробуйте другие ключевые слова.")
        return

    for i, result in enumerate(results, 1):
        print(format_result(result, i))
        print(SEPARATOR)

    # Краткий список источников в конце
    print("\n[SOURCES] Источники этого ответа:")
    seen = set()
    for r in results:
        if r['source_file'] not in seen:
            print(f"  - {r['source_name']}")
            seen.add(r['source_file'])


if __name__ == '__main__':
    main()
