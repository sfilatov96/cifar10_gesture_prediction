#coding=utf-8
import numpy as np
from keras.datasets import cifar10
from keras.models import Sequential,Model,load_model
from keras.layers import Dense, Flatten, Activation
from keras.layers import Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras import optimizers
from keras.utils import np_utils
from PIL import Image
from keras.optimizers import SGD,Adagrad
from src.gesture5 import get_training_data, get_test_data,get_part_generator
from keras.applications.resnet50 import ResNet50


# Задаем seed для повторяемости результатов
np.random.seed(42)

# Загружаем данные





# def prepare():
#             (X_train, y_train) = get_training_data(i)
#             X_train = X_train.astype('float32')
#             X_train /= 255
#             Y_train = np_utils.to_categorical(y_train, nb_classes)
#             yield X_train,Y_train

# Размер мини-выборки
#batch_size = 32
# Количество классов изображений
nb_classes = 20
# Количество эпох для обучения
nb_epoch = 10
# Размер изображений
img_rows, img_cols = 32, 32
# Количество каналов в изображении: RGB
img_channels = 3

# Нормализуем данные
# (X_test, y_test) = get_test_data()
# X_test = X_test.astype('float32')
# X_test /= 255
# Y_test = np_utils.to_categorical(y_test, nb_classes)

#
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
#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.7, nesterov=True)
sgd = Adagrad(lr=0.01, epsilon=1e-08, decay=0.0)




model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=['accuracy'])
#Обучаем модель
try:
    model.fit_generator(get_part_generator(), samples_per_epoch=400000, nb_epoch=5 , nb_worker=9)
except Exception as e:
    print e

model.save(filepath="gesture20_model1.h5")


# Оцениваем качество обучения модели на тестовых данных
# scores = model.evaluate(X_test, Y_test, verbose=0)
# print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))



