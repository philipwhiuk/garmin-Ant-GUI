#!/usr/bin/python
# connector.py
# Handles interaction with remote endpoints

from wx.lib.pubsub import Publisher as pub

# Controller: Interacts with remote sites to synchronize activities
class Connector:
    def __init__(self):
          self.activityCount = 0
    def sync(self):
         pub.sendMessage("SYNC STARTED")
         """
         TODO Synchronization
         """
         pub.sendMessage("SYNC ENDED")                                            
