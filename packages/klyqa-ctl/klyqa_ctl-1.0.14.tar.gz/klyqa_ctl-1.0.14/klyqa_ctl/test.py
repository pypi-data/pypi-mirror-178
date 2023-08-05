#! /usr/bin/python3.6

# -*- coding: utf-8 -*-

from test2 import *
import test2


class M:
    i: int

    def __init__(self):
        self.i = -1

    def update(self, **kwargs):
        # Walk through parsed kwargs dict and look if names in dict exists as attribute in class,
        # then apply the value in kwargs to the value in class.
        for i in kwargs:
            if hasattr(self, i):
                setattr(self, i, kwargs[i])
        pass


m = M()
a = {"i": 3}
m.update(**a)


import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(("0.0.0.0", 2228))
s.settimeout(1)
# PORT = 10801

# s.bind(('', PORT))
print("Listening for broadcast at ", s.getsockname())
BUFFER_SIZE = 4096
while True:
    try:
        data, address = s.recvfrom(BUFFER_SIZE)
    except socket.timeout:
        print("Didn't receive data! [Timeout 5s]")
        continue
print("end")
