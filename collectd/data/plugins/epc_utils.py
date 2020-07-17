import collectd  
import json

def cpu_load(ws, j_res, epc_ip):
    try:
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

def s1_connections(ws, j_res, epc_ip):
    try:
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

def ng_connections(ws, j_res, epc_ip):
    try:
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

def s1_ue_connections(ws, j_res, epc_ip):
    try:
        vl = collectd.Values(type='count')
        vl.host=epc_ip
        vl.plugin="connections"
        vl.plugin_instance="s1_ue"
        vl.interval=5
        s1_con=j_res['s1_connections']
        for con in s1_con:
            print(con)
            vl.type_instance="\"plmn\":\"" + con['plmn'] + "\",\"enb_id_type\":\""\
                 + con['enb_id_type'] + "\",\"enb_id\":\"" + str(con['enb_id']) +"\",\"ip_addr\":\""\
                     + con['ip_addr'] + "\""
            vl.dispatch(values=[con['emm_connected_ue_count']])
    except Exception as ex:
        print(ex)    

def ng_ue_connections(ws, j_res, epc_ip):
    try:
        vl = collectd.Values(type='count')
        vl.host=epc_ip
        vl.plugin="connections"
        vl.plugin_instance="ng_ue"
        vl.interval=5
        s1_con=j_res['ng_connections']
        for con in s1_con:
            print(con)
            vl.type_instance="\"plmn\":\"" + con['plmn'] + "\",\"ran_id_type\":\""\
                 + con['ran_id_type'] + "\",\"ran_id\":\"" + str(con['ran_id']) +"\",\"ip_addr\":\""\
                     + con['ip_addr'] + "\""
            vl.dispatch(values=[con['cn_connected_ue_count']])
    except Exception as ex:
        print(ex)            