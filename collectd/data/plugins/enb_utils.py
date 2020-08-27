import collectd  
import json
from websocket import create_connection

def cpu_load(j_res, enb_id):
    try:
        vl = collectd.Values(type='vcpu')
        vl.host = enb_id
        vl.plugin = "resources"
        vl.plugin_instance = "enb"
        vl.type_instance = "single_core"
        vl.interval = 5
        if j_res['cpu']:
            val = j_res['cpu']['global']
            vl.dispatch(values=[val])
    except Exception as ex:
        print(ex)    


def get_ran_id(j_res):
    if j_res and j_res.get('global_enb_id'):
        return str(j_res['global_enb_id']['enb_id'])
    elif j_res and j_res.get('global_gnb_id'):
        return str(j_res['global_gnb_id']['gnb_id'])
    else:
        return '-1'

def get_lte_cells(j_res):
    cells = []
    if j_res and j_res.get('cells'):
        for key in j_res.get('cells'):
            cells.append(key)
    return cells

def get_nr_cells(j_res):
    cells = []
    if j_res and j_res.get('nr_cells'):
        for key in j_res.get('nr_cells'):
            cells.append(key)
    return cells                 


def cell_throughput(ws, j_res, enb_id, lte_cells, nr_cells):
    vl = collectd.Values(type='throughput')
    vl.plugin='cell'
    vl.plugin_instance='total'
    vl.host=enb_id
    vl.interval=5
    for cell in lte_cells:
        vl.plugin_instance=cell
        vl.type_instance='lte'
        vl.dispatch(values=[j_res["cells"][cell]["ul_bitrate"], j_res["cells"][cell]["dl_bitrate"]])
    for cell in nr_cells:
        vl.plugin_instance=cell
        vl.type_instance='nr'
        vl.dispatch(values=[j_res["cells"][cell]["ul_bitrate"], j_res["cells"][cell]["dl_bitrate"]])


def ue_count(j_res,ran_id):
    vl = collectd.Values(type='count')
    vl.plugin = 'ran_ue'
    vl.plugin_instance = 'total'
    vl.host = ran_id
    vl.type_instance = 'none'
    vl.interval = 5
    vl.dispatch(values=[len(j_res['ue_list'])])        

def imsi_id(enb_ip):
    try:
        ws = create_connection('ws://%s:9000' % enb_ip)
        ws.recv()
        ws.send('{"message":"ue_get"}')   
        result =  ws.recv()
        if ws:
            ws.shutdown
        else:
            return []
        imsi_list = []       
        j_res = json.loads(result)
        ue_list=j_res['ue_list']
        for ue in ue_list:
            if 'enb_id' in ue:
                imsi=str(ue['imsi'])
                if ue['registered']:
                    mme_ue_id = ue['mme_ue_id']
                    imsi_list.append({'imsi':imsi,'mme_ue_id':mme_ue_id})
            if 'ran_id' in ue:
                imsi=str(ue['imsi'])
                if ue['registered']:
                    mme_ue_id = ue['ran_ue_id']
                    imsi_list.append({'imsi':imsi,'ran_ue_id':mme_ue_id})
        return imsi_list
    except Exception as ex:
        print(ex)      


def ue_bitrate(j_res, imsi_list, ran_id):
    for i in range (0,len(j_res['ue_list'])):
        if(len(j_res['ue_list'][i]['cells'][0]) > 1):
            if 'mme_ue_id' in j_res['ue_list'][i]:
                mme_ue_id = j_res['ue_list'][i]['mme_ue_id']
                for imsi in imsi_list:
                    if 'mme_ue_id' in imsi:
                        if imsi['mme_ue_id'] == mme_ue_id:
                            vl = collectd.Values(type='throughput')
                            vl.plugin='ue'
                            vl.plugin_instance=imsi['imsi']
                            vl.host=ran_id
                            vl.type_instance='lte'
                            vl.interval=5
                            vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['ul_bitrate'],j_res['ue_list'][i]['cells'][0]['dl_bitrate']])
            if 'ran_ue_id' in j_res['ue_list'][i]:
                ran_ue_id = j_res['ue_list'][i]['ran_ue_id']
                for imsi in imsi_list:
                    if 'ran_ue_id' in imsi:
                        if imsi['ran_ue_id'] == ran_ue_id:
                            vl = collectd.Values(type='throughput')
                            vl.plugin='ue'
                            vl.plugin_instance=imsi['imsi']
                            vl.host=ran_id
                            vl.type_instance='nr'
                            vl.interval=5
                            vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['ul_bitrate'],j_res['ue_list'][i]['cells'][0]['dl_bitrate']])


