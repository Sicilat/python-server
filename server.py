#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

import pickle
import socket
import threading

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        global logger
        while True:
            try:
                data = client.recv(size)
                if data:
                    #Received data
                    logger.debug("Received data from client")
                else:
                    raise Exception(logger.error("Client disconnected"))
            except:
                client.close()
                return False

def unpickle_data(tdata):
    """
    Unpickle the data from the client
    >>> unpickle_data(b'\x80\x03X\n\x00\x00\x00Easy testsq\x00.')
    "Easy tests"
    >>> unpickle_data("Easy tests")
    "Easy tests"
    """
    try:
        if isinstance(tdata, bytes): #Quick check if tdata is already bytes
            data = pickle.loads(tdata)
        else:
            data = tdata
    except:
        data = False
    return data

def pickle_data(tdata):
    """
    Pickle the data for the client
    >>> pickle_data(b'\x80\x03X\n\x00\x00\x00Easy testsq\x00.')
    b'\x80\x03X\n\x00\x00\x00Easy testsq\x00.'
    >>> pickle_data("Easy tests")
    b'\x80\x03X\n\x00\x00\x00Easy testsq\x00.'
    """
    try:
        if isinstance(tdata, bytes): #Quick check if tdata is already bytes
            data = tdata
        else:
            data = pickle.dumps(tdata)
    except:
        data = False
    return data

###Starting the logger###
try:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except:
    print("!!! Failed to launch logger !!!")
    print("!!!   Immediate shutdown    !!!")
    exit()
###End of logger starting###

logger.info("Server starting...")