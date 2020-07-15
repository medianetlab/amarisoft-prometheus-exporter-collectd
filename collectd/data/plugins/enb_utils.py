import collectd  
import json

def cpu_load(ws, result, epc_ip):
    try:
        j_res = json.loads(result)
        vl = collectd.Values(type='vcpu')
        vl.host = epc_ip
        vl.plugin = "resources"
        vl.plugin_instance = "enb"
        vl.type_instance = "single_core"
        vl.interval = 5
        val = j_res['cpu']['global']
        vl.dispatch(values=[val])
    except Exception as ex:
        print(ex)    