#!/usr/bin/python
# connector.py
# Handles interaction with remote endpoints

from wx.lib.pubsub import Publisher as pub

# Controller: Interacts with remote sites to synchronize activities
class Connector:
    def __init__(self):
         self.connectors = []
    def addConnector(self, connector):
         self.connectors.append(connector)
    def sync(self):
         pub.sendMessage("SYNC STARTED")
         for connector in self.connectors:
              connector.sync()
         pub.sendMessage("SYNC ENDED")                                            
