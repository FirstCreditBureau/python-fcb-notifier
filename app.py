"""Run app"""
# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/01/20 7:12 PM
import argparse
import os
from http import HTTPStatus

from flask import Flask

from internal.config.config import Config
from internal.handler.auth import Authentication
from internal.util.log import logger

app = Flask(__name__)

AUTHENTICATION = None


@app.route('/health', methods=["GET"])
def health():
    """

    :rtype: object
    """
    return {"Code": HTTPStatus.OK, "Status": "ok"}, HTTPStatus.OK


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def main(config_file):
    if config_file is None:
        config_file = "./config/conf.json"
    config = Config()
    config.load_config(config_file)

    AUTHENTICATION = Authentication(config.fcb_notifier_host, config.auth)
    AUTHENTICATION.authorization()

    app.run(host="0.0.0.0", port=config.port)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Сервис для приема сообщении от ПКБ')

    parser.add_argument(
        "--config",
        dest="config",
        required=False,
        help="Конфигурационный файл",
        metavar="FILE",
        type=lambda x: is_valid_file(parser, x)
    )

    args = parser.parse_args()
    main(args.config)
