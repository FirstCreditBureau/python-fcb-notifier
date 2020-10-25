# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/25/20 7:26 PM
import json
import logging
import sys

log_object = {
    "message": "%(message)s",
    "timestamp": "%(asctime)s",
    "severity": "%(levelname)s",
    "caller": "%(module)s",
    # "addr": "%(remote_addr)s"
}


def get_logger():
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(json.dumps(log_object))
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    return logger
