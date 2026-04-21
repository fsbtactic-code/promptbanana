#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup.py - установка Prompt Banana.
Проверяет зависимости, папку sources/ и строит индекс.
"""
import sys
import os
import subprocess
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = Path(__file__).parent

def run(cmd, **kw):
    return subprocess.run(cmd, shell=True, **kw)

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def main():
    section("Prompt Banana — Setup")

    # 1. Зависимости
    section("1/3 Установка зависимостей")
    result = run(f'pip install -r "{BASE / "requirements.txt"}" --quiet')
    if result.returncode != 0:
        print("[ERR] Не удалось установить зависимости. Запустите: pip install scikit-learn numpy")
        sys.exit(1)
    print("[OK] scikit-learn и numpy установлены")

    # 2. Проверка sources/
    section("2/3 Проверка источников")
    sources_dir = BASE / 'sources'
    if not sources_dir.exists():
        sources_dir.mkdir()
        print(f"[>>] Создана папка: {sources_dir}")

    md_files = list(sources_dir.glob('*.md'))
    if not md_files:
        print()
        print("  [!] Папка sources/ пуста.")
        print()
        print("  Добавьте .md файлы в папку:")
        print(f"  {sources_dir}")
        print()
        print("  Затем запустите снова: python setup.py")
        print()
        print("  СОВЕТ: Используйте anonymize_sources.py для скрытия имён файлов.")
        return

    print(f"[OK] Найдено {len(md_files)} .md файлов в sources/")

    # Анонимизация если нужна
    has_non_anon = any(not f.name.startswith('doc_') for f in md_files)
    if has_non_anon:
        print()
        print("  [?] Ваши файлы имеют читаемые имена.")
        ans = input("  Анонимизировать источники (скрыть имена файлов)? [y/N]: ").strip().lower()
        if ans == 'y':
            result = run(f'python "{BASE / "anonymize_sources.py"}"')
            if result.returncode == 0:
                print("[OK] Источники анонимизированы")

    # 3. Сборка индекса
    section("3/3 Сборка TF-IDF индекса")
    result = run(f'python "{BASE / "build_index.py"}"')
    if result.returncode != 0:
        print("[ERR] Ошибка при сборке индекса")
        sys.exit(1)

    section("Готово!")
    print()
    print("  Тест поиска:")
    print(f'    python search.py "chain of thought"')
    print()
    print("  Скилл-команды в Claude Code:")
    commands = list((BASE / '.claude' / 'commands').glob('*.md'))
    for cmd in sorted(commands):
        print(f"    /{cmd.stem}")
    print()
    print("  Для использования: откройте Claude Code в папке")
    print(f"    {BASE}")

if __name__ == '__main__':
    main()
