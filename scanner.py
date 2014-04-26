#!/usr/bin/python
# main.py
# USB Scanner

from wx.lib.pubsub import Publisher as pub

# Controller: Interacts with the hardware to return data
class Scanner:
    def __init__(self):
          self.deviceCount = 0
    def scan(self):
         pub.sendMessage("SCANNING STARTED")
         """
         TODO Scanning
         """
         pub.sendMessage("SCANNING ENDED")
