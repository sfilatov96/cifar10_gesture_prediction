#coding=utf8


from socket import *
import os
import argparse
import numpy as np
from PIL import Image
import cv2
from keras.models import load_model
import json

BUFF = 1024
HOST = '192.168.1.37'
PORT = 9000
WORKERS_COUNT = 2
NCPU = 2
forks = []

# status = {
#     200: "200 OK",
#     403: "403 Forbidden",
#     404: "404 Not Found",
#     405: "405 Method Not Allowed",
#     500: "500 Internal Server Error"
# }


def handler(serversock, pid):
    while 1:
        try:
            print('waiting for connection... listening on port', PORT)
            conn, addr = serversock.accept()
            conn.settimeout(2)
            parse(conn, addr, pid)
        except:
            conn.close()


def parse(conn, addr, pid):
    data = b""
    print("send on PID: ", pid)
    while True:
        tmp = conn.recv(1024)
        data += tmp
        if "\r\r\n" in tmp:
            break

    conn.send(photo(data))
    conn.close()

def chunks(lst, count):
    for i in range(0, len(lst), count):
        yield lst[i:i + count]


def get_from_webcam(frame):
    img = Image.fromarray(frame)
    new_width = 32
    new_height = 32
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    #img = img.rotate(-90)


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






def photo(file):
    try:
        photobytes = file
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



if __name__ == "__main__":
    model = load_model("gesture10_model1.h5")
    parser = argparse.ArgumentParser(description='server')
    parser.add_argument('-p', type=int, help='port of server running')
    parser.add_argument('-r', type=str, help='root document')
    parser.add_argument('-n', type=str, help='number of CPU')
    args = vars(parser.parse_args())
    HOST = args['p'] or HOST
    NCPU = args['n'] or NCPU
    ROOT_DIR = args['r'] or ""
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    for x in range(0, WORKERS_COUNT * NCPU):
        pid = os.fork()
        forks.append(pid)
        if pid == 0:
            print('PID:', os.getpid())
            handler(serversock, os.getpid())
    serversock.close()

    for pid in forks:
        os.waitpid(pid, 0)
