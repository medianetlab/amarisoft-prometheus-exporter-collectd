import collectd
from websocket import create_connection
import json
import threading
import enb_utils as utils


enb_list = []

def read_thread(enb_ip):
    ws = None
    try:
        ws = create_connection('ws://%s:9001' % enb_ip)
        ws.recv()

        ws.send('{"message":"config_get"}')
        result =  ws.recv()
        j_res = json.loads(result)
        ran_id = utils.get_ran_id(j_res)
        lte_cells = utils.get_lte_cells(j_res)
        nr_cells = utils.get_nr_cells(j_res)
        ws.send('{"message":"stats"}')
        result =  ws.recv()
        j_res = json.loads(result)
        utils.cpu_load(j_res, ran_id)
        utils.cell_throughput(ws, j_res, ran_id, lte_cells, nr_cells)

        ws.send('{"message":"ue_get" ,"stats"=true}')
        result =  ws.recv()
        j_res = json.loads(result)
        utils.ue_count(j_res,ran_id)
        imsi_list = utils.imsi_id(enb_ip)
        utils.ue_bitrate(j_res, imsi_list, ran_id)
        utils.ue_stats(j_res, imsi_list, ran_id)
        utils.ue_snr(j_res, imsi_list, ran_id)


    except Exception as e:
        print(e)
        print('enb @ %s is not connected !' % enb_ip)
        if ws:
            ws.shutdown


def read(data=None):
    global enb_list
    for ip_i in enb_list:
        threading.Thread(target=read_thread,kwargs=dict(enb_ip=ip_i)).start()





def write(vl, data=None):
    print "(plugin: %s host: %s type: %s pl.i: %s ty.i: %s): %s\n" % (vl.plugin, vl.host, vl.type,vl.plugin_instance,vl.type_instance, vl.values)





def init():
    global enb_list
    print("loading ENB list")
    f = open('/etc/collectd/plugins/enb_list.cfg', 'r')
    enb_list = f.read().splitlines()
    print(enb_list)

collectd.register_read(read)
collectd.register_write(write)
collectd.register_init(init)
