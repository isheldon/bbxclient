#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wxversion
wxversion.select("2.8")
import wx, os, requests
from webkit_gtk import WKHtmlWindow as HtmlWindow

class HtmlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.html = HtmlWindow(self, size=(1910, 1080))
        self.html.SetEditable(False)
        self.html.LoadUrl("file:///home/sheldon/ltpage/8.html")

        # call soft board and network config
	self.Bind(wx.EVT_LEFT_UP, self.OnClick)

	# timer, check internet access
	self.htmltimer = wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.OnHtmlTimer, self.htmltimer)
	self.htmltimer.Start(1000 * 10)

        self.Layout()

    def OnClick(self, event):
	pos = event.GetPosition()
	if pos.x >= 1911 and pos.y <= 100:
            os.system("/usr/bin/onboard &")
            os.system("/usr/bin/nm-connection-editor &")
	if pos.x >= 1911 and pos.y >= 980:
	    dialog = OffDialog()
            result = dialog.ShowModal()
            dialog.Destroy()
            if result == wx.ID_OK:
                os.system("sudo halt -p")

    def OnHtmlTimer(self, event):
	checkUrl = "http://www.lomotime.cn/"
        localUrl = "file:///home/sheldon/ltpage/8.html"
        remoteUrl = "http://www.lomotime.cn/"
        req = requests.get(checkUrl)
        if req.status_code == 200: # the internet connection is fine
            self.html.LoadUrl(remoteUrl)
        else:
            self.html.LoadUrl(localUrl)

class OffDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'Are you sure to power off?', size=(300, 50))
        okButton = wx.Button(self, wx.ID_OK, "OK", pos=(15, 15))
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel", pos=(115, 15))

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.Show()
        self.ShowFullScreen(True)
        HtmlPanel(self)

if __name__ == '__main__':
    app = wx.App()
    fm = Frame()
    app.SetTopWindow(fm)  
    app.MainLoop()

