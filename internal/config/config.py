"""Config"""
# Created by Жасулан Бердибеков <zhasulan87@gmail.com> at 10/28/20 9:00 PM
import json

from internal.handler.auth import Auth


class Config:

    def __init__(self):
        self.port = None
        self.auth = None
        self.fcb_notifier_host = None

    def load_config(self):
        with open('./config/conf.json', 'r') as f:
            config = json.load(f)

        self.port = config["app_port"]
        self.auth = Auth(
            config["auth"]["login"], config["auth"]["refresh"], config["auth"]["username"], config["auth"]["password"]
        )
        self.fcb_notifier_host = config["fcb_notifier_host"]
