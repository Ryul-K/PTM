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

        "parameter" : "id:order:0x123456"
,
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
        "interface" : "IF.STATE.stateOfcharge",
        "parameter" : "",
        "time" : ""
    }
    IF_STATE_lossRatio = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.STATE.stateOfcharge",
        "parameter" : "",
        "time" : ""
    }
    IF_ID_regist = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.ID.regist",
        "parameter" : ""
        }
    IF_TR_contractMsg = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.TR.contractMsg",
        "parameter" : "id:order:0x135790"
        }




    print('#################################################')
    print('PTM 인증을 시작합니다')
    print('#################################################')
    print('\n')

    print('Blockchain Interface에 연결을 요청합니다\n')
    #print('\n\)
    client.dataReq(IF_ID_onboard)
    client.send(IF_ID_onboard)

# BI에 연결 요청
    print('연결 요청 JSON')
    print(IF_ID_onboard)
    print('\n')

    time.sleep(1)
    IF_ID_onboard.update(client.recv())  #IF_ID_onboard["parameter"] = 'true' 응답

# BI 응답 출력
    print('Blockchain Interface에서 응답 요청이 왔습니다')
    print('\n')

    print('연결 응답 JSON')
    print(IF_ID_onboard)

    if IF_ID_onboard['type'] == 'RES':
        print('성공적으로 연결이 되었습니다.')
        print('\n')

# BI에 B-EMS ID 생성 요청
        print('B-EMS ID 생성을 요청합니다')
        print('\n')

        client.dataReq(IF_ID_create)
        client.send(IF_ID_create)
        print('ID 생성 요청 JSON')
        print(IF_ID_create)
        print('\n')

        time.sleep(1)

# B-EMS ID 응답
        IF_ID_create.update(client.recv())  #IF_ID_onboard["parameter"] = 'true' 응답
        print('Blockchain Interface에서 ID 등록 응답이 왔습니다')
        print('\n')

        print('B-EMS ID 응답 JSON')
        print(IF_ID_create)
        print('\n')

        if IF_ID_create['type'] == 'RES':
            print('성공적으로 ID가 생성되었습니다')
            print('\n')

            print('등록된 ID JSON')
            print(IF_ID_create['parameter'])

            #IF_ID_regist.update(IF_ID_create['parameter'])
            #IF_ID_regist.update(IF_ID_create['parameter'])
            IF_ID_regist['parameter']=IF_ID_create['parameter']

# EMS에 생성된 B-EMS ID 등록 요청
            print('EMS에 B-EMS ID 등록을 요청합니다')
            print('\n')

            print('등록 요청 JSON')
            print(IF_ID_regist)
            print('\n')

            client.dataReq(IF_ID_regist)
            client.send(IF_ID_regist)

            time.sleep(1)

            IF_ID_regist.update(client.recv())

# B-EMS ID 등록 응답

            if IF_ID_regist['type'] == 'RES':
                print('ID가 성공적으로 등록되었습니다.')
                print('\n')

                print('등록 응답 JSON')
                print(IF_ID_regist)
                print('\n')

                print('#################################################')
                print('성공적으로 PTM 인증을 완료합니다')
                print('#################################################')

    client.close()

    #
    # client.connect(host, port_EMS)
    # request = IF_TR_contractMsg
    # print(request)
    # client.send(request)
    # time.sleep(1)
    # print(client.recv())
    # client.close()
