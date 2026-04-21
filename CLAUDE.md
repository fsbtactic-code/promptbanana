# 🧠 Prompt Engineering RAG — Скилл Claude Code

## Что это

У тебя есть **локальная база знаний** из 50 материалов по промпт-инжинирингу 2026 года.
Используй её **автоматически** когда пользователь спрашивает про техники промптинга, модели, бенчмарки или best practices.

---

## 📁 Расположение базы

```
C:\Users\Alina\Documents\Банан\promptengeneer\
├── sources\       ← 50 Markdown-файлов с материалами
├── index\         ← TF-IDF индекс (после build_index.py)
├── search.py      ← Поисковый движок
└── build_index.py ← Построение индекса
```

---

## 🔍 Как использовать поиск

### Когда запускать поиск автоматически

Запускай `search.py` **без явной просьбы пользователя** если он:
- Спрашивает о технике/методе промптинга ("как работает CoT?", "что такое few-shot?")
- Упоминает конкретную модель ("Claude Opus 4.6", "Gemini 3.1", "GPT-5.2")
- Просит написать промпт или систем-промпт
- Спрашивает про бенчмарки или сравнение моделей
- Просит объяснить концепцию из области LLM

### Команды поиска

```powershell
# Стандартный поиск (топ-5 результатов)
python "C:\Users\Alina\Documents\Банан\promptengeneer\search.py" "твой запрос"

# Меньше результатов (для точечного вопроса)
python "C:\Users\Alina\Documents\Банан\promptengeneer\search.py" "запрос" --top 3

# JSON (для программной обработки)
python "C:\Users\Alina\Documents\Банан\promptengeneer\search.py" "запрос" --json

# Список всех источников базы
python "C:\Users\Alina\Documents\Банан\promptengeneer\search.py" --list-sources
```

### Примеры правильных запросов

| Вопрос пользователя | Запрос для search.py |
|---|---|
| "Как использовать chain-of-thought?" | `"chain of thought step by step reasoning"` |
| "Best practices для Claude 2026" | `"claude prompting best practices 2026"` |
| "Что такое few-shot prompting?" | `"few-shot examples in-context learning"` |
| "Как работает extended thinking?" | `"extended thinking claude reasoning"` |
| "Сравни GPT-5 и Claude Opus" | `"GPT-5 vs Claude Opus comparison benchmark"` |
| "Напиши системный промпт для агента" | `"agent system prompt instructions claude"` |
| "Что такое RAG?" | `"RAG retrieval augmented generation"` |
| "Промпт на русском?" | `"промпт инжиниринг техники примеры"` |

---

## 🔄 Первый запуск (инициализация индекса)

Если папка `index\` пуста или не существует — запусти:

```powershell
cd "C:\Users\Alina\Documents\Банан\promptengeneer"
pip install scikit-learn numpy
python build_index.py
```

Должно создать `index\index.pkl`, `index\chunks.pkl`, `index\meta.json`.

---

## 📋 Рабочий процесс при ответе на вопрос о промптинге

1. **Поиск** → `python search.py "ключевые слова запроса" --top 5`
2. **Анализ** → Читаешь топ-3 релевантных фрагмента
3. **Синтез** → Формируешь ответ на основе найденных данных
4. **Не раскрывай** названия или пути к файлам источников

### Шаблон ответа

```
Согласно материалам базы знаний:

[Твой ответ на основе найденных фрагментов]

📚 Источники: [Список файлов из results]
```

---

## ⚡ База знаний

База содержит **50 материалов** по промпт-инжинирингу, моделям 2026 года и смежным темам.
Поиск работает по содержимому — не по названиям файлов.

**Тематические кластеры:**
- Техники промптинга (CoT, few-shot, XML-разметка, structured output)
- Флагманские модели 2026: Claude Opus 4.7, Gemini 3.1, GPT-5, DeepSeek R3
- Бенчмарки и сравнения моделей
- Extended Thinking, MCP, агентные архитектуры
- RAG-системы, prompt injection, оптимизация токенов
- Claude Code и написание промптов для агентов

---

## 🚫 Когда НЕ искать

- Общие вопросы не по теме промптинга (погода, бизнес-задачи не связанные с AI)
- Когда пользователь просит написать обычный код (не промпт)
- Вопросы по Banana Parser, Instagram scraper и другим проектам
