# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/25/20 2:35 AM
import json
from datetime import datetime
from http import HTTPStatus

import requests

import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)


def as_date_format(date_string):
    return datetime.strptime(date_string[:-9], "%Y-%m-%dT%H:%M:%S.%f")


class Authentication:

    def __init__(self, auth_server_endpoint, login, refresh, username, password):
        self.refresh = refresh
        self.login = login
        self.auth_server_endpoint = auth_server_endpoint
        self.username = username
        self.password = password

        self.init = False
        self.token = None
        self.token_expired = None
        self.refresh_token = None
        self.refresh_token_expired = None
        self.pass_change = None

    def from_payload(self, payload):
        self.init = True
        self.token = payload["access"]["hash"]
        self.token_expired = as_date_format(payload["access"]["expires_at"])
        self.refresh_token = payload["refresh"]["hash"]
        self.refresh_token_expired = as_date_format(payload["refresh"]["expires_at"])
        self.pass_change = payload["pass_change_needed"]
        pass

    def authorization(self):
        session = requests.Session()
        session.auth = (self.username, self.password)
        response = session.post(self.auth_server_endpoint + self.login, verify=False)

        if response.status_code == HTTPStatus.OK:
            self.from_payload(json.loads(response.content))
        else:
            pass  # todo logging
        pass

    def refresh_authorization(self):
        payload = {
            "token_hash": self.refresh_token
        }

        response = requests.post(self.auth_server_endpoint + self.refresh_token, data=payload, verify=False)
        if response.status_code == HTTPStatus.OK:
            self.from_payload(json.loads(response.content))
        else:
            pass  # todo logging
        pass

    def bearer_header(self):

        if self.token_expired < datetime.now():
            if self.refresh_token < datetime.now():
                self.authorization()
            else:
                self.refresh_authorization()
            pass

        return {
            "Authorization": "Bearer " + self.token
        }

    pass
