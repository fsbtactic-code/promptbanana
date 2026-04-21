# Установка Prompt Banana

Скопируйте **весь текст ниже** и вставьте в чат Claude Code:

---

```
Установи Prompt Banana — набор команд для генерации профессиональных промптов.

ЗАДАЧА: выполни все шаги ниже последовательно. При любой ошибке — исправь и продолжи. Не останавливайся на ошибках, ищи обходной путь.


ШАГ 1 — Определи рабочую команду Python
Запусти: python --version
Если ошибка или версия < 3 — попробуй: python3 --version
Запомни какая команда работает (python или python3). Используй её во всех следующих шагах.


ШАГ 2 — Скачай и запусти установщик

Вариант A (стандартный):
[python/python3] -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/install_global.py').read().decode())"

Если ошибка SSL — Вариант B:
[python/python3] -c "import ssl; ssl._create_default_https_context = ssl._create_unverified_context; import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/install_global.py').read().decode())"

Если не работает ни один вариант — Вариант C:
curl -o install_global.py https://raw.githubusercontent.com/fsbtactic-code/promptbanana/main/install_global.py
[python/python3] install_global.py


ШАГ 3 — Проверь результат
Проверь наличие файлов:
- Windows: %USERPROFILE%\.claude\commands\promptbnn_claude_opus47.md
- Mac/Linux: ~/.claude/commands/promptbnn_claude_opus47.md

Если файлы есть — установка успешна.
Если нет — покажи ошибку из шага 2 и исправь.


ШАГ 4 — Подтверди установку
Выведи сообщение:
✅ Prompt Banana установлен. Доступные команды:
/promptbnn_claude_opus47
/promptbnn_claude_sonnet46
/promptbnn_gemini3_1_pro
/promptbnn_gemini3_1_advanced
/promptbnn_gpt5
/promptbnn_o4
/promptbnn_deepseek_r3

Затем напомни пользователю: "Перезапустите Claude Code чтобы команды стали активны."
```
