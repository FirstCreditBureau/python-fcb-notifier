"""Run app"""
# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/01/20 7:12 PM
from http import HTTPStatus

from flask import Flask

from internal.config.config import Config
from internal.handler.auth import Authentication
from internal.util.log import get_logger

app = Flask(__name__)

logger = get_logger()
AUTHENTICATION = None


@app.route('/health', methods=["GET"])
def health():
    """

    :rtype: object
    """
    return {"Code": HTTPStatus.OK, "Status": "ok"}, HTTPStatus.OK


if __name__ == '__main__':
    config = Config()

    AUTHENTICATION = Authentication(config.fcb_notifier_host, config.auth)
    AUTHENTICATION.authorization()

    app.run(host="0.0.0.0", port=config.port)
