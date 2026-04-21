<div align="center">

# 🍌 Prompt Banana

**Генератор мега-промптов под любую AI-модель 2026 года**

*Claude Opus 4.7 · Gemini 3.1 · GPT-5 · o4 · DeepSeek R3*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skills-orange?style=flat-square)](https://claude.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## Что это

**Prompt Banana** — набор команд для Claude Code, которые генерируют профессиональные промпты под архитектуру конкретной модели.

Вы описываете задачу → система строит **мега-промпт** (8 000–20 000 символов), учитывая:
- синтаксис и предпочтения конкретной модели (XML для Claude, чистый текст для Gemini, без CoT для o4)
- 10-слойную архитектуру промпта (роль → контекст → цель → ограничения → формат)
- актуальные техники 2026 года из подключённой базы знаний

Никаких внешних API. Всё работает локально.

---

## Установка

Вставьте в чат Claude Code:

```
Установи Prompt Banana: склонируй репозиторий https://github.com/fsbtactic-code/promptbanana
в ~/.claude/promptbanana и запусти python ~/.claude/promptbanana/install_global.py
```

Claude выполнит клонирование, установит зависимости и скопирует команды `/promptbnn_*` глобально.
После — перезапустите Claude Code.







## Команды

| Команда | Модель | Особенность | Длина |
|---|---|---|---|
| `/promptbnn_claude_opus47` | Claude Opus 4.7 | XML-разметка, Extended Thinking | 8–16K |
| `/promptbnn_claude_sonnet46` | Claude Sonnet 4.6 | Компактный XML, агентные задачи | 4–10K |
| `/promptbnn_gemini3_1_pro` | Gemini 3.1 Pro | Чистый текст, якорение контекста | 6–12K |
| `/promptbnn_gemini3_1_advanced` | Gemini 3.1 Advanced | 20M токенов, видео, Deep Research | 8–15K |
| `/promptbnn_gpt5` | GPT-5 Chat | Markdown, Canvas, мультиагент | 8–18K |
| `/promptbnn_o4` | o4 / o4-mini | **Без CoT.** Цель + ограничения | 3–8K |
| `/promptbnn_deepseek_r3` | DeepSeek R3/R2 | **Без CoT.** Ультра-лаконично | 2–6K |

### Пример

```
/promptbnn_gemini3_1_pro создай промпт для анализа 50-страничного PDF контракта

/promptbnn_claude_opus47 промпт для агента по автоматизации отчётов в Google Sheets

/promptbnn_o4 промпт для оптимизации алгоритма поиска
```

---

## Структура проекта

```
promptbanana/
├── .claude/
│   └── commands/              ← Команды (7 моделей)
│       ├── promptbnn_claude_opus47.md
│       ├── promptbnn_claude_sonnet46.md
│       ├── promptbnn_gemini3_1_pro.md
│       ├── promptbnn_gemini3_1_advanced.md
│       ├── promptbnn_gpt5.md
│       ├── promptbnn_o4.md
│       └── promptbnn_deepseek_r3.md
│
├── sources/                   ← Ваши .md файлы с базой (не в git)
├── index/                     ← Поисковый индекс (генерируется)
│
├── CLAUDE.md                  ← Автопоиск по базе знаний
├── install_global.py          ← Глобальный установщик
├── build_index.py             ← Построение индекса
├── search.py                  ← Поиск по базе
├── anonymize_sources.py       ← Скрытие имён файлов
└── requirements.txt
```

### Как работает поиск по базе

1. `build_index.py` читает `.md` файлы из `sources/`, нарезает на чанки по 400 слов
2. Строит TF-IDF матрицу (50 000 токенов, рус+eng) через scikit-learn
3. При вызове команды `search.py` находит топ-5 релевантных фрагментов
4. Claude использует их при генерации промпта

**Почему без векторной БД:**
- Нет зависимости от внешних API
- Мгновенный поиск (<2 сек) по 500+ фрагментам
- Работает полностью офлайн

---

## Принципы генерации промптов

Каждая команда реализует **10-слойную архитектуру Prompt Architect Omega v5.0**:

| Слой | Назначение |
|---|---|
| 1 | System Override — перехват дефолтной личности модели |
| 2 | Interface Activation — Canvas, Artifacts, Code Interpreter |
| 3 | Dynamic Context — входные данные и граф знаний |
| 4 | Terminal Goal — кристальная формулировка цели |
| 5 | Thinking Protocol — только для неreasoning моделей |
| 6 | Execution Pipeline — фазы с паузами и подтверждением |
| 7 | State Machine — удержание контекста |
| 8 | Constraint Matrix — матрица запретов и антипаттернов |
| 9 | Format Contract — точная топология вывода |
| 10 | Ignition Trigger — активационная фраза |

**Ключевое правило 2026:** Reasoning-модели (o4, DeepSeek R3) получают **только** слои 3, 4, 8, 9 — без CoT инструкций. CoT-инструкции ломают нативный RL-алгоритм reasoning-моделей.

---

## Требования

- Python 3.10+
- scikit-learn >= 1.4.0
- numpy >= 1.26.0
- Claude Code

---

## Лицензия

MIT — используйте свободно.

---

<div align="center">
Made with 🍌 by <a href="https://github.com/fsbtactic-code">fsbtactic-code</a>
</div>
