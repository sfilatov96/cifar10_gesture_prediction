#coding=utf8
from os.path import splitext, getsize

from time import gmtime, strftime

from socket import *
import os
import argparse

BUFF = 1024
HOST = '127.0.0.1'
PORT = 5000
WORKERS_COUNT = 2
NCPU = 2
forks = []

status = {
    200: "200 OK",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    500: "500 Internal Server Error"
}
types = {
    ".js": "application/javascript",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".html": "text/html",
    ".png": "image/png",
    ".gif": "image/gif",
    ".css": "text/css",
    ".txt": "text/plain",
    ".swf": "application/x-shockwave-flash",
}


def handler(serversock, pid):
    while 1:
        print('waiting for connection... listening on port', PORT)
        conn, addr = serversock.accept()
        try:
            parse(conn, addr, pid)
        except Exception as e:
            print e
            conn.close()


def parse(conn, addr, pid):
    data = b""
    print("send on PID: ", pid)
    while not b"\r\n" in data:  # ждём первую строку
        tmp = conn.recv(1024)
        if not tmp:  # сокет закрыли, пустой объект
            print "vyshel"
            break
        else:

            data += tmp.decode("utf-8")
            print data

    if not data:  # данные не пришли
        return  # не обрабатываем

    udata = data
    print udata
    udata = udata.split("\r\n", 1)[0]
    print(udata.split(" ", 2))
    if len(udata.split(" ", 2)) < 3:
        pass
    else:
        method, address, protocol = udata.split(" ", 2)
        print address
        if method == "POST" and address == "/api/photo":
            send_answer(conn=conn, i=200, length=0, typ=types[".html"])
        else:
            send_answer(conn=conn, i=405, length=0, typ=types[".html"])


def send_answer(conn, i, length, typ):
    conn.send(b"HTTP/1.1 " + status[i].encode("utf-8") + b"\r\n")
    conn.send(b"Date: " + '{date}'.format(date=strftime("%a, %d %b %Y %X GMT", gmtime())).encode("utf-8") + b"\r\n")
    conn.send(b"Server: sfilatov96\r\n")
    conn.send(b"Connection: keep-alive\r\n")
    conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
    conn.send(b"Content-Length: " + str(length).encode("utf-8") + b"\r\n")
    conn.send(b"\r\n")


if __name__ == "__main__":
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
