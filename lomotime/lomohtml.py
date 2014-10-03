# -*- coding: utf-8 -*-
import gobject
gobject.threads_init()

import pygtk
pygtk.require('2.0')
import gtk, gtk.gdk

# pywebkitgtk (http://code.google.com/p/pywebkitgtk/)
import webkit

import wx, os
import lomoconf, lomoutil

class HtmlWindow(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        # Here is where we do the "magic" to embed webkit into wxGTK.
        whdl = self.GetHandle()
        window = gtk.gdk.window_lookup(whdl)

        # We must keep a reference of "pizza". Otherwise we get a crash.
        self.pizza = pizza = window.get_user_data()

        self.scrolled_window = scrolled_window = pizza.parent

        # Removing pizza to put a webview in it's place
        scrolled_window.remove(pizza)

        self.ctrl = ctrl = webkit.WebView()
        scrolled_window.add(ctrl)

        scrolled_window.show_all()

    # Some basic usefull methods
    def SetEditable(self, editable=True):
        self.ctrl.set_editable(editable)

    def LoadUrl(self, url):
        self.ctrl.load_uri(url)

    def HistoryBack(self):
        self.ctrl.go_back()

    def HistoryForward(self):
        self.ctrl.go_forward()

    def StopLoading(self):
        self.ctrl.stop_loading()

class HtmlPanel(wx.Panel):
  def __init__(self, parent, pos, size):
    wx.Panel.__init__(self, parent, pos=pos, size=size)

    # read from config file 
    self.localUrl = lomoconf.local_url()
    self.remoteUrl = lomoconf.remote_url() + "&machineCode=" + lomoconf.machine_id()
    # print self.remoteUrl

    self.html = HtmlWindow(self, pos=pos, size=size)
    self.html.SetEditable(False)
    self.html.LoadUrl(self.localUrl)
    self.loadtime = 0
    self.remoteon = False

    # timer, check internet access
    self.htmltimer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.OnHtmlTimer, self.htmltimer)
    self.htmltimer.Start(1000 * lomoconf.html_refresh_interval())

    self.Layout()


  def OnHtmlTimer(self, event):
    if lomoutil.internet_on(): # the internet connection is fine
      if not self.remoteon:
        # load remote url and stop the timer
        self.html.LoadUrl(self.remoteUrl)
        if self.loadtime == 1:
          self.remoteon = True
        self.loadtime = self.loadtime + 1
    else:
      self.html.LoadUrl(self.localUrl)
      self.remoteon = False
      self.loadtime = 0

