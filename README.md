<div align="center">

# 🍌 Prompt Banana RAG

**Локальная RAG-система для генерации идеальных промптов под любую модель 2026 года**

*Claude Opus 4.7 · Gemini 3.1 · GPT-5 · o4 · DeepSeek R3*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skills-orange?style=flat-square)](https://claude.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## Что это

**Prompt Banana RAG** — движок для генерации профессиональных промптов, заточенных под архитектуру конкретной модели.

Вы описываете задачу → система строит **мега-промпт** под выбранную модель (8 000–20 000 символов), учитывая:
- синтаксис и предпочтения конкретной модели (XML для Claude, чистый текст для Gemini, отсутствие CoT для o4)
- 10-слойную архитектуру промпта (роль → контекст → цель → ограничения → формат)
- актуальные техники 2026 года из локальной базы знаний

Никаких внешних API. Всё работает локально.

---

## Быстрый старт — установка одним промптом в Claude Code

Откройте терминал в Claude Code и вставьте:

```
Установи Prompt Banana RAG:

1. Склонируй репозиторий: git clone https://github.com/fsbtactic-code/promptbanana .
2. Установи зависимости: pip install -r requirements.txt
3. Создай папку sources/ и добавь в неё свои .md файлы с базой знаний
4. Запусти: python setup.py
5. Проверь: python search.py "chain of thought"

После успешной установки скажи мне об этом и покажи список доступных /prompt команд.
```

> **Примечание:** Если хотите использовать собственную базу знаний — положите `.md` файлы в папку `sources/` перед запуском `setup.py`. Он предложит анонимизировать имена файлов автоматически.

---

## Скилл-команды (slash commands)

После установки в Claude Code доступны команды. Укажите команду + описание задачи:

| Команда | Модель | Синтаксис промпта | Длина |
|---|---|---|---|
| `/promptbnn_claude_opus47` | Claude Opus 4.7 | XML-разметка, Extended Thinking | 8–16K |
| `/promptbnn_claude_sonnet46` | Claude Sonnet 4.6 | Компактный XML, агентные задачи | 4–10K |
| `/promptbnn_gemini3_1_pro` | Gemini 3.1 Pro | Чистый текст, якорение контекста | 6–12K |
| `/promptbnn_gemini3_1_advanced` | Gemini 3.1 Advanced | 20M токенов, видео, Deep Research | 8–15K |
| `/promptbnn_gpt5` | GPT-5 Chat | Markdown, Canvas, мультиагентные дебаты | 8–18K |
| `/promptbnn_o4` | o4 / o4-mini | **Без CoT.** Только цель + ограничения | 3–8K |
| `/promptbnn_deepseek_r3` | DeepSeek R3/R2 | **Без CoT.** Ультра-лаконично, R-правила | 2–6K |

### Пример использования

```
/promptbnn_gemini3_1_pro создай промпт для анализа 50-страничного PDF контракта

/promptbnn_claude_opus47 промпт для агента по автоматизации отчётов в Google Sheets

/promptbnn_o4 промпт для решения задачи на оптимизацию алгоритма
```

---

## Архитектура

```
promptbanana/
├── .claude/
│   └── commands/              ← Скилл-файлы (7 моделей)
│       ├── promptbnn_claude_opus47.md
│       ├── promptbnn_claude_sonnet46.md
│       ├── promptbnn_gemini3_1_pro.md
│       ├── promptbnn_gemini3_1_advanced.md
│       ├── promptbnn_gpt5.md
│       ├── promptbnn_o4.md
│       └── promptbnn_deepseek_r3.md
│
├── sources/                   ← Ваши .md файлы с базой знаний (не в git)
├── index/                     ← TF-IDF индекс (генерируется, не в git)
│
├── CLAUDE.md                  ← Главный скилл: RAG-поиск по базе
├── build_index.py             ← Построение индекса
├── search.py                  ← CLI поиск по базе
├── anonymize_sources.py       ← Скрытие имён файлов источников
├── setup.py                   ← Установщик
└── requirements.txt
```

### Как работает RAG

1. `build_index.py` читает все `.md` файлы из `sources/`, чистит от Markdown-разметки, нарезает на чанки по 400 слов с перекрытием 80 слов
2. Строит TF-IDF матрицу (50 000 токенов, uni+bigrams, рус+eng) через scikit-learn
3. При вызове скилл-команды `search.py` вычисляет cosine similarity запроса с матрицей и возвращает топ-5 чанков
4. Claude использует найденные фрагменты при генерации промпта

**Почему TF-IDF, а не векторная БД:**
- Нет зависимостей от OpenAI/Gemini API для эмбеддингов
- Мгновенный поиск (<2 сек) по 500+ чанкам
- Работает полностью офлайн
- При необходимости заменяется на `sentence-transformers` без изменения CLI

---

## Принципы генерации промптов

Каждый скилл реализует **10-слойную архитектуру Prompt Architect Omega v5.0**:

| Слой | Назначение |
|---|---|
| 1 | System Override — перехват дефолтной личности модели |
| 2 | Interface Activation — Canvas, Artifacts, Code Interpreter |
| 3 | Dynamic Context — входные данные и граф знаний |
| 4 | Terminal Goal — кристальная формулировка цели |
| 5 | Thinking Protocol — только для неreasoning моделей |
| 6 | Execution Pipeline — фазы с паузами и подтверждением |
| 7 | State Machine — удержание контекста в длинных сессиях |
| 8 | Constraint Matrix — матрица запретов и антипаттернов |
| 9 | Format Contract — точная топология вывода |
| 10 | Ignition Trigger — активационная фраза |

**Ключевое правило 2026:** Reasoning-модели (o4, DeepSeek R3) получают **только** слои 3, 4, 8, 9 — без CoT инструкций, мультиагентных блоков и примеров рассуждений. Это принципиально: CoT-инструкции ломают нативный RL-алгоритм reasoning-моделей.

---

## Требования

- Python 3.10+
- scikit-learn >= 1.4.0
- numpy >= 1.26.0
- Claude Code (для slash-команд)

---

## Лицензия

MIT — используйте свободно, атрибуция приветствуется.

---

<div align="center">
Made with 🍌 by <a href="https://github.com/fsbtactic-code">fsbtactic-code</a>
</div>
