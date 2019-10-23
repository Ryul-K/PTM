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

def IF_ID_create(request):
    return {
        "type" : "RES",
        "interface" : "IF.ID.create",
        "parameter" : {"id" : "bems:0x123456", "password" : "1234"}
    }

def IF_TR_offer(request):
    return {
        "type" : "RES",
        "interface" : "IF.TR.offer",
        "parameter" : {"offerId" : "id:offer:0x345678"},
        "state" : "success"
    }

def IF_TR_order(request):
    return {
        "type" : "RES",
        "interface" : "IF.TR.order",
        "parameter" : {"orderId" : " orderId: (offerId:0x876543)"},
        "state" : "success"
    }

def IF_TR_browse(request):
    order1 = {"offerId":"0x876543", "price":500, "quantity":200, "hour":2, "tolerance":5}
    order2 = {"offerId":"0x345678", "price":800, "quantity":400, "hour":4, "tolerance":5}
    return {
        "type" : "RES",
        "interface" : "IF.TR.browse",
        "parameter" : {"order1" : order1, "order2" : order2}

    }

def IF_TR_accept(request):
    return {
        "type" : "RES",
        "interface" : "IF.TR.accept",
        "parameter" : {"tradeId" : "trade:0xce3f42"}
        }

def IF_TR_check(request):
    return {
        "type" : "RES",
        "interface" : "IF.TR.check",
        "parameter" : {"tradeId" : "trade:0xce3f42"},
        "state" : "success"
        }



'''
-------------------- API ends ---------------------
'''

# Blockchain Interface (BI), acting as a server, receives request from PTM
if __name__ == "__main__":
    port = 9000
    server = Server(port)

    while True:
        server.accept()
        data = server.recv()


        interface = data['interface']

        if interface == 'IF.ID.onboard':
            response = IF_ID_onboard(data)
        elif interface == 'IF.ID.create':
            response = IF_ID_create(data)
        elif interface == 'IF.TR.offer':
            response = IF_TR_offer(data)
        elif interface == 'IF.TR.order':
            response = IF_TR_order(data)
        elif interface == 'IF.TR.browse':
            response = IF_TR_browse(data)
        elif interface == 'IF.TR.accept':
            response = IF_TR_accept(data)
        elif interface == 'IF.TR.check':
            response = IF_TR_check(data)



        server.send(response)

    server.close()
