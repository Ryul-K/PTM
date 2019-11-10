from socket import *
import json

def helper_send(sock, data):
    try:
        serialized = json.dumps(data)

    except(TypeError, ValueError):
        raise Exception('Cannot send JSON-serializable data')

    sock.send(serialized.encode('utf-8'))

def helper_recv(sock):
    CONST_RECV_MAX_SIZE = 1024
    data = sock.recv(CONST_RECV_MAX_SIZE)
    # print(data)
    try:
        deserialized = json.loads(data)
        # print(deserialized)
    except(TypeError, ValueError):
        raise Exception('Data is not in JSON format')

    return deserialized

class Server(object):
    backlog = 5
    client = None

    def __init__(self, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('localhost', port))
        self.socket.listen(self.backlog)

    def __del__(self):
        self.close()

    def accept(self):
        if self.client:
            self.client.close()
        self.client, self.client_addr = self.socket.accept()

        return self

    def send(self, data):
        if not self.client:
            raise Exception('Cannot send data, no client is connected')
        helper_send(self.client, data)

        return self

    def recv(self):
        if not self.client:
            raise Exception('Cannot receive data, no client is connected')

        return helper_recv(self.client)

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
        if self.socket:
            self.socket.close()
            self.socket = None

'''
-------------------- API starts -------------------
'''
def IF_ID_onboard(request):
    return {
	    "type" : "RES",
	    "interface" : "IF.ID.onboard",
	    "parameter" : {"status" : "success"}
    }

def IF_ID_retrieve(request):
    return  {'type': 'RES', 'interface': 'IF.ID.retrieve', 'parameter': 'id:bems:dc5f5ca3959409c3292f44e942b9957dd2b4de6c', 'errno': '0'}

def IF_ID_create(request):
    return  {'type': 'RES', 'interface': 'IF.ID.create', 'parameter': 'id:bems:dc5f5ca3959409c3292f44e942b9957dd2b4de6c', 'errno': '0'}

def IF_TR_offer(request):
    return  {'type': 'RES', 'interface': 'IF.TR.offer', 'parameter':
'id:deal:0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6', 'errno': '0'}

def IF_TR_order(request):
    return  {'type': 'RES', 'interface': 'IF.TR.order', 'parameter': 'True', 'errno': '0'}

def IF_TR_browse_offers(request):
    order1 = {"offerId":"0x876543", "price":500, "quantity":200, "hour":2, "tolerance":5}
    order2 = {"offerId":"0x345678", "price":800, "quantity":400, "hour":4, "tolerance":5}
    return  {'type': 'RES', 'interface': 'IF.TR.browse', 'parameter': [
    {'id': 'id:deal:0x8e4728dc498e271d8b66488284bb982f14d87ae61baaf37dce52fc125f05ef60', 'seller':
'id:bems:8f61d6654a585b2b89b2290b9de3c7c6ab543063', 'price': 50, 'quantity': '200'},
{'id': 'id:deal:0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6', 'seller':
'id:bems:dc5f5ca3959409c3292f44e942b9957dd2b4de6c', 'price': 1000, 'quantity': '500'}
], 'errno': '0'}

def IF_TR_browse_orders(request):
    order1 = {"offerId":"0x876543", "price":500, "quantity":200, "hour":2, "tolerance":5}
    order2 = {"offerId":"0x345678", "price":800, "quantity":400, "hour":4, "tolerance":5}
    return {
    'type': 'RES', 'interface': 'IF.TR.browse', 'parameter': [{'id':'id:deal:0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6', 'orderer':
'id:bems:4ebd680f2cc1f76bdf65b5b2c2afc0d64c553279', 'quantity': '20'}], 'errno': '0'}

def IF_TR_accept(request):
    return {'type': 'RES', 'interface': 'IF.TR.accept', 'parameter': 'True', 'errno': '0'}

def IF_TR_check(request):
    return {'type': 'RES', 'interface': 'IF.TR.check', 'parameter': 'established', 'errno': '0'}

def IF_TR_list_ongoing(request):
    return {'type': 'RES', 'interface': 'IF.TR.list.ongoing', 'parameter': [{'id':
'id:deal:0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6', 'seller':
'id:bems:dc5f5ca3959409c3292f44e942b9957dd2b4de6c', 'buyer': 'id:bems:4ebd680f2cc1f76bdf65b5b2c2afc0d64c553279', 'price': '1000',
'quantity': '20'}], 'errno': '0'}

def IF_TR_finish(request):
    return  {'type': 'RES', 'interface': 'IF.TR.finish', 'parameter': 'True', 'errno': '0'}

def IF_TR_list_finished(request):
    return  {'type': 'RES', 'interface': 'IF.TR.list', 'parameter':
[
{'id': 'id:deal:0x30368cf4cbd95fe7595fa699ef3ad1605758da4716645987d2b7d78bce106e45', 'seller':
'id:bems:0952f2da6727f39d133abc4f3714c1b8cec39d67', 'buyer': 'id:bems:b5f6ab90f6affaf2573c0c00f6188273b999e552', 'price':
'100000', 'quantity': '900'},
{'id': 'id:deal:0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6', 'seller':
'id:bems:dc5f5ca3959409c3292f44e942b9957dd2b4de6c', 'buyer': 'id:bems:4ebd680f2cc1f76bdf65b5b2c2afc0d64c553279', 'price':
'1000', 'quantity': '20'}
], 'errno': '0'}

'''
-------------------- API ends ---------------------
'''

# Blockchain Interface (BI), acting as a server, receives request from PTM
if __name__ == "__main__":
    port = 8888
    server = Server(port)

    while True:
        server.accept()
        data = server.recv()


        interface = data['interface']

        if interface == 'IF.ID.onboard':
            response = IF_ID_onboard(data)

        elif interface == 'IF.ID.create':
            response = IF_ID_create(data)

        elif interface == 'IF.ID.retrieve':
            response = IF_ID_retrieve(data)

        elif interface == 'IF.TR.offer':
            response = IF_TR_offer(data)

        elif interface == 'IF.TR.order':
            response = IF_TR_order(data)

        elif interface == 'IF.TR.browse.offers':
            response = IF_TR_browse_offers(data)

        elif interface == 'IF.TR.browse.orders':
            response = IF_TR_browse_orders(data)

        elif interface == 'IF.TR.accept':
            response = IF_TR_accept(data)

        elif interface == 'IF.TR.check':
            response = IF_TR_check(data)

        elif interface == 'IF.TR.finish':
            response = IF_TR_finish(data)

        elif interface == 'IF.TR.list.ongoing':
            response = IF_TR_list_ongoing(data)

        elif interface == 'IF.TR.list.finished':
            response = IF_TR_list_finished(data)

        server.send(response)

    server.close()
