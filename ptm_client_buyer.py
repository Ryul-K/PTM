from socket import *
import json
import time

def helper_send(sock, data):
    try:
        serialized = json.dumps(data)
    except(TypeError, ValueError):
        raise Exception('Cannot send JSON-serializable data')

    sock.send(serialized.encode('utf-8'))

def helper_recv(sock):
    CONST_RECV_MAX_SIZE = 4096
    data = sock.recv(CONST_RECV_MAX_SIZE)
    try:
        deserialized = json.loads(data)
    except(TypeError, ValueError):
        raise Exception('Data is not in JSON format')

    return deserialized

class Client(object):
    socket = None

    def __del__(self):
        self.close()

    def connect(self, host, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((host, port))

        self.socket.setblocking(True)
        return self

    def send(self, data):
        if not self.socket:
            raise Exception('Need a connection first before sending data')
        helper_send(self.socket, data)
        return self

    def recv(self):
        if not self.socket:
            raise Exception('Need a connection first before receiving data')
        return helper_recv(self.socket)

    def recv_and_close(self):
        data = self.recv()
        self.close()
        return data

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None


# PTM, acting as a client, makes requests to Blockchain Interface (BI)
if __name__ == "__main__":
    port = 8888
    host = '15.164.215.166' # localhost for test

    IF_ID_onboard = {
	    "type" : "REQ",
	    "interface" : "IF.ID.onboard",
	    "parameter" : "password"
    }
    IF_ID_create = {
        "type" : "REQ",
        "interface" : "IF.ID.create",
        "parameter" : ""
    }

    IF_ID_retrieve = {
        "type" : "REQ",
        "interface" : "IF.ID.retrieve",
        "parameter" : ""
    }

    IF_TR_offer = {
        "type" : "REQ",
        "interface" : "IF.TR.offer",
        "parameter" : '{"price":"1000", "quantity":"500", "hour":"4"}'
    }

    IF_TR_order = {
        "type" : "REQ",
        "interface" : "IF.TR.order",
        "parameter" : '{"deal": "0xa8b05f0bc681a1c95430a2d3e195a0c1646d0e236e3c4b8ab8538b50052dedf9", "quantity": "100"}'
    }

    IF_TR_browse_offers = {
        "type" : "REQ",
        "interface" : "IF.TR.browse.offers",
        "parameter" : ""
    }

    IF_TR_browse_orders = {
        "type" : "REQ",
        "interface" : "IF.TR.browse.orders",
        "parameter" : '{"deal": "0xe03070397c6d216f48e50bf393d8d90fe150430xe03070397c6d216f48e50bf393d8d90fe15043"}'
    }
    IF_TR_accept = {
        "type" : "REQ",
        "interface" : "IF.TR.accept",
        "parameter" : '{"deal": "0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6", "order": "id:bems:4ebd680f2cc1f76bdf65b5b2c2afc0d64c553279"}'
    }

    IF_TR_check = {
        "type" : "REQ",
        "interface" : "IF.TR.check",
        "parameter" : '{"deal": "0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6"}'
    }

    IF_TR_finish = {
        "type" : "REQ",
        "interface" : "IF.TR.finish",
        "parameter" : '{"deal": "0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6"}'
    }

    IF_TR_list_ongoing= {
        "type" : "REQ",
        "interface" : "IF.TR.list.ongoing",
        "parameter" : ""
    }

    IF_TR_list_finished= {
        "type" : "REQ",
        "interface" : "IF.TR.list.finished",
        "parameter" : ""
    }

    # connect to BI server
    client = Client()
    client.connect(host, port)

    print('client connected...')

    # create ID
    request = IF_ID_create
    print(f'PTM ==> BI: {request}')
    client.send(request)
    print(f'BI ==> PTM: {client.recv()}')

    # retrieve ID
    # request = IF_ID_retrieve
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    # offer deal (with own ID)
    # request = IF_TR_offer
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    # browse(list) offers
    # request = IF_TR_browse_offers
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    # order deal
    # request = IF_TR_order
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    # browse(list) orders
    # request = IF_TR_browse_orders
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    # accept an order
    # request = IF_TR_accept
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    # check the deal status
    # request = IF_TR_check
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    # check the ongoing deals
    # request = IF_TR_list_ongoing
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    # finish the deal(trade)
    # request = IF_TR_finish
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    # list finished deals
    # request = IF_TR_list_finished
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')

    client.close()
