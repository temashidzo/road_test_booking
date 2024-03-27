#!/bin/bash

# Максимальное разрешенное количество процессов vscode-server
MAX_ALLOWED_PROCESSES=10

echo "Поиск процессов vscode-server..."

# Получаем список PID процессов vscode-server
VSCODE_PIDS=$(pgrep -f 'vscode-server/bin/.*node' || echo "No processes found.")

# Если не найдено ни одного процесса, выходим из скрипта
if [ "$VSCODE_PIDS" == "No processes found." ]; then
    echo "Процессы vscode-server не обнаружены."
    exit 0
fi

# Подсчитываем количество процессов
VSCODE_PROCESSES_COUNT=$(echo "$VSCODE_PIDS" | wc -l)

echo "Найдено $VSCODE_PROCESSES_COUNT процессов vscode-server."

# Если количество процессов превышает максимально допустимое, завершаем их
if [ "$VSCODE_PROCESSES_COUNT" -gt "$MAX_ALLOWED_PROCESSES" ]; then
    echo "Количество процессов превышает максимально разрешенные $MAX_ALLOWED_PROCESSES."
    # Убиваем процессы
    TO_KILL=$(($VSCODE_PROCESSES_COUNT - $MAX_ALLOWED_PROCESSES))
    echo "Завершение $TO_KILL лишних процессов..."
    echo "$VSCODE_PIDS" | head -n "$TO_KILL" | xargs -r kill
    echo "Лишние процессы vscode-server были завершены."
else
    echo "Количество процессов vscode-server в пределах нормы."
fi
