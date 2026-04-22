# 🍌 Prompt Banana — Web Edition

Эта папка содержит **автономные системные промпты** для генерации мега-промптов прямо в браузере — без Claude Code, установки и терминала.

## Как использовать

### Вариант A — Claude.ai Projects (рекомендуется)

1. Откройте [claude.ai/projects](https://claude.ai/projects) → **New Project**
2. В разделе **Project instructions** вставьте содержимое нужного файла
3. В чате напишите вашу задачу — Claude сгенерирует мега-промпт

### Вариант B — одноразовый чат

Вставьте содержимое файла как **первое сообщение** в новый чат, затем опишите задачу.

---

## Файлы

| Файл | Для какой модели | Интерфейс |
|---|---|---|
| `claude_opus47.md` | Claude Opus 4.7 | claude.ai |
| `claude_sonnet46.md` | Claude Sonnet 4.6 | claude.ai |
| `gemini_3_1_pro.md` | Gemini 3.1 Pro | gemini.google.com |
| `gemini_3_1_advanced.md` | Gemini 3.1 Advanced | gemini.google.com |
| `gpt5.md` | GPT-5 Chat | chatgpt.com |
| `o4.md` | o4 / o4-mini | chatgpt.com |
| `deepseek_r3.md` | DeepSeek R3 | chat.deepseek.com |

---

## Пример

Открываете `gemini_3_1_pro.md`, копируете текст, вставляете в Project Instructions на claude.ai. Затем пишете в чат:

```
Мне нужен промпт для анализа конкурентов в нише SaaS
```

Claude генерирует полный мега-промпт (6–12K символов) специально под архитектуру Gemini 3.1 Pro.

---

## Отличие от Claude Code версии

| | Claude Code `/promptbnn_*` | Web `web/*.md` |
|---|---|---|
| Поиск по базе| ✅ 50 документов | ✅ Встроен в промпт |
| Установка | git clone + python | Не нужна |
| Интерфейс | Claude Code terminal | Любой браузер |
| Качество | Максимум | Максимум |
