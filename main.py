#!/usr/bin/python
# main.py
# Entry point for Application
import wx
import logging
from wx.lib.pubsub import Publisher as pub
from scanner import Scanner
from connector import Connector
from garminConnect import GarminConnector
from ant import AntScanner

# Model: Contains information on device
class DeviceData:
    def __init__(self):
         self.deviceName = "None"

# Model: Contains list of activities to sync with remote source
class ActivityList:
    def __init__(self):
         self.activityCount = 0
# View: Activity Tab
class ActivityTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
	self.title = wx.StaticText(self, label="Activities", pos=(20,0))
        self.syncActivities = wx.Button(self, wx.ID_ANY, "Sync activities", pos=(40, 30))

# View: Courses Tab
class CoursesTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.title = wx.StaticText(self, label="Courses", pos=(20,0))

# View: Workouts Tab
class WorkoutsTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.title = wx.StaticText(self, label="Workouts", pos=(20,0))

# View: Main Frame
class MainView(wx.Frame):
    def __init__(self, parent):
         wx.Frame.__init__(self, parent, title='ANT Agent for Linux', size=(640,480))
         # Menu Bar
         filemenu = wx.Menu()
         self.aboutMenuItem = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
         filemenu.AppendSeparator()
         self.exitMenuItem = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
         menuBar = wx.MenuBar()
         menuBar.Append(filemenu, "&File")
         self.SetMenuBar(menuBar)
         # Status Bar
         self.statusBar = self.CreateStatusBar()
         # Top Panel
         topPanel = wx.Panel(self)
         deviceData = wx.StaticText(topPanel, label="Device Details", pos=(20,0))
         device = wx.StaticText(topPanel, label="Your device: ", pos=(40, 30))
         status = wx.StaticText(topPanel, label="Status: ", pos=(40,60))
         lastSync = wx.StaticText(topPanel, label="Last sync: ", pos=(40, 90))
         self.scanForDevices = wx.Button(topPanel, wx.ID_ANY, "Scan for devices", pos=(40, 120))
         # Bottom Panel
         bottomPanel = wx.Panel(self)
         tabs = wx.Notebook(bottomPanel)
         activityTab = ActivityTab(tabs)
         self.syncActivities = activityTab.syncActivities
         tabs.AddPage(activityTab, "Activities")
         coursesTab = CoursesTab(tabs)
         tabs.AddPage(coursesTab, "Courses")
         workoutsTab = WorkoutsTab(tabs)
         tabs.AddPage(workoutsTab, "Workouts")
         
         sizer = wx.BoxSizer(wx.VERTICAL)
         sizer.Add(tabs, 1, wx.ALL|wx.EXPAND, 5)
         bottomPanel.SetSizer(sizer)
         # Layout
         self.sizer = wx.BoxSizer(wx.VERTICAL)
         self.sizer.Add(topPanel, 1, wx.EXPAND)
         self.sizer.Add(bottomPanel, 1, wx.EXPAND)
         self.SetSizer(self.sizer)
         self.SetAutoLayout(1)
         # self.sizer.Fit(self)
         self.Show(True)
    def setStatus(self, message):
         self.statusBar.SetStatusText(message)

# Controller : Handles logic for main screen
class MainController:
    def __init__(self, app):
        self.deviceData = DeviceData()
        self.view = MainView(None)
        self.view.scanForDevices.Bind(wx.EVT_BUTTON, self.ScanForDevices)
        self.view.syncActivities.Bind(wx.EVT_BUTTON, self.SyncActivities)
        self.view.Bind(wx.EVT_MENU, self.OnAbout, self.view.aboutMenuItem)
        self.view.Bind(wx.EVT_MENU, self.OnExit, self.view.exitMenuItem)
        self.view.Show()
        self.scanner = Scanner()
        ## TODO Preferences for Selected Scanners
        self.scanner.addScanner(AntScanner())
        self.connector = Connector()
        ## TODO Preferences for Selected Connectors
        self.connector.addConnector(GarminConnector())
        pub.subscribe(self.ScanningStarted, "SCANNING STARTED")
        pub.subscribe(self.DeviceDetected, "DEVICE DETECTED")
        pub.subscribe(self.ActivityRetrieved, "ACTIVITY RETRIEVED")
        pub.subscribe(self.ScanningEnded, "SCANNING ENDED")
        pub.subscribe(self.SyncStarted, "SYNC STARTED")
        pub.subscribe(self.SyncEnded, "SYNC ENDED")
        pub.subscribe(self.LoginSuccesful, "LOGIN SUCCESFUL")
        pub.subscribe(self.LoginFailed, "LOGIN FAILED")
        pub.subscribe(self.ActivitiesUploaded, "ACTIVITIES UPLOADED")
    def ScanForDevices(self, evt):
        self.scanner.scan()
    def ScanningStarted(self, evt):
        self.view.setStatus("Scanning started")
    def ScanningEnded(self, evt):
        self.view.setStatus("Scanning ended")
    def DeviceDetected(self, evt):
        self.view.setStatus("Device detected")
    def ActivityRetrieved(self, evt):
        self.view.setStatus("Retrieved activity")
    def SyncActivities(self, evt):
        self.connector.sync()
    def SyncStarted(self, evt):
        self.view.setStatus("Sync started")
    def SyncEnded(self, evt):
        self.view.setStatus("Sync ended")
    def LoginSuccesful(self, evt):
        self.view.setStatus("Login Succesful")
    def LoginFailed(self, evt):
        self.view.setStatus("Login Failed")
    def ActivitiesUploaded(self, evt):
        self.view.setStatus("Activities Uploaded")
    def OnExit(self,e):
        self.Close(True)
    def OnAbout(self, event):
        dlg = wx.MessageDialog( self.view, "A community-developed Linux version of the ANT Agent. Supports Garmin-based fitness devices that communicate either over USB serial or via the ANT USB connector. Developed by Philip Whitehouse, based on work by Braiden Kindt, Gustav Tiger and Collin (cpfair). Copyright 2014", "About ANT Agent for Linux", wx.OK);
        dlg.ShowModal()
        dlg.Destroy()
logging.basicConfig()
app = wx.App(False)
controller = MainController(app)
app.MainLoop()