def ue_stats(j_res, imsi_list, ran_id):
   for i in range (0,len(j_res['ue_list'])):
        if(len(j_res['ue_list'][i]['cells'][0]) > 1):
            if 'mme_ue_id' in j_res['ue_list'][i]:
                mme_ue_id = j_res['ue_list'][i]['mme_ue_id']
                for imsi in imsi_list:
                    if 'mme_ue_id' in imsi:
                        if imsi['mme_ue_id'] == mme_ue_id:
                            vl = collectd.Values(type='stats')
                            vl.plugin='ue'
                            vl.plugin_instance=imsi['imsi']
                            vl.host=ran_id
                            vl.type_instance='lte'
                            vl.interval=5
                            values = []
                            values.append(j_res['ue_list'][i]['cells'][0]['dl_mcs'])
                            if 'ul_mcs' in j_res['ue_list'][i]['cells'][0]:
                                values.append(j_res['ue_list'][i]['cells'][0]['ul_mcs'])
                            else:
                                values.append(0)
                            values.append(j_res['ue_list'][i]['cells'][0]['cqi'])
                            values.append(j_res['ue_list'][i]['cells'][0]['dl_tx'])
                            values.append(j_res['ue_list'][i]['cells'][0]['ul_tx'])
                            values.append(j_res['ue_list'][i]['cells'][0]['dl_retx'])
                            values.append(j_res['ue_list'][i]['cells'][0]['ul_retx'])
                            vl.dispatch(values=values)
            if 'ran_ue_id' in j_res['ue_list'][i]:
                ran_ue_id = j_res['ue_list'][i]['ran_ue_id']
                for imsi in imsi_list:
                    if 'ran_ue_id' in imsi:
                        if imsi['ran_ue_id'] == ran_ue_id:
                            vl = collectd.Values(type='stats')
                            vl.plugin='ue'
                            vl.plugin_instance=imsi['imsi']
                            vl.host=ran_id
                            vl.type_instance='nr'
                            vl.interval=5
                            values = []
                            values.append(j_res['ue_list'][i]['cells'][0]['dl_mcs'])
                            if 'ul_mcs' in j_res['ue_list'][i]['cells'][0]:
                                values.append(j_res['ue_list'][i]['cells'][0]['ul_mcs'])
                            else:
                                values.append(0)
                            values.append(j_res['ue_list'][i]['cells'][0]['cqi'])
                            values.append(j_res['ue_list'][i]['cells'][0]['dl_tx'])
                            values.append(j_res['ue_list'][i]['cells'][0]['ul_tx'])
                            values.append(j_res['ue_list'][i]['cells'][0]['dl_retx'])
                            values.append(j_res['ue_list'][i]['cells'][0]['ul_retx'])
                            vl.dispatch(values=values)

def ue_snr(j_res, imsi_list, ran_id):
    for i in range (0,len(j_res['ue_list'])):
        if(len(j_res['ue_list'][i]['cells'][0]) > 1):
            if 'mme_ue_id' in j_res['ue_list'][i]:
                mme_ue_id = j_res['ue_list'][i]['mme_ue_id']
                for imsi in imsi_list:
                    if 'mme_ue_id' in imsi:
                        if imsi['mme_ue_id'] == mme_ue_id:
                            if 'pusch_snr' in j_res['ue_list'][i]['cells'][0]:
                                vl = collectd.Values(type='snr')
                                vl.plugin='ue'
                                vl.plugin_instance=imsi['imsi']
                                vl.host=ran_id
                                vl.type_instance='pusch'
                                vl.interval=5
                                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['pusch_snr']])
                            if 'pucch1_snr' in j_res['ue_list'][i]['cells'][0]:
                                vl = collectd.Values(type='snr')
                                vl.plugin='ue'
                                vl.plugin_instance=imsi['imsi']
                                vl.host=ran_id
                                vl.type_instance='pusch'
                                vl.interval=5
                                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['pucch1_snr']])    
            if 'ran_ue_id' in j_res['ue_list'][i]:
                ran_ue_id = j_res['ue_list'][i]['ran_ue_id']
                for imsi in imsi_list:
                    if 'ran_ue_id' in imsi:
                        if imsi['ran_ue_id'] == ran_ue_id:
                            if 'pusch_snr' in j_res['ue_list'][i]['cells'][0]:
                                vl = collectd.Values(type='snr')
                                vl.plugin='ue'
                                vl.plugin_instance=imsi['imsi']
                                vl.host=ran_id
                                vl.type_instance='pusch'
                                vl.interval=5
                                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['pusch_snr']])
                            if 'pucch1_snr' in j_res['ue_list'][i]['cells'][0]:
                                vl = collectd.Values(type='snr')
                                vl.plugin='ue'
                                vl.plugin_instance=imsi['imsi']
                                vl.host=ran_id
                                vl.type_instance='pusch'
                                vl.interval=5
                                vl.dispatch(values=[j_res['ue_list'][i]['cells'][0]['pucch1_snr']])    
