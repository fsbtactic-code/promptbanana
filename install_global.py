#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_global.py — Prompt Banana RAG: глобальный установщик.

Запуск одной командой в Claude Code:
  python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/install_global.py').read().decode())"

Что делает:
  1. Клонирует репозиторий в ~/.claude/promptbanana/
  2. Устанавливает зависимости (scikit-learn, numpy)
  3. Находит существующие .md файлы в sources/ или создаёт минимальный индекс
  4. Подставляет корректные пути в скилл-файлы
  5. Копирует скиллы в ~/.claude/commands/ (глобальный доступ)
  6. Выводит список готовых команд
"""

import sys, os, shutil, subprocess, json, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

REPO_URL   = "https://github.com/fsbtactic-code/promptbanana.git"
INSTALL_DIR = Path.home() / ".claude" / "promptbanana"
COMMANDS_DIR = Path.home() / ".claude" / "commands"
PLACEHOLDER = "{PROMPTBANANA_SEARCH}"

def run(cmd, cwd=None, check=False):
    return subprocess.run(cmd, shell=True, cwd=cwd,
                         capture_output=True, text=True, encoding='utf-8', errors='replace')

def section(title):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")

def main():
    print("\n🍌 PROMPT BANANA RAG — Global Installer")
    print("=" * 55)

    # ── 1. Клонирование / обновление ─────────────────────────
    section("1/4  Клонирование репозитория")
    if (INSTALL_DIR / ".git").exists():
        print(f"  [>>] Обновляем существующую установку: {INSTALL_DIR}")
        r = run("git pull --quiet", cwd=INSTALL_DIR)
        if r.returncode != 0:
            print(f"  [!]  git pull вернул: {r.stderr.strip()}")
        else:
            print("  [OK] Обновлено до актуальной версии")
    else:
        print(f"  [>>] Клонируем в {INSTALL_DIR}")
        INSTALL_DIR.parent.mkdir(parents=True, exist_ok=True)
        r = run(f'git clone --depth 1 "{REPO_URL}" "{INSTALL_DIR}"')
        if r.returncode != 0:
            print(f"  [ERR] git clone завершился с ошибкой:\n{r.stderr}")
            sys.exit(1)
        print("  [OK] Репозиторий клонирован")

    # ── 2. Зависимости ────────────────────────────────────────
    section("2/4  Установка зависимостей")
    r = run(f'pip install scikit-learn numpy --quiet')
    if r.returncode != 0:
        print(f"  [WARN] pip install: {r.stderr.strip()}")
    else:
        print("  [OK] scikit-learn, numpy установлены")

    # ── 3. Индекс ─────────────────────────────────────────────
    section("3/4  Сборка индекса")
    sources_dir = INSTALL_DIR / "sources"
    index_dir   = INSTALL_DIR / "index"
    sources_dir.mkdir(exist_ok=True)

    md_files = list(sources_dir.glob("*.md"))
    if not md_files:
        # Создаём минимальный стартовый документ чтобы индекс собрался
        starter = sources_dir / "doc_001.md"
        starter.write_text(
            "# Prompt Engineering Starter\n\n"
            "Chain-of-thought (CoT) prompting improves reasoning by asking the model to think step by step.\n\n"
            "Few-shot examples help models understand the expected output format.\n\n"
            "XML tags work best with Claude. Structured headers work best with Gemini.\n\n"
            "Reasoning models (o4, DeepSeek R3) should NOT receive chain-of-thought instructions.\n\n"
            "System prompts should define: role, context, goal, constraints, output format.\n",
            encoding='utf-8'
        )
        print("  [>>] sources/ пуста — создан стартовый doc_001.md")
        print("  [!]  Добавьте свои .md файлы в:")
        print(f"       {sources_dir}")
        print("       Затем запустите: python build_index.py")

    r = run(f'python "{INSTALL_DIR / "build_index.py"}"', cwd=INSTALL_DIR)
    if r.returncode != 0:
        print(f"  [WARN] Не удалось собрать индекс: {r.stderr.strip()[:200]}")
        print("         Скиллы будут работать без RAG-поиска.")
    else:
        lines = [l for l in r.stdout.strip().splitlines() if l.strip()]
        summary = next((l for l in lines if "Чанков" in l or "DONE" in l), "OK")
        print(f"  [OK] Индекс собран → {summary.strip()}")

    # ── 4. Скилл-файлы ────────────────────────────────────────
    section("4/4  Установка скилл-файлов")
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    search_path = str(INSTALL_DIR / "search.py")
    # На Windows экранируем обратные слэши
    if os.name == 'nt':
        search_path_escaped = search_path.replace("\\", "\\\\")
    else:
        search_path_escaped = search_path

    skills_src = INSTALL_DIR / ".claude" / "commands"
    if not skills_src.exists():
        print("  [ERR] Папка .claude/commands не найдена в репозитории")
        sys.exit(1)

    installed = []
    for skill_file in sorted(skills_src.glob("promptbnn_*.md")):
        content = skill_file.read_text(encoding='utf-8')
        # Подставляем актуальный путь к search.py
        content = content.replace(PLACEHOLDER, search_path_escaped)
        # Убираем старые захардкоженые пути (на случай если они остались)
        import re
        content = re.sub(
            r'python\s+"[^"]*search\.py"',
            f'python "{search_path_escaped}"',
            content
        )
        dest = COMMANDS_DIR / skill_file.name
        dest.write_text(content, encoding='utf-8')
        installed.append(skill_file.stem)
        print(f"  [OK] /{skill_file.stem}")

    # Записываем путь к search.py для справки
    config = {"search_py": search_path, "install_dir": str(INSTALL_DIR)}
    (INSTALL_DIR / "install_config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8'
    )

    # ─── Финал ───────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  ✅  PROMPT BANANA RAG УСТАНОВЛЕН")
    print("=" * 55)
    print()
    print("  Доступные команды в Claude Code:")
    for name in installed:
        print(f"    /{name} [описание задачи]")
    print()
    print("  Пример:")
    print("    /promptbnn_gemini3_1_pro создай промпт для")
    print("    анализа конкурентов в нише SaaS")
    print()
    print("  Добавить свои источники:")
    print(f"    {sources_dir}")
    print(f"    python \"{INSTALL_DIR / 'build_index.py'}\"")
    print()

if __name__ == "__main__":
    main()
