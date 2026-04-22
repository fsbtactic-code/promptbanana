#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package.py — Prompt Banana: сборка .skill файлов для claude.ai.

Создаёт:
  dist/*.skill   — zip-архивы с SKILL.md внутри (официальный формат Claude)
  dist/*.md      — те же скиллы как отдельные .md файлы с YAML frontmatter

Запуск: python package.py
"""

import zipfile
import sys
import io
from pathlib import Path

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent.resolve()
DIST_DIR = BASE_DIR / "dist"

# Метаданные для каждого скилла
SKILLS = [
    {
        "file":        "web/claude_opus47.md",
        "name":        "Prompt Banana — Claude Opus 4.7",
        "description": "Генерирует мега-промпты (8–16K символов) под архитектуру Claude Opus 4.7. XML-разметка, Extended Thinking, Artifacts v4, 10-слойная структура.",
        "out":         "prompt-banana-claude-opus47",
    },
    {
        "file":        "web/claude_sonnet46.md",
        "name":        "Prompt Banana — Claude Sonnet 4.6",
        "description": "Генерирует компактные промпты (4–10K символов) под Claude Sonnet 4.6. Оптимизирован для агентных задач и Tool Use.",
        "out":         "prompt-banana-claude-sonnet46",
    },
    {
        "file":        "web/gemini_3_1_pro.md",
        "name":        "Prompt Banana — Gemini 3.1 Pro",
        "description": "Генерирует промпты (6–12K символов) под Gemini 3.1 Pro. Текстовая архитектура без XML, якорение контекста, 2M токенов.",
        "out":         "prompt-banana-gemini-pro",
    },
    {
        "file":        "web/gemini_3_1_advanced.md",
        "name":        "Prompt Banana — Gemini 3.1 Advanced",
        "description": "Генерирует промпты (8–15K символов) под Gemini 3.1 Advanced. Deep Research, 20M токенов, Workspace интеграция.",
        "out":         "prompt-banana-gemini-advanced",
    },
    {
        "file":        "web/gpt5.md",
        "name":        "Prompt Banana — GPT-5",
        "description": "Генерирует мега-промпты (8–18K символов) под GPT-5. Markdown архитектура, Canvas, Deep Research, симуляция Роя Экспертов.",
        "out":         "prompt-banana-gpt5",
    },
    {
        "file":        "web/o4.md",
        "name":        "Prompt Banana — o4 / o4-mini",
        "description": "Генерирует ультра-лаконичные промпты (2–6K символов) под o4/o4-mini. Без CoT инструкций — только цель, ограничения, формат.",
        "out":         "prompt-banana-o4",
    },
    {
        "file":        "web/deepseek_r3.md",
        "name":        "Prompt Banana — DeepSeek R3",
        "description": "Генерирует минималистичные промпты (1.5–5K символов) под DeepSeek R3. R-Rules архитектура, без CoT.",
        "out":         "prompt-banana-deepseek-r3",
    },
]


def build_skill_content(meta: dict, body: str) -> str:
    """Собирает SKILL.md с YAML frontmatter + тело скилла."""
    yaml_header = (
        f"---\n"
        f"name: {meta['name']}\n"
        f"description: {meta['description']}\n"
        f"---\n\n"
    )
    return yaml_header + body


def make_skill_file(meta: dict):
    """Создаёт .skill файл (zip с SKILL.md внутри)."""
    src = BASE_DIR / meta["file"]
    if not src.exists():
        print(f"  [SKIP] Файл не найден: {src}")
        return

    body = src.read_text(encoding="utf-8")
    skill_content = build_skill_content(meta, body)

    out_path = DIST_DIR / f"{meta['out']}.skill"
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("SKILL.md", skill_content)

    size_kb = out_path.stat().st_size // 1024
    print(f"  [OK] {out_path.name} ({max(size_kb, 1)} KB)")
    return out_path


def make_md_file(meta: dict):
    """Создаёт .md файл с YAML frontmatter (альтернативный формат)."""
    src = BASE_DIR / meta["file"]
    if not src.exists():
        return

    body = src.read_text(encoding="utf-8")
    skill_content = build_skill_content(meta, body)

    out_path = DIST_DIR / f"{meta['out']}.md"
    out_path.write_text(skill_content, encoding="utf-8")
    print(f"  [OK] {out_path.name}")
    return out_path


def main():
    print()
    print("=" * 52)
    print("  🍌  PROMPT BANANA — Skill Packager")
    print("=" * 52)

    DIST_DIR.mkdir(exist_ok=True)

    print("\n  📦 Создание .skill файлов:")
    skill_files = []
    for meta in SKILLS:
        f = make_skill_file(meta)
        if f:
            skill_files.append(f)

    print("\n  📄 Создание .md файлов (с YAML frontmatter):")
    md_files = []
    for meta in SKILLS:
        f = make_md_file(meta)
        if f:
            md_files.append(f)

    print()
    print("=" * 52)
    print(f"  ✅  Готово! Создано {len(skill_files)} .skill + {len(md_files)} .md")
    print("=" * 52)
    print(f"\n  Папка: {DIST_DIR}")
    print()
    print("  Как загрузить в claude.ai:")
    print("  → Настройки → Skills → Upload → выбрать .skill файл")
    print()


if __name__ == "__main__":
    main()
