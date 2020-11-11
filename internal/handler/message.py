"""CDN download module"""
# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/28/20 9:34 PM
import json
from http import HTTPStatus

import requests

import internal
from internal.util.log import logger
from internal.util.tls import TLSAdapter


def file_read(proxy_url, code, filename):
    """

    :param proxy_url:
    :param code:
    :param filename:
    :return:
    """
    payload = {
        "code": code,
        "filename": filename
    }

    session = requests.Session()
    session.mount('https://', TLSAdapter())
    response = session.post(
        proxy_url,
        data=json.dumps(payload),
        headers=internal.handler.auth.AUTH_INSTANCE.bearer_header()
    )
    if response.status_code == HTTPStatus.OK:
        data = response.content
        return data

    logger.error("CDN прокси вернул ошибку")
    return None
