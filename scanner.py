#!/usr/bin/python
# scanner.py
# USB Scanner

from wx.lib.pubsub import Publisher as pub

# Controller: Interacts with the hardware to return data
class Scanner:
    def __init__(self):
         self.scanners = []
    def addScanner(self, scanner):
         self.scanners.append(scanner)
    def scan(self):
         pub.sendMessage("SCANNING STARTED")
         for scanner in self.scanners:
              scanner.scan()
         pub.sendMessage("SCANNING ENDED")
