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

    def dataReq(self, data):
        target = data['target']
        if target == 'BI' :
            self.connect(host, 8888)
        elif target == 'EMS' :
            self.connect(host, 9999)


class stateAnalysis(object) :
    def stateValue(self, soc, gen, loss):
        tradeState = ""
        if soc > 70 :
            tradeState = "none"
            if gen > loss :
                tradeState = "sell"

        elif soc < 30 :
            tradeState = "none"
            if gen < loss :
                tradeState = "buy"

        elif 30 <= soc <= 70 :
            tradeState = "none"

        return tradeState

class tradeAssitant(object) :

    def dicTrasfer(self, data) :
        data1 = data
        return data1

    def browseData(self, data1, data2) :
        target = {}
        if data1['price'] < data2['price'] :
            target = data1
        elif data1['price'] > data2['price'] :
            target = data2

        return target

# PTM, acting as a client, makes requests to Blockchain Interface (BI)
if __name__ == "__main__":
    state = stateAnalysis()
    trade = tradeAssitant()
    host = 'localhost' # localhost for test
    i = 0

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
    IF_ID_retrieve = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.ID.retrieve",
        "parameter" : ""
    }
    IF_TR_offer = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.offer",
        "parameter" : '{"price":"1000", "quantity":"500", "hour":"4"}'
    }
    IF_TR_order = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.order",
        "parameter" : {"deal": "0xa8b05f0bc681a1c95430a2d3e195a0c1646d0e236e3c4b8ab8538b50052dedf9", "quantity": 100}
    }
    IF_TR_browse_offers = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.browse.offers",
        "parameter" : ""
    }
    IF_TR_browse_orders = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.browse.orders",
        "parameter" : '{"deal": "0xe03070397c6d216f48e50bf393d8d90fe150430xe03070397c6d216f48e50bf393d8d90fe15043"}'
    }
    IF_TR_accept = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.accept",
        "parameter" : '{"deal": "0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6", "order": "id:bems:4ebd680f2cc1f76bdf65b5b2c2afc0d64c553279"}'
    }
    IF_TR_check = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.check",
        "parameter" : '{"deal": "0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6"}'
    }
    IF_TR_finish = {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.finish",
        "parameter" : '{"deal": "0xe03070397c6d216f48e50bf393d8d90fe150430d6efd7252af8541dc9b3128b6"}'
    }
    IF_TR_list_ongoing= {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.list.ongoing",
        "parameter" : ""
    }
    IF_TR_list_finished= {
        "target" : "BI",
        "type" : "REQ",
        "interface" : "IF.TR.list.finished",
        "parameter" : ""
    }

    #EMS request

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
        "parameter" : {}
        }

    # connect to BI server
    client = Client()

    print('client connected...')
    while True:
        i += 1
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

            #구매
            if state.stateValue(a,b,c) == 'buy' :
                print("### 전력이 부족합니다. ###\n")
                print("전력 구매를 수행합니다.\n")
                print("거래 리스트를 불러옵니다.\n")
                client.dataReq(IF_TR_browse_offers)
                client.send(IF_TR_browse_offers)
                time.sleep(1)
                tmpofferlist = client.recv()
                #print(tmpofferlist)

                tmpofferlist1 = trade.dicTrasfer(tmpofferlist['parameter'][0])
                tmpofferlist2 = trade.dicTrasfer(tmpofferlist['parameter'][1])
                tmpTarget = trade.browseData(tmpofferlist1, tmpofferlist2)
                print('판매분석결과 거래 Id : ' + tmpTarget['id'] + '가 가장 저렴합니다.\n')
                # print(tmpofferlist2)
                IF_TR_order['parameter']['deal'] = tmpTarget['id']
                #print(IF_TR_order['parameter']['deal'])
                print(IF_TR_order['parameter']['deal'] + '로 주문을 진행합니다.\n')
                client.dataReq(IF_TR_order)
                client.send(IF_TR_order)
                time.sleep(1)
                tmpOrder = client.recv()
                #print(f'BI ==> PTM: {tmpOrder}')
                if tmpOrder['parameter'] == 'True' :
                    print('정상적으로 주문이 완료되었습니다.\n')
                    time.sleep(3)

                    client.dataReq(IF_TR_check)
                    client.send(IF_TR_check)
                    time.sleep(1)
                    tmpCheck = client.recv()
                    #print(f'BI ==> PTM: {tmpCheck}')

                    if tmpCheck['parameter'] == 'established' :
                        print('주문이 성공적으로 체결되었습니다.\n')
                        print('deal id : ' + tmpTarget['id'])
                        print('seller id : ' + tmpTarget['seller'])
                        print('price : ' + str(tmpTarget['price']))
                        print('quantity : ' + tmpTarget['quantity'] + '\n')

                        print('EMS에 거래정보를 전달합니다.')
                        IF_TR_contractMsg['parameter'] = tmpTarget
                        #print(IF_TR_contractMsg)
                        client.dataReq(IF_TR_contractMsg)
                        client.send(IF_TR_contractMsg)
                        time.sleep(1)
                        tmpContractmsg = client.recv()
                        #print(f'BI ==> PTM: {tmpContractmsg}')
                        if tmpContractmsg['state'] == 'success' :
                            print('거래 정보가 EMS에 성공적으로 전달되었습니다.')
                            print('전력 상태를 모니터링 합니다.')
                            time.sleep(30)


            #판매

            #판매
            elif state.stateValue(a,b,c) == 'sell' :
                print('### 전력량이 많습니다. ###\n')
                print('전력 판매를 수행합니다.\n')
                print('전력 거래를 제안합니다.\n')
                client.dataReq(IF_TR_offer)
                client.send(IF_TR_offer)
                time.sleep(1)
                tmpOffer = client.recv()  #tmpOffer['parameter'] 에 deal id 발급
                #print(f'BI ==> PTM: {tmpOffer}')

                time.sleep(1) #주문이 들어올때까지 대기

                print('주문을 조회합니다.\n')
                client.dataReq(IF_TR_browse_orders)
                client.send(IF_TR_browse_orders)
                time.sleep(1)
                tmpOrderlist = client.recv()
                #print(f'BI ==> PTM: {tmpOrderlist}')

                print('주문이 들어왔습니다.')
                print('deal id : ' + tmpOrderlist['parameter'][0]['id'])
                print('orderer : ' + tmpOrderlist['parameter'][0]['orderer'])
                print('quantity : ' + tmpOrderlist['parameter'][0]['quantity'] + '\n')

                print('거래를 확정합니다.')
                client.dataReq(IF_TR_accept)
                client.send(IF_TR_accept)
                time.sleep(1)
                tmpAccept = client.recv()
                #print(f'BI ==> PTM: {tmpAccept}')
                if tmpAccept['parameter'] == 'True' :
                    print('EMS에 거래정보를 전달합니다.\n')
                    IF_TR_contractMsg['parameter'] = tmpOrderlist
                    #print(IF_TR_contractMsg)
                    client.dataReq(IF_TR_contractMsg)
                    client.send(IF_TR_contractMsg)
                    time.sleep(1)
                    tmpContractmsg = client.recv()
                    #print(f'BI ==> PTM: {tmpContractmsg}')
                    if tmpContractmsg['state'] == 'success' :
                        print('거래 정보가 EMS에 성공적으로 전달되었습니다.\n')
                        print('전력 상태를 모니터링 합니다.')
                        time.sleep(30)

            #정상상태
            elif state.stateValue(a,b,c) == 'none' :
                print("전력 상태 이상없습니다. 주기적으로 모니터링을 수행합니다.\n")
                time.sleep(30)
                continue


# client.dataReq(IF_TR_accept)
# client.send(IF_TR_accept)
# time.sleep(1)
# tmpaccept = client.recv()
# print(f'BI ==> PTM: {tmpaccept}')

    # create ID
    # request = IF_ID_create
    # print(f'PTM ==> BI: {request}')
    # client.send(request)
    # print(f'BI ==> PTM: {client.recv()}')
    # time.sleep(5)
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
