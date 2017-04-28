#!/usr/bin/env python

import requests, json, time

mgmtip = "ip-addr"
port = "443"
user = "api"
pw = "password"

def api_call(ip_addr, port, command, json_payload, sid):
    url = 'https://' + str(ip_addr) + ':' + str(port) + '/web_api/' + command
    if sid == '':
        request_headers = {'Content-Type' : 'application/json'}
    else:
        request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
    r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, verify=False)
    return r.json()

def login(user,password):
    payload = {'user':user, 'password' : password, 'continue-last-session':'true'}
    response = api_call(mgmtip, port, 'login', payload, '')
    return response["sid"]

def action(ip):

    sid = login(user,pw)
    print("session id: " + sid)
    
    # Create a new group called BadIPList
    group_data = {'name':'BadIPList'}
    group = api_call(mgmtip, port,'add-group', group_data ,sid)
    print(json.dumps(group))

    # Create a new host
    new_host_data = {'name':ip, 'ip-address':ip, 'comments':'Set Via OpenDXL'}
    new_host = api_call(mgmtip, port,'add-host', new_host_data ,sid)
    print(json.dumps(new_host))

    # Add the new created host to the BadIPList group
    add_host_group_data = {'name':ip, 'groups':'BadIPList'}
    add_host_group = api_call(mgmtip, port, 'set-host', add_host_group_data, sid)
    print(json.dumps(add_host_group))
    time.sleep(2)

    publish = api_call(mgmtip, port,"publish", {},sid)
    print("publish result: " + json.dumps(publish))
    time.sleep(5)

    logout_result = api_call(mgmtip, 443,"logout", {},sid)
    print("logout result: " + json.dumps(logout_result))
    print("Finished to import bad IP address")    

    return ip
