import collectd
from websocket import create_connection
import json
import threading
import epc_utils as utils



epc_list = []

def read_thread(epc_ip):
    try:
        
        ws = create_connection('ws://%s:9000' % epc_ip)
        ws.recv()

        ws.send('{"message":"stats"}')      
        result =  ws.recv()
        j_res = json.loads(result)
        utils.cpu_load(ws, j_res, epc_ip)
        utils.s1_connections(ws, j_res, epc_ip)
        utils.ng_connections(ws, j_res, epc_ip)

        ws.send('{"message":"ue_get"}')   
        result =  ws.recv()
        j_res = json.loads(result)
        utils.ue_info(ws, j_res, epc_ip)

    except Exception as e:
        print(e)
        print('epc @ %s is not connected !' % epc_ip)
        ws.shutdown


def read(data=None):
    global epc_list
    for ip_i in epc_list:
        threading.Thread(target=read_thread,kwargs=dict(epc_ip=ip_i)).start()





def write(vl, data=None):
    print ("(plugin: %s host: %s type: %s pl.i: %s ty.i: %s): %s\n" \
         % (vl.plugin, vl.host, vl.type,vl.plugin_instance,vl.type_instance, vl.values))





def init():
    global epc_list
    print("loading EPC list")
    f = open('/etc/collectd/plugins/epc_list.cfg', 'r')
    epc_list = f.read().splitlines()
    print(epc_list)

collectd.register_read(read)
collectd.register_write(write)
collectd.register_init(init)
