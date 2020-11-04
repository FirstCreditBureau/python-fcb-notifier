"""Run app"""
# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/01/20 7:12 PM
from http import HTTPStatus

from flask import Flask

from internal.config.config import Config
from internal.handler.auth import Authentication

app = Flask(__name__)

config = Config()
config.load_config()

AUTHENTICATION = Authentication(config.fcb_notifier_host, config.auth)
AUTHENTICATION.authorization()


@app.route('/health', methods=["GET"])
def health():
    """

    :rtype: object
    """
    return {"Code": HTTPStatus.OK, "Status": "ok"}, HTTPStatus.OK


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.port)
