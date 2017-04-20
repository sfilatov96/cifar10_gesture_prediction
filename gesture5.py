#coding=utf8
from six.moves import cPickle as pick
import numpy as np
import os
from keras.utils import np_utils
from random import shuffle

gesture_symbols = {
    0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
    "а": 10, "б": 11, "в": 12, "г": 13, "д": 14, "е": 15, "ё": 16, "ж": 17, "з": 18,
    "и": 19, "й": 20, "к": 21, "л": 22, "м": 23, "н": 24, "о": 25, "п": 26, "р": 27,
    "с": 28, "т": 29, "у": 30, "ф": 31, "х": 32, "ц": 33, "ч": 34, "ш": 35, "щ": 36,
    "ъ": 37, "ы": 38, "ь": 39, "э": 40, "ю": 41, "я": 42, "*": 43
}



def get_data_from_pkl(i=None,part=None,test=False,vk=False,live=False):
    if test:
        fs = open("saving_models/%s_test.pkl" % i, "rb")
    elif live:
        fs = open("saving_models/%s_live.pkl" % i, "rb")
    elif vk:
        fs = open("saving_models/vk.pkl" , "rb")
    elif i:
        fs = open("saving_models/%s/%s" % (i,part),"rb")
    else:
        fs = open("saving_models/shuffle/%s" %  part, "rb")
    dct = pick.load(fs)
    print("Готово!")
    return (dct["data"], (dct["label"]))



def get_part():
    print("Выгрузка сериализованных данных ")
    path = "saving_models/shuffle/"
    listOfFiles = os.listdir(path)
    data = []
    label = []
    for e,l in enumerate(listOfFiles):
        if e == 5:
            break
        print("part: %s" % l)
        buf_data, buf_label = get_data_from_pkl( part=l)
        data += buf_data
        label += buf_label
    return data,label

def get_training_data():
    data, label = get_part()
    data = np.array(data)
    label = np.array(label)
    X_train = data.astype('float32')
    X_train /= 255
    Y_train = np_utils.to_categorical(label, 5)
    print("Суммарно:", len(data),len(label))
    return X_train,Y_train

def get_test_data():
    data, label = get_data_from_pkl(1,test=True)
    for i in range(2, 6):
            buf_data, buf_label = get_data_from_pkl(i,test=True)
            data += buf_data
            label += buf_label

    print("Суммарно:", len(data), len(label))
    print(np.array(data), np.array(label))
    return (np.array(data), np.array(label))

def get_vk_data():
    data, label = get_data_from_pkl(1, vk=True)
    print("Суммарно:", len(data), len(label))
    print(np.array(data), np.array(label))
    return (np.array(data), np.array(label))


def get_live_data():
    data, label = get_data_from_pkl(1,live=True)
    for i in range(2, 6):
            buf_data, buf_label = get_data_from_pkl(i,live=True)
            data += buf_data
            label += buf_label

    print("Суммарно:", len(data), len(label))
    return (np.array(data), np.array(label))


def get_part_generator():
    nb_classes = 20
    shuffle_list =[]
    path = "saving_models/shuffle/"
    listOfFiles = os.listdir(path)
    for l in listOfFiles:
        shuffle_list.append(l)
        print("Выгрузка сериализованных данных -- %s" % l)
    print shuffle_list
    shuffle(shuffle_list)
    shuffle(shuffle_list)
    shuffle(shuffle_list)
    print shuffle_list
    while True:
        for l in shuffle_list:
            print("part: %s" % l)
            data, label = get_data_from_pkl(part=l)
            print label
            for i in range(len(label)):
                if label[i] > 15:
                    label[i] -= 1
            data = np.array(data)
            label = np.array(label)
            X_train = data.astype('float32')
            X_train /= 255
            Y_train = np_utils.to_categorical(label, nb_classes)
            for ind in range(0,len(X_train), 32):
                print ind
                yield np.array(X_train[ind:ind+32]), np.array(Y_train[ind:ind+32])