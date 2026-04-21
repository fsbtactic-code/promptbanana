#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_global.py — Prompt Banana: глобальный установщик.

Работает на Windows / macOS / Linux.
Не требует git. Скачивает архив напрямую с GitHub.

Запуск одной командой в Claude Code:
  python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/install_global.py').read().decode())"
"""

import sys
import os
import io
import json
import shutil
import zipfile
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# ── Кодировка для Windows-терминалов ──────────────────────────
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ── Константы ─────────────────────────────────────────────────
REPO_ZIP_URL  = "https://github.com/fsbtactic-code/promptbanana/archive/refs/heads/main.zip"
REPO_ZIP_DIR  = "promptbanana-main"        # имя папки внутри zip
INSTALL_DIR   = Path.home() / ".claude" / "promptbanana"
COMMANDS_DIR  = Path.home() / ".claude" / "commands"
PLACEHOLDER   = "{PROMPTBANANA_SEARCH}"

def section(emoji, text):
    print(f"\n{'─'*55}")
    print(f"  {emoji}  {text}")
    print(f"{'─'*55}")

def pip_install(*packages):
    """Устанавливает пакеты через текущий Python (sys.executable)."""
    cmd = [sys.executable, "-m", "pip", "install", "--quiet", "--upgrade"] + list(packages)
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result.returncode == 0, result.stderr

def download_and_extract():
    """Скачивает zip-архив репозитория и распаковывает в INSTALL_DIR."""
    print(f"  [>>] Скачиваем архив...")
    try:
        # Некоторые машины требуют User-Agent
        req = urllib.request.Request(REPO_ZIP_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
    except urllib.error.URLError as e:
        print(f"  [ERR] Не удалось скачать архив: {e}")
        sys.exit(1)

    print(f"  [>>] Распаковываем ({len(data)//1024} KB)...")
    tmp_dir = INSTALL_DIR.parent / "_pb_tmp"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir, ignore_errors=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            zf.extractall(tmp_dir)
    except zipfile.BadZipFile as e:
        print(f"  [ERR] Поврежденный архив: {e}")
        sys.exit(1)

    extracted = tmp_dir / REPO_ZIP_DIR
    if not extracted.exists():
        # Попробуем найти единственную распакованную папку
        subdirs = [d for d in tmp_dir.iterdir() if d.is_dir()]
        if len(subdirs) == 1:
            extracted = subdirs[0]
        else:
            print(f"  [ERR] Неожиданная структура архива: {list(tmp_dir.iterdir())}")
            sys.exit(1)

    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR, ignore_errors=True)
    shutil.move(str(extracted), str(INSTALL_DIR))
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"  [OK] Установлено в: {INSTALL_DIR}")

def build_index():
    """Собирает поисковый индекс."""
    sources_dir = INSTALL_DIR / "sources"
    sources_dir.mkdir(exist_ok=True)

    md_files = list(sources_dir.glob("*.md"))
    if not md_files:
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
        print("  [>>] Создан стартовый источник (можно добавить свои .md файлы позже)")

    result = subprocess.run(
        [sys.executable, str(INSTALL_DIR / "build_index.py")],
        cwd=INSTALL_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    if result.returncode != 0:
        print(f"  [WARN] Индекс не собран — скиллы работают без поиска по базе")
        print(f"         {result.stderr.strip()[:200]}")
        return False

    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    summary = next((l for l in lines if "Чанков" in l or "DONE" in l), "OK")
    print(f"  [OK] Индекс готов: {summary}")
    return True

def install_skills():
    """Копирует скилл-файлы в ~/.claude/commands/ с подстановкой пути."""
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    search_path = str(INSTALL_DIR / "search.py")

    skills_src = INSTALL_DIR / ".claude" / "commands"
    if not skills_src.exists():
        print("  [ERR] Скилл-файлы не найдены в архиве")
        sys.exit(1)

    installed = []
    for skill_file in sorted(skills_src.glob("promptbnn_*.md")):
        content = skill_file.read_text(encoding='utf-8')
        content = content.replace(PLACEHOLDER, search_path)
        dest = COMMANDS_DIR / skill_file.name
        dest.write_text(content, encoding='utf-8')
        installed.append("/" + skill_file.stem)

    # Сохраняем конфиг установки
    cfg = {"search_py": search_path, "install_dir": str(INSTALL_DIR), "version": "1.0"}
    (INSTALL_DIR / "install_config.json").write_text(
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
    print(f"  Папка   : {INSTALL_DIR}")

    # ── 1. Скачать и распаковать ──────────────────────────────
    section("1/4", "Загрузка файлов")
    download_and_extract()

    # ── 2. Зависимости ───────────────────────────────────────
    section("2/4", "Установка зависимостей")
    ok, err = pip_install("scikit-learn", "numpy")
    if ok:
        print("  [OK] scikit-learn, numpy")
    else:
        print(f"  [WARN] pip: {err.strip()[:150]}")
        print("         Если поиск не работает — установите вручную: pip install scikit-learn numpy")

    # ── 3. Индекс ─────────────────────────────────────────────
    section("3/4", "Сборка базы знаний")
    build_index()

    # ── 4. Скилл-файлы ────────────────────────────────────────
    section("4/4", "Установка команд")
    installed = install_skills()
    for cmd in installed:
        print(f"  [OK] {cmd}")

    # ── Готово ────────────────────────────────────────────────
    print()
    print("=" * 55)
    print("  ✅  PROMPT BANANA УСТАНОВЛЕН")
    print("=" * 55)
    print()
    print("  Перезапустите Claude Code, затем используйте:")
    print()
    for cmd in installed:
        print(f"    {cmd} [описание вашей задачи]")
    print()
    print("  Пример:")
    print("    /promptbnn_claude_opus47 промпт для анализа")
    print("    конкурентов в нише SaaS")
    print()
    print("  Добавить собственные источники:")
    print(f"    {INSTALL_DIR / 'sources'}")
    print(f"    python \"{INSTALL_DIR / 'build_index.py'}\"")
    print()

if __name__ == "__main__":
    main()
