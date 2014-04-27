#!/usr/bin/python
# connector.py
# Handles ANT+ USB protocol interaction

import logging
import antd

_log = logging.getLogger("ant")

class AntScanner:
    def __init__(self):
         self.count = 0
    def scan(self):
         self.count = self.count+1
