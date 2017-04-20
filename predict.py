#coding=utf-8
from keras.models import load_model
from keras.utils import np_utils
import matplotlib.pyplot as plt
import scipy.misc as smp

from src.gesture5 import get_test_data,get_vk_data,get_live_data

gesture_symbols = {
    0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
    "а": 10, "б": 11, "в": 12, "г": 13, "д": 14, "е": 15,  "ж": 16, "з": 17,
    "и": 18, "й": 19, "к": 20, "л": 21, "м": 22, "н": 23, "о": 24, "п": 25, "р": 26,
    "с": 27, "т": 28, "у": 29, "ф": 30, "х": 31, "ц": 32, "ч": 33, "ш": 34, "щ": 35,
    "ъ": 36, "ы": 37, "ь": 38, "э": 39, "ю": 40, "я": 41, "*": 42
}

(X_test, y_test) = get_test_data()

real = X_test

nb_classes = 20


X_test = X_test.astype('float32')
X_test /= 255

Y_test = np_utils.to_categorical(y_test, nb_classes)

model = load_model("gesture20_model1.h5")


# Оцениваем качество обучения модели на тестовых данных
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))

res = model.predict_classes(X_test)


print(y_test)
print(res)

plt.imshow(smp.toimage(X_test[5]))
plt.show()

