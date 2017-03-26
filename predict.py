#coding=utf-8
import numpy as np
from keras.datasets import cifar10
from keras.models import load_model
from keras.utils import np_utils
import matplotlib.pyplot as plt
from PIL import Image
import scipy.misc as smp

from src.gesture5 import get_test_data,get_vk_data,get_live_data






(X_test, y_test) = get_live_data()

real = X_test

nb_classes = 10


X_test = X_test.astype('float32')
X_test /= 255

Y_test = np_utils.to_categorical(y_test, nb_classes)

model = load_model("gesture10_model1.h5")


# Оцениваем качество обучения модели на тестовых данных
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))

res = model.predict_classes(X_test)


print(y_test)
print(res)

plt.imshow(smp.toimage(X_test[5]))
plt.show()

