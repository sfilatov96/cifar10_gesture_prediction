#coding=utf8
from six.moves import cPickle as pick
import numpy as np
import os

def get_data_from_pkl(i,part=None,test=False,vk=False,live=False):
    if test:
        fs = open("saving_models/%s_test.pkl" % i, "rb")
    elif live:
        fs = open("saving_models/%s_live.pkl" % i, "rb")
    elif vk:
        fs = open("saving_models/vk.pkl" , "rb")
    else:
        fs = open("saving_models/%s/%s" % (i,part),"rb")
    dct = pick.load(fs,encoding="bytes")
    print("Готово!")
    for j in range(len(dct["label"])):
        dct["label"][j] = [dct["label"][j] - 1]
    return (dct["data"], (dct["label"]))



def get_part(i):
    print("Выгрузка сериализованных данных -- %s" % i)
    path = "saving_models/%s/" % i
    listOfFiles = os.listdir(path)
    data = []
    label = []
    for l in listOfFiles:
        print("part: %s" % l)
        buf_data, buf_label = get_data_from_pkl(i, part=l)
        data += buf_data
        label += buf_label
    return data,label

def get_training_data():
    data, label = get_part(1)

    for i in range(2,6):
        buf_data,buf_label = get_part(i)
        data += buf_data
        label += buf_label

    print("Суммарно:", len(data),len(label))
    #print (np.array(data),np.array(label))
    return (np.array(data),np.array(label))

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