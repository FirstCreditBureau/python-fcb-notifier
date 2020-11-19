# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/25/20 7:26 PM
import json
import logging
import sys
import datetime as dt

log_object = {
    "message": "%(message)s",
    "timestamp": "%(asctime)s",  # 2020-11-19T22:34:54.036
    "severity": "%(levelname)s",
    "caller": "%(module)s",
    # "addr": "%(remote_addr)s"
}


class FilterNoQuotes(logging.Filter):

    def filter(self, record):
        record.msg = record.msg.replace('"', '')
        return record


class Formatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp

    def formatMessage(self, record):
        return self._style.format(record)

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%dT%H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s


def get_logger():
    logger_ = logging.getLogger("werkzeug")
    logger_.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter(json.dumps(log_object), datefmt="%Y-%m-%dT%H:%M:%S.%f")
    formatter = Formatter(json.dumps(log_object))
    log_handler.setFormatter(formatter)
    logger_.addHandler(log_handler)
    logger_.addFilter(FilterNoQuotes())
    return logger_


logger = get_logger()
