# Используем лёгкий базовый образ Python
FROM python:3.12-slim

# Устанавливаем зависимости для OpenCV и Matplotlib (без GUI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем зависимости отдельно (для кэширования)
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной проект
COPY . .

# Создаём папки, чтобы не было ошибок при запуске
RUN mkdir -p logs output examples

# Указываем команду по умолчанию
# Можно задать видео через переменные окружения
ENV VIDEO_PATH="examples/demo.mp4"
ENV OUTPUT_PATH="output/heatmap_result.png"

# По умолчанию — запуск CLI
CMD ["python", "-m", "src.cli", "--video", "examples/demo.mp4", "--output", "output/heatmap_result.png"]
