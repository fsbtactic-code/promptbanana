Установи инструмент Prompt Banana из репозитория на GitHub.

Шаги:

1. Склонируй репозиторий в папку ~/.claude/promptbanana:
   git clone https://github.com/fsbtactic-code/promptbanana ~/.claude/promptbanana

2. Запусти установщик:
   python ~/.claude/promptbanana/install_global.py

   Если команда python не найдена — попробуй python3.
   Если git не установлен — скачай архив вручную:
   https://github.com/fsbtactic-code/promptbanana/archive/refs/heads/main.zip
   Распакуй в ~/.claude/promptbanana/ и запусти python install_global.py

3. Проверь что установка прошла успешно — должны появиться файлы:
   Windows: %USERPROFILE%\.claude\commands\promptbnn_claude_opus47.md
   Mac/Linux: ~/.claude/commands/promptbnn_claude_opus47.md

4. Сообщи пользователю об успешной установке и выведи список доступных команд:
   /promptbnn_claude_opus47
   /promptbnn_claude_sonnet46
   /promptbnn_gemini3_1_pro
   /promptbnn_gemini3_1_advanced
   /promptbnn_gpt5
   /promptbnn_o4
   /promptbnn_deepseek_r3

   Напомни: перезапустить Claude Code после установки.
