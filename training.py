#coding=utf-8
import os
from six.moves import cPickle
from matplotlib import pyplot
from scipy.misc import toimage
import numpy as np
from PIL import Image
import random

def chunks(lst, count):
    for i in range(0,len(lst),count):
        yield lst[i:i+count]


def conserve_training_files():
    shuffle_list = []
    count_part = 1
    dct = {"data": [], "label": []}
    for i in range(0,10):
        print("Выгрузка фотографий -- %s" % i)
        path = "/home/sfilatov96/hands_dataset/%s/" % i
        listOfFiles = os.listdir(path)
        for l in listOfFiles:
            print("Photo %s Folder %s" % (l,i))
            shuffle_list.append((path+l,i))
    random.shuffle(shuffle_list)
    countOfFiles = len(shuffle_list)
    print("Всего %s" % countOfFiles)
    i = 0
    for l,k in shuffle_list:
        try:
            file = l
            img = Image.open(fp=file)
            new_width = 32
            new_height = 32
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

            lst = np.array(img.getdata()).transpose()
            r,g,b = lst

            r = list(r)
            r = list(chunks(r,32))
            r = list(chunks(r,32))
            g = list(g)
            g = list(chunks(g,32))
            g = list(chunks(g,32))
            b = list(b)
            b = list(chunks(b,32))
            b = list(chunks(b,32))
            lst = [r[0],g[0],b[0]]

            dct["data"].append(lst)
            dct["label"].append(k)

            print("Number %s/%s Path %s" % (i,countOfFiles,l))
        except Exception as e:
            #print("Error %s" % i,e)
            pass
        if i % 5000 == 0 or i == countOfFiles:
            fs = "shuffle/part%s.pkl" % (count_part)
            fp = open(fs, 'wb')
            cPickle.dump(dct, fp, 2)
            fp.close()
            dct = {"data": [], "label": []}
            count_part += 1
        i += 1


def conserve_test_files(live=False):
    for j in range(1,6):
        #j = int(input())
        if live:
            path = "/home/sfilatov96/live_dataset/%s/" % j
            fs = "%s_live.pkl" % j
        else:
            path = "/home/sfilatov96/test_dataset/%s_test/" % j
            fs = "%s_test.pkl" % j

        listOfFiles = os.listdir(path)

        countOfFiles = len(listOfFiles)

        print("Gesture %s" % j)
        dct = {"data": [], "label": []}


        for i in range(1, countOfFiles + 1):
            try:
                if not live:
                    file = "/home/sfilatov96/test_dataset/%s_test/%s_test_%s.jpg" % (j, j, i)
                else:
                    file = "/home/sfilatov96/live_dataset/%s/%s_%s.jpg" % (j, j, i)
                img = Image.open(fp=file)
                new_width = 32
                new_height = 32

                img = img.resize((new_width, new_height), Image.ANTIALIAS)

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
                lst = [r[0], g[0], b[0]]

                dct["data"].append(lst)
                dct["label"].append(j)

                print("Number %s" % i)
            except Exception as e:
                print("Error %s" % i,e)

        fp = open(fs, 'wb')
        cPickle.dump(dct, fp, 2)
        fp.close()



def conserve_vk_files():
    path = "/home/sfilatov96/vk_dataset/"

    listOfFiles = os.listdir(path)

    countOfFiles = len(listOfFiles)

    print("Gesture ")
    dct = {"data": [], "label": []}

    fs = "vk.pkl"

    for i in listOfFiles:
        try:
            file = "/home/sfilatov96/vk_dataset/%s.jpg" %  i
            img = Image.open(fp=file)
            new_width = 32
            new_height = 32

            img = img.resize((new_width, new_height), Image.ANTIALIAS)

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
            lst = [r[0], g[0], b[0]]

            dct["data"].append(lst)
            dct["label"].append(2)

            print("Number %s" % i)
        except:
            print("Error %s" % i)

    with open(fs, 'wb') as fp:
        cPickle.dump(dct, fp, 2)



conserve_training_files()
