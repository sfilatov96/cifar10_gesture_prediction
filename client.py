import json
import base64
import requests
import time
import os

PHOTOS_PATH = '/home/sfilatov96/vk_dataset/'
RATE = 0.1


def test_photo(photo_path):
    print photo_path
    with open(photo_path, 'rb') as file:
        photo = base64.b64encode(file.read())
        response = requests.post(
            'http://localhost:5000/api/photo',
            data=json.dumps({'photo': photo})
        )
        print(response.text)


def get_files_in_path(path):
    return [file for file in os.listdir(path) if not file.startswith('.')]


if __name__ == '__main__':
    for photo_path in get_files_in_path(PHOTOS_PATH):
        test_photo(PHOTOS_PATH+photo_path)
        if RATE:
            time.sleep(RATE)