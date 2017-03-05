#coding=utf-8
import numpy as np
from keras.datasets import cifar10
from keras.models import Sequential,Model,load_model
from keras.layers import Dense, Flatten, Activation
from keras.layers import Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from PIL import Image
from keras.optimizers import SGD
from src.gesture5 import get_training_data, get_test_data

# Задаем seed для повторяемости результатов
np.random.seed(42)

# Загружаем данные
(X_train, y_train) = get_training_data()
(X_test, y_test) = get_test_data()




# Размер мини-выборки
batch_size = 32
# Количество классов изображений
nb_classes = 5
# Количество эпох для обучения
nb_epoch = 10
# Размер изображений
img_rows, img_cols = 32, 32
# Количество каналов в изображении: RGB
img_channels = 3

# Нормализуем данные
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

# Преобразуем метки в категории
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

# Создаем последовательную модель

model = Sequential()
# Первый сверточный слой
model.add(Convolution2D(32, 3, 3, border_mode='same',
                        input_shape=(3, 32, 32), activation='relu'))
# Второй сверточный слой
model.add(Convolution2D(32, 3, 3, activation='relu'))
# Первый слой подвыборки
model.add(MaxPooling2D(pool_size=(2, 2)))
# Слой регуляризации Dropout
model.add(Dropout(0.25))

# Третий сверточный слой
model.add(Convolution2D(64, 3, 3, border_mode='same', activation='relu'))
# Четвертый сверточный слой
model.add(Convolution2D(64, 3, 3, activation='relu'))
# Второй слой подвыборки
model.add(MaxPooling2D(pool_size=(2, 2)))
# Слой регуляризации Dropout
model.add(Dropout(0.25))
# Слой преобразования данных из 2D представления в плоское
model.add(Flatten())
# Полносвязный слой для классификации
model.add(Dense(512, activation='relu'))
# Слой регуляризации Dropout
model.add(Dropout(0.5))
# Выходной полносвязный слой
model.add(Dense(nb_classes, activation='softmax'))

# Задаем параметры оптимизации
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=['accuracy'])
#Обучаем модель
model.fit(X_train, Y_train,batch_size=batch_size,nb_epoch=nb_epoch,validation_split=0.1,shuffle=True)

model.save(filepath="gesture_model4.h5")

# Оцениваем качество обучения модели на тестовых данных
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))



