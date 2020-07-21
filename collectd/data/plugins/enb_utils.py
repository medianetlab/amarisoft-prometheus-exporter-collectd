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