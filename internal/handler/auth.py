"""This module specified Authentication Class"""
# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/25/20 2:35 AM
import json
from datetime import datetime
from http import HTTPStatus

import requests

from internal.util.log import logger
from internal.util.tls import TLSAdapter

AUTH_INSTANCE = None


def request_auth(config):
    global AUTH_INSTANCE
    AUTH_INSTANCE = Authentication(config.fcb_notifier_host, config.auth)
    AUTH_INSTANCE.authorization()
    pass


def as_date_format(date_string):
    """

    :rtype: object
    """
    return datetime.strptime(date_string[:-9], "%Y-%m-%dT%H:%M:%S.%f")


class LoginResult:
    """Login Result data storage"""

    def __init__(self):
        self.token = None
        self.token_expired = None
        self.refresh_token = None
        self.refresh_token_expired = None
        self.pass_change = None

    def from_payload(self, payload):
        """

        :rtype: object
        """
        self.token = payload["access"]["hash"]
        self.token_expired = as_date_format(payload["access"]["expires_at"])
        self.refresh_token = payload["refresh"]["hash"]
        self.refresh_token_expired = as_date_format(payload["refresh"]["expires_at"])
        self.pass_change = payload["pass_change_needed"]


class Auth:
    """Auth data storage"""

    def __init__(self, login_method, refresh_method, username, password):
        self.refresh_method = refresh_method
        self.login_method = login_method
        self.username = username
        self.password = password


class Authentication:
    """Main class for authentication"""

    def __init__(self, auth_server_endpoint, auth):
        self.auth_server_endpoint = auth_server_endpoint
        self.auth = auth
        self.login = LoginResult()

    def authorization(self):
        """

        :return: bool
        """
        session = requests.Session()
        # session.verify = False
        session.mount('https://', TLSAdapter())
        session.auth = (self.auth.username, self.auth.password)

        response = session.post(self.auth_server_endpoint + self.auth.login_method)

        if response.status_code == HTTPStatus.OK:
            self.login.from_payload(json.loads(response.content))
            return True

        logger.error("request response error: %s", response.content.decode("utf-8"))
        return False

    def refresh_authorization(self):
        """

        :return: bool
        """
        payload = {
            "token_hash": self.login.refresh_token
        }

        session = requests.Session()
        session.mount('https://', TLSAdapter())
        response = session.post(self.auth_server_endpoint + self.auth.refresh_method, data=payload)

        if response.status_code == HTTPStatus.OK:
            self.login.from_payload(json.loads(response.content))
            return True

        logger.error("request response error: %s", response.content.decode("utf-8"))
        return False

    def bearer_header(self):
        """

        :return:
        """
        if self.login.token_expired < datetime.now():
            if self.login.refresh_token < datetime.now():
                auth_result = self.authorization()
            else:
                auth_result = self.refresh_authorization()
        else:
            auth_result = True

        if auth_result:
            return {
                "Authorization": "Bearer " + self.login.token
            }

        return None
