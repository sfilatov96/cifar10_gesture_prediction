# coding=utf-8
import numpy as np
from keras.datasets import cifar10
from keras.models import load_model
from keras.utils import np_utils
import matplotlib.pyplot as plt
import scipy.misc as smp
from  scipy import ndimage
from PIL import Image
import os
import cv2

from flask import Flask
from flask import request
import json
import base64


def chunks(lst, count):
    for i in range(0, len(lst), count):
        yield lst[i:i + count]


def get_from_webcam(frame):
    img = Image.fromarray(frame)
    new_width = 32
    new_height = 32
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    img = img.rotate(-90)


    lst = np.array(img.getdata()).transpose()
    r, g, b = lst

    r = list(r)
    r = list(chunks(r, 32))
    r = list(chunks(r, 32))
    g = list(g)
    g = list(chunks(g, 32))
    g = list(chunks(g, 32))
    b = list(b)
    b = list(chunks(b, 32))
    b = list(chunks(b, 32))
    lst = [b[0], g[0], r[0]]
    #  t.show()
    # print np.array(lst)
    return np.array(lst)


app = Flask(__name__)


@app.route('/api/photo', methods=['POST'])
def photo():
    try:
        f = request.files["file"]
        photobytes = f.stream.read()
        img = cv2.imdecode(np.frombuffer(photobytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)


        X_test = get_from_webcam(img)

        X_test = X_test.astype('float32')
        X_test /= 255
        gesture = model.predict_classes(np.array([X_test]), verbose=0)

        result = {}
        result['gesture'] = gesture[0]
        print json.dumps(result)
        return json.dumps(result)
    except BaseException as e:
        print('Error: ', e)
        return json.dumps({'error': e.message})

model = load_model("gesture10_model1.h5")
app.run(host='0.0.0.0', port=5000)