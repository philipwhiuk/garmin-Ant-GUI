#!/usr/bin/python
# main.py
# Entry point for Application
import wx
class AgentFrame(wx.Frame):
    def __init__(self, parent, title):
         wx.Frame.__init__(self, parent, title=title, size=(640,480))
         filemenu = wx.Menu()
         aboutMenuItem = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
         self.Bind(wx.EVT_MENU, self.OnAbout, aboutMenuItem)
         filemenu.AppendSeparator()
         exitMenuItem = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
         self.Bind(wx.EVT_MENU, self.OnExit, exitMenuItem)
         menuBar = wx.MenuBar()
         menuBar.Append(filemenu, "&File")
         self.SetMenuBar(menuBar)
         self.Show(True)
    def OnAbout(self, event):
	dlg = wx.MessageDialog( self, "A community-developed Linux version of the ANT Agent. Supports Garmin fitness devices", "About ANT Agent for Linux", wx.OK)
        dlg.ShowModal()
	dlg.Destroy()
    def OnExit(self,e):
        self.Close(True)

app = wx.App(False)
frame = AgentFrame(None, 'ANT Agent for Linux')
app.MainLoop()
