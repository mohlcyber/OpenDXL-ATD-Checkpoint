#!/usr/bin/env python

import requests, json

def api_call(ip_addr, port, command, json_payload, sid):
    url = 'https://' + str(ip_addr) + ':' + str(port) + '/web_api/' + command
    if sid == '':
        request_headers = {'Content-Type' : 'application/json'}
    else:
        request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
    r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, verify=False)
    return r.json()

def login(user,password):
    payload = {'user':user, 'password' : password}
    response = api_call('1.1.1.1', 443, 'login',payload, '')
    return response["sid"]

def action(ipv4):

    sid = login('username','password')

    group_data = {'name':'BadIPList'}
    group_result = api_call('1.1.1.1', 443,'add-group', group_data ,sid)

    new_host_data = {'name':ip, 'ip-address':ip, 'comments':'Set Via OpenDXL', 'groups':'BadIPList'}
    new_host_result = api_call('1.1.1.1', 443,'add-host', new_host_data ,sid)

    publish_result = api_call('1.1.1.1', 443,"publish", {},sid)

    logout_result = api_call('1.1.1.1', 443,"logout", {},sid)
    print("Finished to import bad IP address")    

    return ip
