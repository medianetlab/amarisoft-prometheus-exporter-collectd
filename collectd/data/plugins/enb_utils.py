import collectd  
import json

def cpu_load(ws, j_res, enb_ip):
    try:
        vl = collectd.Values(type='vcpu')
        vl.host = enb_ip
        vl.plugin = "resources"
        vl.plugin_instance = "enb"
        vl.type_instance = "single_core"
        vl.interval = 5
        val = j_res['cpu']['global']
        vl.dispatch(values=[val])
    except Exception as ex:
        print(ex)    