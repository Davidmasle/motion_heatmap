import argparse
import logging
from src.heatmap import motion_heatmap

def main():
    parser = argparse.ArgumentParser(description="Тепловая карта движения на видео")
    parser.add_argument("--video", required=True, help="Путь к видеофайлу")
    parser.add_argument("--output", default="output/heatmap_result.png", help="Путь для сохранения результата")
    parser.add_argument("--blur", type=int, default=11, help="Степень размытия карты")
    parser.add_argument("--show", action="store_true", help="Показать процесс обработки")
    args = parser.parse_args()

    logging.basicConfig(
        filename="logs/heatmap.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )

    print(f"[INFO] Обработка видео: {args.video}")
    motion_heatmap(args.video, args.output, show_frames=args.show, blur=args.blur)
    print(f"[INFO] Результат сохранен: {args.output}")

if __name__ == "__main__":
    main()
