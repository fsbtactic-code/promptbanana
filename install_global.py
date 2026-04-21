#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_global.py — Prompt Banana: установщик.

Запуск ПОСЛЕ клонирования репозитория:
  python install_global.py

Что делает:
  1. Устанавливает зависимости (scikit-learn, numpy)
  2. Создаёт стартовую базу знаний если sources/ пуста
  3. Строит поисковый индекс
  4. Копирует команды /promptbnn_* в ~/.claude/commands/
"""

import sys
import os
import io
import json
import shutil
import subprocess
from pathlib import Path

# Кодировка для Windows-терминалов
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR     = Path(__file__).parent.resolve()
COMMANDS_DIR = Path.home() / ".claude" / "commands"
PLACEHOLDER  = "{PROMPTBANANA_SEARCH}"


def section(n, text):
    print(f"\n{'─'*55}")
    print(f"  {n}  {text}")
    print(f"{'─'*55}")


def pip_install(*packages):
    cmd = [sys.executable, "-m", "pip", "install", "--quiet", "--upgrade"] + list(packages)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode == 0, r.stderr.strip()


def build_index():
    sources_dir = BASE_DIR / "sources"
    sources_dir.mkdir(exist_ok=True)

    if not list(sources_dir.glob("*.md")):
        starter = sources_dir / "doc_001.md"
        starter.write_text(
            "# Prompt Engineering Starter\n\n"
            "Chain-of-thought prompting improves reasoning by asking the model to think step by step.\n\n"
            "Few-shot examples help models understand the expected output format.\n\n"
            "XML tags work best with Claude. Structured headers work best with Gemini.\n\n"
            "Reasoning models (o4, DeepSeek R3) should NOT receive chain-of-thought instructions.\n\n"
            "System prompts define: role, context, goal, constraints, output format.\n",
            encoding='utf-8'
        )
        print("  [>>] Создан стартовый источник (добавьте свои .md файлы в sources/ позже)")

    r = subprocess.run(
        [sys.executable, str(BASE_DIR / "build_index.py")],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    if r.returncode != 0:
        print(f"  [!]  Индекс не собран — команды работают без поиска по базе")
        return False

    for line in r.stdout.strip().splitlines():
        if "Чанков" in line or "DONE" in line:
            print(f"  [OK] {line.strip()}")
    return True


def install_skills():
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    search_path = str(BASE_DIR / "search.py")

    skills_src = BASE_DIR / ".claude" / "commands"
    if not skills_src.exists():
        print("  [ERR] Папка .claude/commands не найдена")
        return []

    installed = []
    for skill_file in sorted(skills_src.glob("promptbnn_*.md")):
        content = skill_file.read_text(encoding='utf-8')
        content = content.replace(PLACEHOLDER, search_path)
        dest = COMMANDS_DIR / skill_file.name
        dest.write_text(content, encoding='utf-8')
        installed.append("/" + skill_file.stem)
        print(f"  [OK] /{skill_file.stem}")

    cfg = {"search_py": search_path, "install_dir": str(BASE_DIR)}
    (BASE_DIR / "install_config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    return installed


def main():
    print()
    print("=" * 55)
    print("  🍌  PROMPT BANANA — установка")
    print("=" * 55)
    print(f"  Python  : {sys.version.split()[0]}")
    print(f"  Система : {sys.platform}")
    print(f"  Папка   : {BASE_DIR}")

    section("1/3", "Установка зависимостей")
    ok, err = pip_install("scikit-learn", "numpy")
    if ok:
        print("  [OK] scikit-learn, numpy")
    else:
        print(f"  [!]  {err[:150]}")
        print("       Установите вручную: pip install scikit-learn numpy")

    section("2/3", "Сборка базы знаний")
    build_index()

    section("3/3", "Установка команд")
    installed = install_skills()

    print()
    print("=" * 55)
    print("  ✅  УСТАНОВКА ЗАВЕРШЕНА")
    print("=" * 55)
    print()
    print("  Перезапустите Claude Code, затем используйте:")
    print()
    for cmd in installed:
        print(f"    {cmd} [описание задачи]")
    print()
    print("  Пример:")
    print("    /promptbnn_claude_opus47 промпт для анализа")
    print("    конкурентов в нише SaaS")
    print()


if __name__ == "__main__":
    main()
