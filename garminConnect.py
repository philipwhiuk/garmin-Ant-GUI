#!/usr/bin/python
# garminConnect.py
# Handles interaction with remote endpoints

import requests
import logging

from wx.lib.pubsub import Publisher as pub

_log = logging.getLogger("garminConnect")

# Controller: A connect to control interaction with GarminConnect
class GarminConnector:
    def __init__(self):
        self.username = ""
        self.password = ""
    def sync(self):
        self.login()
    def login(self):
        self.rsession = requests.Session()
        gcPreResp = self.rsession.get("http://connect.garmin.com/", allow_redirects=False)
        # New site gets this redirect, old one does not
        if gcPreResp.status_code == 200:
            _log.warning("Using old login style")
        elif gcPreResp.status_code == 302:
            _log.warning("Using new style login")
            # JSIG CAS, cool I guess.
            # Not quite OAuth though, so I'll continue to collect raw credentials.
            # Commented stuff left in case this ever breaks because of missing parameters...
            data = {
                "username": self.username,
                "password": self.password,
                "_eventId": "submit",
                "embed": "true",
                # "displayNameRequired": "false"
            }
