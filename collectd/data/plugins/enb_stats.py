import collectd
from websocket import create_connection
import json
import threading
import enb_utils as utils


enb_list = []

def read_thread(enb_ip):
    try:
        ws = create_connection('ws://%s:9001' % enb_ip)
        ws.recv()
        ws.send('{"message":"stats"}')
        result =  ws.recv()
        utils.cpu_load(ws, result, epc_ip)


        # enb throughput
        vl = collectd.Values(type='bitrate')
        vl.plugin='enb_stats'
        vl.plugin_instance='total'
        vl.host=enb_ip
        vl.type_instance='dl'
        vl.interval=5
        #print(j_res)
        vl.dispatch(values=[j_res["cells"]["10"]["dl_bitrate"]])
        vl.type_instance='ul'
        vl.dispatch(values=[j_res["cells"]["10"]["ul_bitrate"]])

        # enb ue_count
        ws.send('{"message":"ue_get" ,"stats"=true}')
        result =  ws.recv()
        j_res = json.loads(result)
        #print(j_res)
        vl = collectd.Values(type='count')
        vl.plugin='enb_ue'
        vl.plugin_instance='total'
        vl.host=enb_ip
        vl.type_instance='none'
        vl.interval=5
        vl.dispatch(values=[len(j_res['ue_list'])])

        # ue bitrate
        for i in range (0,len(j_res['ue_list'])):
            if(len(j_res['ue_list'][i]['cells'][0]) > 1):
                mme_ue_id = j_res['ue_list'][i]['mme_ue_id']
                enb_ue_id = j_res['ue_list'][i]['enb_ue_id']
                vl = collectd.Values(type='bitrate')
                vl.plugin='ue_stats'
                vl.plugin_instance=str(mme_ue_id)
                vl.host=enb_ip
                vl.type_instance='dl'
                vl.interval=5
                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['dl_bitrate']])
                vl.type_instance='ul'
                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['ul_bitrate']])
     

        # ue cqi
        for i in range (0,len(j_res['ue_list'])):
            if(len(j_res['ue_list'][i]['cells'][0]) > 1):
                mme_ue_id = j_res['ue_list'][i]['mme_ue_id']
                enb_ue_id = j_res['ue_list'][i]['enb_ue_id']
                vl = collectd.Values(type='cqi')
                vl.plugin='ue_stats'
                vl.plugin_instance=str(mme_ue_id)
                vl.host=enb_ip
                vl.type_instance='cqi'
                vl.interval=5
                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['cqi']])

        # ue mcs
        for i in range (0,len(j_res['ue_list'])):
            if(len(j_res['ue_list'][i]['cells'][0]) > 1):
                mme_ue_id = j_res['ue_list'][i]['mme_ue_id']
                enb_ue_id = j_res['ue_list'][i]['enb_ue_id']
                vl = collectd.Values(type='mcs')
                vl.plugin='ue_stats'
                vl.plugin_instance=str(mme_ue_id)
                vl.host=enb_ip
                vl.type_instance='dl'
                vl.interval=5
                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['dl_mcs']])
                vl.type_instance='ul'
                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['ul_mcs']])

        # ue pucch_snr
        for i in range (0,len(j_res['ue_list'])):
            if(len(j_res['ue_list'][i]['cells'][0]) > 1):
                mme_ue_id = j_res['ue_list'][i]['mme_ue_id']
                enb_ue_id = j_res['ue_list'][i]['enb_ue_id']
                vl = collectd.Values(type='pucch_snr')
                vl.plugin='ue_stats'
                vl.plugin_instance=str(mme_ue_id)
                vl.host=enb_ip
                vl.type_instance='snr'
                vl.interval=5
                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['pucch1_snr']])


        # ue pusch_snr
        for i in range (0,len(j_res['ue_list'])):
            if(len(j_res['ue_list'][i]['cells'][0]) > 1):
                mme_ue_id = j_res['ue_list'][i]['mme_ue_id']
                enb_ue_id = j_res['ue_list'][i]['enb_ue_id']
                vl = collectd.Values(type='pusch_snr')
                vl.plugin='ue_stats'
                vl.plugin_instance=str(mme_ue_id)
                vl.host=enb_ip
                vl.type_instance='snr'
                vl.interval=5
                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['pusch_snr']])
        ws.shutdown

    except Exception as e:
        print(e)
        print('enb @ %s is not connected !' % enb_ip)
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
