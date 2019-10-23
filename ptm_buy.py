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

class tradeAssitant(object) :

    def dicTrasfer(self, data) :
        data1 = data
        return data1

    def browseData(self, data1, data2) :
        lowPrice = 0
        target = {}
        if data1['price'] < data2['price'] :
            lowPrice = data1['price']
            target = data1
        elif data1['price'] > data2['price'] :
            lowPrice = data2['price']
            target = data2

        return target

# PTM, acting as a client, makes requests to Blockchain Interface (BI)
if __name__ == "__main__":
    port_BI = 9000
    port_EMS = 9001
    host = 'localhost'
    client = Client()
    trade = tradeAssitant()
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

    }
    IF_TR_check = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.check",
        "parameter" : ""
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
        "parameter" : "id:order:0x123456"
        }
    IF_TR_contractMsg = {
        "target" : "EMS",
        "type" : "REQ",
        "interface" : "IF.TR.contractMsg",
        "parameter" : ""
        }


# 판매정보 브라우징
    print('현재 마켓에 있는 판매정보를 요청합니다.')
    print(IF_TR_browse)
    print('\n')
    client.dataReq(IF_TR_browse)
    client.send(IF_TR_browse)
    time.sleep(1)

    IF_TR_browse.update(client.recv())  #IF_ID_onboard["parameter"] = 'true' 응답

    if IF_TR_browse['type'] == 'RES':
        print('성공적으로 마켓정보를 수신하였습니다.')
        print('\n')
        print(IF_TR_browse['parameter'])
        print('\n')
        time.sleep(1)
    # print(IF_TR_browse)
    # print('\n')
    # print(IF_TR_order)
    # print('\n')
    #print(trade.dicTrasfer(IF_TR_browse['parameter']['order1']))

# 판매정보 기반 가격 책정
        tmpOrder1 = trade.dicTrasfer(IF_TR_browse['parameter']['order1'])
        tmpOrder2 = trade.dicTrasfer(IF_TR_browse['parameter']['order2'])
        tmpTarget = trade.browseData(tmpOrder1, tmpOrder2)
        print('판매분석결과 orderId : ' + tmpTarget['offerId'] + '가 가장 저렴합니다.')
        print('\n')
        time.sleep(1)
        IF_TR_order['parameter'] = 'offerId : ' + tmpTarget['offerId']

# BI에 주문 요청
        print('주문을 요청합니다.')
        print(IF_TR_order)
        print('\n')
        client.dataReq(IF_TR_order)
        client.send(IF_TR_order)
        time.sleep(1)

        IF_TR_order.update(client.recv())

        if IF_TR_order['type'] == 'RES':
            print('주문이 성공적으로 요청되었습니다.')
            print(IF_TR_order)
            print('\n')
            time.sleep(1)

# BI에 주문 결과 확인요청
            tmpCheck = IF_TR_order['parameter']
            print(tmpCheck)
            IF_TR_check['parameter'] = tmpCheck #orderId 맵핑
            print('주문을 확인합니다')
            print(IF_TR_check)
            print('\n')
            client.dataReq(IF_TR_check)
            client.send(IF_TR_check)
            time.sleep(1)

            tmpCheck1 = client.recv()
            IF_TR_check['parameter']['tradeId'] = tmpCheck1['parameter']['tradeId']
            IF_TR_check['state'] = tmpCheck1['state']
            if tmpCheck1['type'] == 'RES':
                print('주문이 성공적으로 체결되었습니다.')
                print('tradeID는 '+IF_TR_check['parameter']['tradeId']+' 입니다')
                print('\n')
                print(IF_TR_check)
                print('\n')

# EMS에 거래결과 알림

                print('EMS에 체결된 주문정보를 전송합니다.')
                print(IF_TR_contractMsg)
                print('\n')
                IF_TR_contractMsg['parameter'] = IF_TR_check['parameter']
                print(IF_TR_contractMsg)
                print('\n')
                client.dataReq(IF_TR_contractMsg)
                client.send(IF_TR_contractMsg)
                time.sleep(1)

                tmpContract = client.recv()
                if tmpContract['type'] == 'RES':
                    print('EMS에 주문정보를 성공적으로 전송하였습니다.')
                    print('\n')
                    print(tmpContract)
                    print('\n')
    #print(trade.browseData(trade.dicTrasfer(IF_TR_browse['parameter']['order1']),trade.dicTrasfer(IF_TR_browse['parameter']['order2']) ))
    #trade.dicTrasfer(IF_TR_browse['parameter']['order1'])
    #trade.dicTrasfer(IF_TR_browse['parameter']['order2'])
               #서버응답 실패


    # IF_TR_browse.update(client.recv())  #정상적으로 받아서 update했다고 가정 스도코드
    # orderlist = IF_TR_browse.parameter  #리스트업
    # for i in orderlist                  #price 최소값 도출 /  index 찾아야함
    #     i = 1
    #     min = orderlist.pirce[1]
    #     if orderlist.pirce[i+1] < orderlist.pirce[1] :
    #         min = orderlist.pirce[i+1]
    #         i = i+1
    #
    # IF_TR_order['parameter'] = {"id":"0x876543"}   #최솟값 오더
    # client.dataReq(IF_TR_order)
    # client.send(IF_TR_order)
    # time.sleep(1)
    # if IF_TR_order['type'] == 'RES':                # 정상 응답
    #     print('success to order')
    #     client.dataReq(IF_TR_check)                 # 거래 체결 확인 (체크)
    #     client.send(IF_TR_check)
    #     #print(IF_ID_create)
    #     time.sleep(1)
    #     if IF_TR_check['type'] == 'RES':             # 거래 체결 체크 응답
    #         print('success to contract')
    #         client.dataReq(IF_TR_contractMsg)       # EMS 거래 정보 전달
    #         client.send(IF_TR_contractMsg)
    #         #print(IF_ID_create)
    #         time.sleep(1)
    #         if IF_TR_check['type'] == 'RES':          # 정상 응답
    #             print('success to sending contractMsg ')


    client.close()

    #
    # client.connect(host, port_EMS)
    # request = IF_TR_contractMsg
    # print(request)
    # client.send(request)
    # time.sleep(1)
    # print(client.recv())
    # client.close()
