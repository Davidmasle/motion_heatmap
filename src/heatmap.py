import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import logging

def motion_heatmap(video_path="video.mp4", save_path="heatmap_output.png", show_frames=False, blur=11):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Файл {video_path} не найден")

    logging.info(f"[INFO] Начата обработка видео: {video_path}")
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Не удалось считать видео")

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
        _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

        kernel = np.ones((3,3), np.uint8)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_DILATE, kernel)

        heatmap += fgmask.astype(np.float32)
        frame_count += 1

        if show_frames:
            cv2.imshow("Motion Mask", fgmask)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

    logging.info(f"[INFO] Обработано кадров: {frame_count}")

    heatmap = cv2.GaussianBlur(heatmap, (blur, blur), 0)
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = heatmap.astype(np.uint8)
    colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    cv2.imwrite(save_path, colored)
    logging.info(f"[INFO] Тепловая карта сохранена: {save_path}")

    plt.figure(figsize=(10,6))
    plt.title("Motion Heatmap")
    plt.imshow(cv2.cvtColor(colored, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
