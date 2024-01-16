# detect_fire
MVP for determining fire using the object detection method and screening out false alarms using the gorenje recognition analysis on a series of frames mediated by the lstm model.

Принимает на вход путь к тестируемому видео.

Пример запуска:

python detect_fire.py -u video/test_video_no_fire_4.mp4

Ссылка на модель lstm https://drive.google.com/file/d/1RKHdaOe7yx6dtWXZ31iVaa-Tmfkyk8Xe/view?usp=drive_link

Ссылка на модель Yolo https://drive.google.com/file/d/11od9cQS5vrhm8bqCI_ZfVWvhuUPDm02t/view?usp=drive_link

Модели скачать в каталог с файлом detect_fire.py

Ссылка на тестовое видео с огнём   https://drive.google.com/file/d/1nZs7sXOwf8qSe8eTQyhXiB_OSp2789Pk/view?usp=drive_link

Ссылка на тестовое видео без огня   https://drive.google.com/file/d/1xH9zvdroQfKrvUfjRxVAeDdLD1WTG9d7/view?usp=drive_link
