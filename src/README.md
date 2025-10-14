# Motion Heatmap

Motion Heatmap - мини-проект для анализа движения в видео и построения тепловой карты активности.
Программа использует OpenCV для выделения движущихся областей и Matplotlib для визуализации результата в виде тепловой карты, показывающей, где движение происходило чаще всего.

---

## Структура проекта
```
motion_heatmap/
├─ src/
│  ├─ heatmap.py     
│  └─ cli.py                   
├─ examples/                   
├─ output/                     
├─ logs/                       
├─ requirements.txt
├─ Dockerfile
└─ README.md

```
---

## Локальный запуск
```bash
git clone <https://github.com/Davidmasle/motion_heatmap.git>

cd motion_heatmap

docker build -t motion_heatmap .

docker run -it --rm \
    -v "$(pwd)/examples:/app/examples" \
    -v "$(pwd)/output:/app/output" \
    motion_heatmap \
    python -m src.cli --video examples/video.mp4 --output output/result.png
```
