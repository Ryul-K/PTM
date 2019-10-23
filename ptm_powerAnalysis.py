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
    CONST_RECV_MAX_SIZE = 1024
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

    def dataReq(self, data):
        target = data['target']
        if target == 'BI' :
            self.connect(host, 9000)
        elif target == 'EMS' :
            self.connect(host, 9001)


class stateAnalysis(object) :
    def stateValue(self, soc, gen, loss):
        tradeState = ""
        if soc > 70 :
            if gen > loss :
                tradeState = "sell"
            tradeState = "none"
        elif soc < 30 :
            if gen < loss :
                tradeState = "buy"
            tradeState = "none"
        elif 30 <= soc <= 70 :
            tradeState = "none"

        return tradeState




#
# def dataReq(data, port_BI, port_EMS):
#     target = data['target']
#     print(target)
#     if target = BI
#         client.connect(host, port_BI)
#     elif target = EMS
#         client.connect(host, port_EMS)
#     request = data
#     print(request)
#     client.send(request)
#     time.sleep(1)
#
#     print(client.recv())
#     client.close()




# PTM, acting as a client, makes requests to Blockchain Interface (BI)
if __name__ == "__main__":
    port_BI = 9000
    port_EMS = 9001
    host = 'localhost'
    client = Client()
    state = stateAnalysis()
    #BI request
    IF_ID_onboard = {
        "target" : "BI",
	    "type" : "REQ",
	    "interface" : "IF.ID.onboard",
	    "parameter" : "password"
    }
    IF_ID_create = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.ID.create",
        "parameter" : ""
    }
    IF_TR_offer = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.offer",
        "parameter" : '{"price":"1000", "quantity":"500", "hour":"4", "tolerance":"5"}'
    }
    IF_TR_order = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.order",
        "parameter" : "id:offer:0x345678"
    }
    IF_TR_browse = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.browse",
        "parameter" : ""
    }
    IF_TR_accept = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.accept",
        "parameter" : "id:order:0x123456",
        "qwe" : "qqqq",
        "qqqq" : "wwww"
    }

    #EMS request
    IF_STATE_stateOfcharge = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.STATE.stateOfcharge",
        "parameter" : "",
        "time" : ""
    }
    IF_STATE_genRatio = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.STATE.genRatio",
        "parameter" : "",
        "time" : ""
    }
    IF_STATE_lossRatio = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.STATE.lossRatio",
        "parameter" : "",
        "time" : ""
    }
    IF_STATE_stateParams = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.STATE.stateParams",
        "parameter" : "",
        "time" : ""
    }
    IF_ID_regist = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.ID.regist",
        "parameter" : "id:order:0x123456"
        }
    IF_TR_contractMsg = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.TR.contractMsg",
        "parameter" : "id:order:0x135790"
        }

    print('EMS에 상태 정보를 요청합니다.')
    print(IF_STATE_stateParams)
    print('\n')
    client.dataReq(IF_STATE_stateParams)
    client.send(IF_STATE_stateParams)
    time.sleep(1)

    IF_STATE_stateParams.update(client.recv())
    if IF_STATE_stateParams['type'] == 'RES' :
        print('성공적으로 상태 정보를 수신하였습니다.')
        print(IF_STATE_stateParams)
        print('\n')
        a = IF_STATE_stateParams['parameter']['stateOfcharge']
        b = IF_STATE_stateParams['parameter']['genRatio']
        c = IF_STATE_stateParams['parameter']['lossRatio']

        print(state.stateValue(a,b,c))


    client.close()

    #
    # client.connect(host, port_EMS)
    # request = IF_TR_contractMsg
    # print(request)
    # client.send(request)
    # time.sleep(1)
    # print(client.recv())
    # client.close()
