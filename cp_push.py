#!/usr/bin/env python3
# Written by mohlcyber 15.05.2020 v.0.2

import sys
import requests
import json
import time

requests.packages.urllib3.disable_warnings()


class Checkpoint():
    def __init__(self, ip):
        cpip = 'ip-addr'
        cpport = '443'
        self.base_url = 'https://{0}:{1}/web_api/'.format(str(cpip), str(cpport))
        self.verify = False

        self.user = 'api'
        self.pw = 'password'

        self.group = 'BadIPList'
        self.ip = ip

        self.session = requests.Session()
        self.headers = {'Content-Type': 'application/json'}
        self.login()

        self.main()

    def login(self):
        try:
            payload = {
                'user': self.user,
                'password' : self.pw,
                'continue-last-session': 'true'
            }

            res = self.session.post(self.base_url + 'login', data=json.dumps(payload),
                                    headers=self.headers, verify=self.verify)

            if res.status_code == 200:
                self.headers['X-chkp-sid'] = res.json()["sid"]
            else:
                print('ERROR: login() - {0} - {1}'.format(str(res.status_code), res.text))
                sys.exit()
        except Exception as error:
            print('ERROR: login() - {0}'.format(str(error)))

    def api_call(self, command, payload):
        try:
            res = self.session.post(self.base_url + command, data=json.dumps(payload),
                                    headers=self.headers, verify=self.verify)

            if res.status_code == 200:
                print('STATUS: Run {0}.'.format(command))
            else:
                print('ERROR: api_call() - command: {0} - http: {1}-{2}'.format(command, res.status_code, res.text))
        except Exception as error:
            print('ERROR: api_call() - {0}'.format(str(error)))
            self.api_call('logout', {})

    def main(self):
        # self.api_call('show-group', {'name': self.group})
        # group_data = {'name': 'BadIPList'}
        # self.api_call('add-group', group_data)

        new_host_data = {'name': self.ip, 'ip-address': self.ip, 'comments': 'Set Via OpenDXL'}
        self.api_call('add-host', new_host_data)

        add_host_group_data = {'name': self.ip, 'groups': self.group}
        self.api_call('set-host', add_host_group_data)
        time.sleep(2)

        self.api_call('publish', {})
        time.sleep(5)

        self.api_call('logout', {})
        print("SUCCESS: Finished to import bad IP address")

if __name__ == '__main__':
    Checkpoint(sys.argv[1])