# 🍌 Prompt Banana — Skills для Claude.ai

Скилл-пакет для генерации мега-промптов под любую AI-модель 2026 года.
Один файл — все модели: Claude, Gemini, GPT-5, o4, DeepSeek.

---

## Установка

### Шаг 1 — Скачайте файл

**[⬇ Скачать prompt-banana.zip](https://github.com/fsbtactic-code/promptbanana/raw/main/releases/prompt-banana.zip)**

### Шаг 2 — Загрузите в Claude.ai

1. Откройте [claude.ai](https://claude.ai)
2. Перейдите в **Customize → Skills**
3. Нажмите **Upload Skill**
4. Выберите скачанный `prompt-banana.zip`
5. Активируйте скилл

### Шаг 3 — Используйте

Напишите в новом чате:

```
Создай промпт для [ваша задача] под Claude Opus 4.7
```

или просто:

```
Мне нужен промпт для анализа конкурентов
```

Claude спросит целевую модель и сгенерирует готовый мега-промпт.

---

## Поддерживаемые модели

| Модель | Архитектура | Длина промпта |
|---|---|---|
| Claude Opus 4.7 | XML, 10 слоёв, Extended Thinking | 8–16K символов |
| Claude Sonnet 4.6 | Компактный XML, Tool Use | 4–10K символов |
| Gemini 3.1 Pro | Текст, якорение контекста | 6–12K символов |
| Gemini 3.1 Advanced | Deep Research, 20M токенов | 8–15K символов |
| GPT-5 | Markdown, Canvas, Рой Экспертов | 8–18K символов |
| o4 / o4-mini | 4 элемента, без CoT | 2–6K символов |
| DeepSeek R3 | R-Rules, ультра-минимал | 1.5–5K символов |

---

## Как это работает

Скилл содержит профиль каждой модели с точными правилами синтаксиса, антипаттернами и архитектурой промпта. Claude читает нужный профиль и генерирует промпт, оптимизированный под конкретную модель — правильная длина, правильный синтаксис, правильные механики.

---

## Содержимое пакета

```
prompt-banana.zip
└── prompt-banana/
    ├── Skill.md              ← главный файл (роутинг)
    ├── claude-opus47.md      ← профиль Claude Opus 4.7
    ├── claude-sonnet46.md    ← профиль Claude Sonnet 4.6
    ├── gemini-pro.md         ← профиль Gemini 3.1 Pro
    ├── gemini-advanced.md    ← профиль Gemini 3.1 Advanced
    ├── gpt5.md               ← профиль GPT-5
    ├── o4.md                 ← профиль o4 / o4-mini
    └── deepseek-r3.md        ← профиль DeepSeek R3
```
