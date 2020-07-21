import collectd  
import json

def cpu_load(ws, j_res, enb_id):
    try:
        vl = collectd.Values(type='vcpu')
        vl.host = enb_id
        vl.plugin = "resources"
        vl.plugin_instance = "enb"
        vl.type_instance = "single_core"
        vl.interval = 5
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

def get_cells_info(j_res):


def cell_throughput(ws, j_res, enb_id, cell_ids):
    vl = collectd.Values(type='throughput')
    vl.plugin='cell'
    vl.plugin_instance='total'
    vl.host=enb_id
    vl.type_instance='dl'
    vl.interval=5
    vl.dispatch(values=[j_res["cells"]["1"]["dl_bitrate"]])
    vl.type_instance='ul'
    vl.dispatch(values=[j_res["cells"]["1"]["ul_bitrate"]])