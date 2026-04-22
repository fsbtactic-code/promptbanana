# 🍌 Prompt Banana — Web Edition

Системные промпты для генерации мега-промптов прямо в браузере. Без установки, без терминала.

---

## ⚡ Быстрая установка через .skill файл (Claude.ai)

1. Запустите `python package.py` — создаст папку `dist/` с файлами
2. Откройте [claude.ai](https://claude.ai) → **Settings** → **Skills** → **Upload**
3. Выберите нужный `.skill` файл из папки `dist/`

| Файл | Модель |
|---|---|
| `prompt-banana-claude-opus47.skill` | Claude Opus 4.7 |
| `prompt-banana-claude-sonnet46.skill` | Claude Sonnet 4.6 |
| `prompt-banana-gemini-pro.skill` | Gemini 3.1 Pro |
| `prompt-banana-gemini-advanced.skill` | Gemini 3.1 Advanced |
| `prompt-banana-gpt5.skill` | GPT-5 |
| `prompt-banana-o4.skill` | o4 / o4-mini |
| `prompt-banana-deepseek-r3.skill` | DeepSeek R3 |

> Альтернатива `.skill`: используйте `.md` файлы из папки `dist/` — они тоже содержат YAML frontmatter.

---

## Ручная установка (если нет доступа к .skill)



### Claude.ai → через Projects (постоянно)

Самый удобный способ — создать отдельный **Project** для каждой модели:

1. Откройте [claude.ai](https://claude.ai) → нажмите **Projects** в левом меню
2. **+ New Project** → дайте название (например, "Prompt Banana — Opus 4.7")
3. Нажмите **⚙ Project Settings** → раздел **Project Instructions**
4. Откройте нужный файл по ссылке ниже → **выделите всё** (Ctrl+A) → **скопируйте**
5. Вставьте в поле Project Instructions → **Save**

Теперь каждый новый чат в этом проекте автоматически использует промпт-архитектор.

**Файлы для Claude:**
- [claude_opus47.md](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/claude_opus47.md) — для генерации промптов под Claude Opus 4.7
- [claude_sonnet46.md](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/claude_sonnet46.md) — для генерации промптов под Claude Sonnet 4.6

**Использование после установки:**
Откройте нужный Project → напишите вашу задачу → получите мега-промпт.

---

### ChatGPT → через Custom GPT (постоянно)

1. Откройте [chatgpt.com](https://chatgpt.com) → нажмите **Explore GPTs** → **+ Create**
2. Перейдите на вкладку **Configure**
3. В поле **Instructions** вставьте содержимое нужного файла:
   - [gpt5.md](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/gpt5.md) — для GPT-5
   - [o4.md](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/o4.md) — для o4 / o4-mini
4. Дайте GPT название → **Save** → **Only me** (приватный)

Теперь этот Custom GPT всегда работает как Prompt Architect для нужной модели.

**Быстрый вариант (одноразово):**
Просто вставьте файл первым сообщением в новый чат, затем опишите задачу.

---

### Gemini → через Gems (постоянно)

1. Откройте [gemini.google.com](https://gemini.google.com) → нажмите **Gems** в левом меню
2. **+ New Gem** → дайте название
3. В поле **Instructions** вставьте содержимое:
   - [gemini_3_1_pro.md](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/gemini_3_1_pro.md) — для Gemini 3.1 Pro
   - [gemini_3_1_advanced.md](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/gemini_3_1_advanced.md) — для Gemini Advanced
4. **Save** → откройте этот Gem для работы

---

### DeepSeek → одноразово (Gems пока нет)

DeepSeek пока не поддерживает сохранённые системные промпты в веб-интерфейсе.

1. Откройте [chat.deepseek.com](https://chat.deepseek.com) → новый чат
2. Включите **DeepThink (R1)** режим (иконка в интерфейсе)
3. Вставьте содержимое [deepseek_r3.md](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/deepseek_r3.md) первым сообщением
4. Опишите задачу в следующем сообщении

---

## Быстрые ссылки на файлы

| Файл | Скопировать содержимое |
|---|---|
| Claude Opus 4.7 | [открыть](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/claude_opus47.md) |
| Claude Sonnet 4.6 | [открыть](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/claude_sonnet46.md) |
| Gemini 3.1 Pro | [открыть](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/gemini_3_1_pro.md) |
| Gemini 3.1 Advanced | [открыть](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/gemini_3_1_advanced.md) |
| GPT-5 | [открыть](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/gpt5.md) |
| o4 / o4-mini | [открыть](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/o4.md) |
| DeepSeek R3 | [открыть](https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/web/deepseek_r3.md) |

---

## Пример использования

После установки в Claude.ai Project пишете:

```
Сделай промпт для плана публикаций в Threads для маркетолога
```

Claude генерирует полный мега-промпт (8–16K символов) под выбранную модель с 10-слойной архитектурой, который вы копируете и используете.
