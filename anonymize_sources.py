#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anonymize_sources.py - переименовывает файлы в sources/ в doc_001.md...doc_050.md
и сохраняет маппинг в sources_map.json (не добавлять в git!).

Запуск: python anonymize_sources.py
"""

import os
import sys
import json
import shutil
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR   = Path(__file__).parent
SOURCES    = BASE_DIR / 'sources'
MAP_FILE   = BASE_DIR / 'sources_map.json'
INDEX_DIR  = BASE_DIR / 'index'

def anonymize():
    md_files = sorted(SOURCES.glob('*.md'))
    if not md_files:
        print('[ERR] Нет .md файлов в sources/')
        sys.exit(1)

    # Загружаем существующий маппинг если есть (для идемпотентности)
    existing_map = {}
    if MAP_FILE.exists():
        with open(MAP_FILE, encoding='utf-8') as f:
            existing_map = {v: k for k, v in json.load(f).items()}  # original→anon

    mapping = {}  # anon_name → original_name
    renames = []  # [(old_path, new_path)]

    for i, md_file in enumerate(md_files, 1):
        original_name = md_file.name
        anon_name = f'doc_{i:03d}.md'

        # Пропускаем уже анонимизированные
        if original_name.startswith('doc_') and len(original_name) == 10:
            mapping[original_name] = existing_map.get(original_name, original_name)
            continue

        mapping[anon_name] = original_name
        renames.append((md_file, SOURCES / anon_name))

    if not renames:
        print('[OK] Файлы уже анонимизированы')
        # Показываем текущий маппинг
        _show_summary(mapping)
        return

    print(f'[>>] Анонимизация {len(renames)} файлов...\n')
    for old_path, new_path in renames:
        print(f'  {old_path.name[:55]:<55} -> {new_path.name}')
        old_path.rename(new_path)

    # Сохраняем маппинг
    with open(MAP_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f'\n[OK] Переименовано: {len(renames)} файлов')
    print(f'[OK] Маппинг сохранён: {MAP_FILE}')
    print()
    print('[!] ВАЖНО: добавьте sources_map.json в .gitignore если нужна конфиденциальность')
    print()
    _show_summary(mapping)

    # Удаляем старый индекс — нужно пересобрать
    if INDEX_DIR.exists():
        shutil.rmtree(INDEX_DIR)
        print(f'[>>] Старый индекс удалён. Запустите: python build_index.py')

def _show_summary(mapping):
    print(f'[LIB] Маппинг ({len(mapping)} файлов):')
    for anon, orig in sorted(mapping.items())[:10]:
        print(f'  {anon} <- {orig[:65]}')
    if len(mapping) > 10:
        print(f'  ... и ещё {len(mapping)-10} файлов (полный список в sources_map.json)')

if __name__ == '__main__':
    anonymize()
