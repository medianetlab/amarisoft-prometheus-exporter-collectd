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
        vl.plugin="s1_connections"
        vl.interval=5
        s1_con=j_res['s1_connections']
        for con in s1_con:
            vl.plugin_instance=str(con['enb_id'])
            vl.type_instance="\'plmn\':\'" + con['plmn'] + "\', \'enb_id_type\':\'"\
                 + con['enb_id_type'] + "\', \'ip_addr\':\'"\
                     + con['ip_addr'].split(":",1)[0] + "\'"
            vl.dispatch(values=[con['emm_connected_ue_count']])
    except Exception as ex:
        print(ex)    

def ng_connections(ws, j_res, epc_ip):
    try:
        vl = collectd.Values(type='count')
        vl.host=epc_ip
        vl.plugin="ng_connections"
        vl.interval=5
        ng_con=j_res['ng_connections']
        for con in ng_con:
            vl.plugin_instance=str(con['ran_id'])
            vl.type_instance="\'plmn\':\'" + con['plmn'] + "\',\'ran_id_type\':\'"\
                 + con['ran_id_type'] + "\',\'ip_addr\':\'"\
                     + con['ip_addr'].split(":",1)[0] + "\'"
            vl.dispatch(values=[con['cn_connected_ue_count']])
    except Exception as ex:
        print(ex)            

def ue_info(ws, j_res, epc_ip):
    try:
        vl = collectd.Values(type='info')
        vl.plugin="ue"
        vl.interval=5
        ue_list=j_res['ue_list']
        for ue in ue_list:
            vl.host=str(ue['enb_id'])
            vl.plugin_instance=str(ue['imsi'])
            vl.type_instance=str(ue['tac'])
            registered = 0
            enb_ue_id = -1
            mme_ue_id = -1
            if ue['registered']:
                registered = 1
                enb_ue_id = ue['enb_ue_id']
                mme_ue_id = ue['mme_ue_id']
            bearers = ue['bearers']
            dl_speed = 0
            ul_speed = 0
            for bearer in bearers:
                dl_speed = dl_speed + bearer['dl_total_bytes']
                ul_speed = ul_speed + bearer['ul_total_bytes']
            vl.dispatch(values=[dl_speed, ul_speed, enb_ue_id, mme_ue_id, registered])
    except Exception as ex:
        print(ex)      