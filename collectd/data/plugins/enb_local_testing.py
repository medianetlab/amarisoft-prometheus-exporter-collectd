from websocket import create_connection
import json
import threading


ws = create_connection("ws://10.2.1.10:9001", timeout=4)
enb_list = []

def read_thread(enb_ip):
    try:
        ws = create_connection('ws://%s:9001' % enb_ip)
        ws.send('{"message":"stats"}')
        result =  ws.recv()
        j_res = json.loads(result)
        #print(j_res)
        print(j_res["cells"]["10"]["dl_bitrate"])

        # get enb - ue info
        ws.send('{"message":"ue_get","stats"=true}')
        result =  ws.recv()
        j_res = json.loads(result)
        print(j_res)
        print(len(j_res['ue_list']))

        # get ue info


        print("ue_specific_info")
        for i in range (0,len(j_res['ue_list'])):
            if(len(j_res['ue_list'][i]['cells'][0]) > 1) :
                print("dl_bitrate: " + str(j_res['ue_list'][i]['cells'][0]['dl_bitrate']))
                print("ul_bitrate: " + str(j_res['ue_list'][i]['cells'][0]['ul_bitrate']))
            else:
                print("Iddle UE")

    except Exception as e:
        print('enb @ %s is not connected !' % enb_ip)
        print(e)


def read(data=None):
    global enb_list
    for ip_i in enb_list:
        threading.Thread(target=read_thread,kwargs=dict(enb_ip=ip_i)).start()

if __name__ == "__main__":
    print("loading ENB list")
    f = open('enb_list.cfg', 'r')
    enb_list = f.read().splitlines()
    read()
