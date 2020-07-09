from websocket import create_connection
import json
import threading



epc_list = []

def read_thread(epc_ip):
    try:
        ws = create_connection('ws://%s:9000' % epc_ip)
        ws.send('{"message":"stats"}')
        result =  ws.recv()
        j_res = json.loads(result)
        print(j_res)
        print("cpu_usage: ")
        print(j_res['cpu'])
        ws.send('{"message":"enb"}')
        result =  ws.recv()
        j_res = json.loads(result)
        #print(j_res)
        print(j_res)

        for i in range (0,len(j_res['enb_list'])):
            plmn = j_res['enb_list'][i]['plmn']
            eNB_ID = j_res['enb_list'][i]['eNB_ID']
            address = j_res['enb_list'][i]['address']
            ue_ctx = j_res['enb_list'][i]['ue_ctx']
            address=address[0:address.index(":")]
            print(address)
            print("ip_"+str(address)+"_ID_"+str(eNB_ID)+"_ID")

        ws.send('{"message":"ue_get"}')
        result =  ws.recv()
        j_res = json.loads(result)
        print(j_res['ue_list'])
        for i in range (0,len(j_res['ue_list'])):
            imsi = j_res['ue_list'][i]['imsi']

            registered = j_res['ue_list'][i]['registered']
            if(registered):
                bearers = j_res['ue_list'][i]['bearers']
                print(bearers)
            print(imsi)
            try:
                enb_ue_id = j_res['ue_list'][i]['enb_ue_id']
                mme_ue_id = j_res['ue_list'][i]['mme_ue_id']
                print(enb_ue_id)
                print(mme_ue_id)
                print(imsi+" CONNECTED")
            except Exception as ex:
                print(imsi+" DISCONNECTED")
            print(registered)



    except Exception as e:
        print('epc @ %s is not connected !' % epc_ip)
        print(e)


def read(data=None):
    global epc_list
    for ip_i in epc_list:
        threading.Thread(target=read_thread,kwargs=dict(epc_ip=ip_i)).start()

if __name__ == "__main__":
    print("loading EPC list")
    f = open('epc_list.cfg', 'r')
    epc_list = f.read().splitlines()
    read()                