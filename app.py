"""Run app"""
# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/01/20 7:12 PM
import argparse
import os
import warnings
from http import HTTPStatus

from flask import Flask
from urllib3.exceptions import InsecureRequestWarning

from internal.config.config import Config
from internal.controllers.EndpointController import endpoint_blueprint
from internal.handler.auth import request_auth

warnings.simplefilter('ignore', InsecureRequestWarning)

app = Flask(__name__)
app.register_blueprint(endpoint_blueprint)


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

    request_auth(config)

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
