#coding=utf-8
import numpy as np
from keras.datasets import cifar10
from keras.models import load_model
from keras.utils import np_utils
import matplotlib.pyplot as plt
import scipy.misc as smp
from PIL import Image
import cv2
import os


def chunks(lst, count):
    for i in range(0,len(lst),count):
        yield lst[i:i+count]

def get_from_webcam(frame):
    img = Image.fromarray(frame)
    new_width = 32
    new_height = 32

    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    print

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
    # plt.imshow(smp.toimage(np.array(lst)))
    # plt.show()
    # print np.array(lst)
    return np.array(lst)
#


# Оцениваем качество обучения модели на тестовых данных
# scores = model.evaluate(X_test, Y_test, verbose=0)
# print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))
model = load_model("gesture_model4.h5")
cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()


    # Y_test = np_utils.to_categorical(y_test, nb_classes)
    x = 500
    y = 500
    w = 300
    h = 500
    cv2.rectangle(frame, (x - w / 2, y - h / 2), (x + w / 2, y + h / 2), (255, 0, 0), 2)
    cv2.imshow('img', frame)
    frame = frame[x - w / 2: x + w / 2, y - h / 2: y + h / 2]
    # Display the resulting frame
    cv2.imshow('frame',frame)
    #if cv2.waitKey(1) & 0xFF == ord('p'):
    X_test = get_from_webcam(frame)
    X_test = X_test.astype('float32')
    X_test /= 255
    res = model.predict_classes(np.array([X_test]), verbose=0)
    print(res[0] + 1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



