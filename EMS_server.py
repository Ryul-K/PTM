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
def IF_STATE_stateParams(request):

        return {
            "type" : "RES",
            "interface" : "IF.TR.stateParams",
            "parameter" : { "stateOfcharge" : 30,
                            "genRatio" : 10,
                            "lossRatio" : 15
                        },
            "state" : "success"
            }

def IF_STATE_stateOfcharge(request):
        return {
            "type" : "RES",
            "interface" : "IF.STATE.stateOfcharge",
            "parameter" : "",
            "time" : ""
        }

def IF_STATE_genRatio(request):
        return {
            "type" : "RES",
            "interface" : "IF_STATE_genRatio",
            "parameter" : "",
            "time" : ""
        }

def IF_STATE_lossRatio(request):
        return {
            "type" : "RES",
            "interface" : "IF_STATE_lossRatio",
            "parameter" : "",
            "time" : ""
        }
def IF_ID_regist(request):
        return {
            "type" : "RES",
            "interface" : "IF.ID.regist",
            "parameter" : "",
            "status" : "success"
            }
def IF_TR_contractMsg(request):
        return {
            "type" : "RES",
            "interface" : "IF.TR.contractMsg",
            "parameter" : "",
            "state" : "success"
            }


'''
-------------------- API ends ---------------------
'''

# Blockchain Interface (BI), acting as a server, receives request from PTM
if __name__ == "__main__":
    port = 9001
    server = Server(port)

    while True:
        server.accept()
        data = server.recv()


        interface = data['interface']

        if interface == 'IF.STATE.stateOfcharge':
            response = IF_STATE_stateOfcharge(data)
        elif interface == 'IF.STATE.genRatio':
            response = IF_STATE_genRatio(data)
        elif interface == 'IF.STATE.lossRatio':
            response = IF_STATE_lossRatio(data)
        elif interface == 'IF.ID.regist':
            response = IF_ID_regist(data)
        elif interface == 'IF.TR.contractMsg':
            response = IF_TR_contractMsg(data)
        elif interface == 'IF.STATE.stateParams':
            response = IF_STATE_stateParams(data)


        server.send(response)

    server.close()
