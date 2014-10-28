# -*- coding: utf-8 -*-

import wx, memcache

class CodePanel(wx.Panel):
  def __init__(self, parent, pos = wx.DefaultPosition, size = wx.DefaultSize):
    wx.Panel.__init__(self, parent, pos = pos, size = size)
    self.SetBackgroundColour(wx.WHITE)
 
    # cache that stores the consumer code
    self.ccCache = memcache.Client(['127.0.0.1:11211'], debug=0)
  
    # consumer code
    self.clientCode = None
    self.cctimer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.OnConsumerCodeTimer, self.cctimer)
    self.cctimer.Start(1000)

  def showConsumerCode(self):
    if self.clientCode != None:
      self.clientCode.Destroy()
    self.clientCode = wx.StaticText(self, -1, "████████████████", (0, 0))
    self.clientCode.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD))
    self.clientCode.SetForegroundColour(wx.WHITE)
    cCode = self.ccCache.get('ConsumerCode')

    fontsize = 16
    if cCode != None:
      if len(cCode) > 4:
        codetxt = cCode
        fontsize = 14
      else:
        codetxt = " 消费码:".decode("utf8") + (cCode or "")

      self.clientCode.Destroy()
      self.clientCode = wx.StaticText(self, -1, codetxt, (0,5))
      self.clientCode.SetFont(wx.Font(fontsize, wx.SWISS, wx.NORMAL, wx.BOLD))
      self.clientCode.SetForegroundColour(wx.BLACK)

  def OnConsumerCodeTimer(self, event):
    self.showConsumerCode()

