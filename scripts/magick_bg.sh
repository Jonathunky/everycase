#!/bin/bash

# Директория с исходными файлами
INPUT_DIR="/everyphone"

# Директория для сохранения обработанных файлов
OUTPUT_DIR="/magick"

# Проверка существования директории для выходных файлов
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
fi

# Перебор всех PNG файлов в INPUT_DIR
for file in "$INPUT_DIR"/*.png; do
    # Получение только имени файла без пути
    filename=$(basename "$file")

    # Применение команды magick к файлу
    magick "$file" -fuzz 10% -transparent white "$OUTPUT_DIR/$filename"
done

echo "Обработка завершена."
