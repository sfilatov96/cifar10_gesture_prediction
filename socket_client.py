import json
import base64
import requests
import time
import os
from socket import *

PHOTOS_PATH = '/home/sfilatov96/vk_dataset/'
RATE = 0.01


def test_photo(photo_path):
    print photo_path
    file = open(photo_path, 'rb')
    l = file.read()
    print len(l)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('62.109.1.48', 6000))
    sock.send(l+"\r\r\n")

    data = sock.recv(1024)
    print data
    sock.close()





def get_files_in_path(path):
    return [file for file in os.listdir(path) if not file.startswith('.')]


if __name__ == '__main__':
    for photo_path in get_files_in_path(PHOTOS_PATH):
        test_photo(PHOTOS_PATH+photo_path)
        if RATE:
            time.sleep(RATE)
