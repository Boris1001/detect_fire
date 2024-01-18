import numpy as np
import os
import cv2
from ultralytics import YOLO
import json
import subprocess
from urllib.parse import urlparse

# Чтение конфигурации из JSON файла
with open('config.json', 'r') as file:
    config = json.load(file)
    
camera_url = config['camera_url']

# Извлечение IP-адреса из URL
parsed_url = urlparse(camera_url)
camera_ip = parsed_url.hostname

# Использование настроек из конфигурации
video_url = config['camera_url']


# Загрузка модели и получение прогноза
def extract_objects(input_path, crop_dir_name="result", resize_dim=(64, 64)):
    model = YOLO('best_2_classes_50_n.pt')
    cap = cv2.VideoCapture(input_path)
    assert cap.isOpened(), "Error reading video file"
    
    if not os.path.exists(crop_dir_name):
        os.mkdir(crop_dir_name)

    idx = 0
    extracted_images = []
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break

        results = model.predict(im0, show=False, conf=0.5, project = 'result')
        boxes = results[0].boxes.xyxy.cpu().tolist()

        if boxes:
            for box in boxes:
                idx += 1
                crop_obj = im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                resized_crop_obj = cv2.resize(crop_obj, resize_dim)
                cv2.imwrite(os.path.join(crop_dir_name, f"{idx}.jpg"), crop_obj)
                extracted_images.append(resized_crop_obj)
                
                if len(extracted_images) >= 10:
                    return extracted_images[:10]

    cap.release()


#Для YOLO модели:
#Запуск видео
def process_video_and_predict_fire(input_path):
    sequence = extract_objects(input_path)
    if sequence and len(sequence) == 30:
        print('Fire')
    else:
        print("Недостаточно данных для анализа")

'''
#Для lstm модели:
def predict_fire(sequence):
    data = np.vstack(sequence)

    if data.size == 30 * 64 * 64 * 3:
        data = data.reshape(-1, 30, 64, 64, 3)
        predictions = model_LSTM.predict(data)
        if predictions[0][0] >= 0.5:
            print('FIRE!!!')
        else:
            print('No fire.')
 #       print("Predicted fire probability:", round(predictions[0][0], 2))
    else:
        print("Невозможно выполнить предсказание, неверное количество данных")


def process_video_and_predict_fire(input_path):
    sequence = extract_objects(input_path)
    if sequence and len(sequence) == 10:
        predict_fire(sequence)
    else:
        print("Недостаточно данных для анализа")

'''

# Прверка по пингу

def ping_host(host):
    response = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE)
    return response.returncode == 0

if ping_host(camera_ip):
    print(f"{camera_ip} is reachable")
    process_video_and_predict_fire(video_url)
else:
    print(f"{camera_ip} is not reachable")
