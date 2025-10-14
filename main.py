import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def motion_heatmap(video_path="video.mp4", save_path="heatmap_output.png", show_frames=False):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Файл {video_path} не найден")

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Не удалось считать видео")

    # первый кадр в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    heatmap = np.zeros_like(gray, dtype=np.float32)

    fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)

        # Бинаризация маски (чтобы не учитывать тени)
        _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

        kernel = np.ones((3,3), np.uint8)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_DILATE, kernel)

        heatmap += fgmask.astype(np.float32)

        frame_count += 1

        if show_frames:
            cv2.imshow("Frame", frame)
            cv2.imshow("Motion Mask", fgmask)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

    print(f"[INFO] Обработано кадров: {frame_count}")

    # Нормализация тепловой карты
    heatmap = cv2.GaussianBlur(heatmap, (11,11), 0)
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = heatmap.astype(np.uint8)

    # Цветовая карта
    colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Сохраняем результат
    cv2.imwrite(save_path, colored)
    print(f"[INFO] Тепловая карта сохранена как {save_path}")

    plt.figure(figsize=(10,6))
    plt.title("Motion Heatmap")
    plt.imshow(cv2.cvtColor(colored, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    motion_heatmap("video.mp4", save_path="heatmap_result.png", show_frames=True)
