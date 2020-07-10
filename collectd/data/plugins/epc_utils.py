import collectd  
import json

def cpu_load(ws, result, epc_ip):
    try:
        j_res = json.loads(result)
        vl = collectd.Values(type='vcpu')
        vl.host = epc_ip
        vl.plugin = "resources"
        vl.plugin_instance = "mme"
        vl.type_instance = "single_core"
        vl.interval = 5
        val = j_res['cpu']['global']
        vl.dispatch(values=[val])
    except Exception as ex:
        print(ex)    

def s1_connections(ws, result, epc_ip):
    try:
        j_res = json.loads(result)
        vl = collectd.Values(type='count')
        vl.host=epc_ip
        vl.plugin="connections"
        vl.plugin_instance="mme"
        vl.type_instance="s1"
        vl.interval=5
        val=len(j_res['s1_connections'])
        vl.dispatch(values=[val])
    except Exception as ex:
        print(ex)    

def ng_connections(ws, result, epc_ip):
    try:
        j_res = json.loads(result)
        vl = collectd.Values(type='count')
        vl.host=epc_ip
        vl.plugin="connections"
        vl.plugin_instance="mme"
        vl.type_instance="ng"
        vl.interval=5
        val=len(j_res['ng_connections'])
        vl.dispatch(values=[val])
    except Exception as ex:
        print(ex)    