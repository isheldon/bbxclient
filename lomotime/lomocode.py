# -*- coding: utf-8 -*-

import wx, memcache

class CodePanel(wx.Panel):
  def __init__(self, parent, pos = wx.DefaultPosition, size = wx.DefaultSize):
    wx.Panel.__init__(self, parent, pos = pos, size = size)
 
    # static text for consumer code
    self.clientCodeLabel = wx.StaticText(self, -1, "消费码:", (0, 10))
    self.clientCodeLabel.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL))

    # cache that stores the consumer code
    self.ccCache = memcache.Client(['127.0.0.1:11211'], debug=0)
  
    # consumer code
    self.cctimer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.OnConsumerCodeTimer, self.cctimer)
    self.cctimer.Start(1000 * 2)

  def showConsumerCode(self):
    self.clientCode = wx.StaticText(self, -1, "████", (100, 10))
    self.clientCode.SetFont(wx.Font(22, wx.SWISS, wx.NORMAL, wx.BOLD))
    self.clientCode.SetForegroundColour(wx.WHITE)
    cCode = self.ccCache.get('ConsumerCode')
    if cCode != None:
      self.clientCode = wx.StaticText(self, -1, cCode, (100,10))
      self.clientCode.SetFont(wx.Font(22, wx.SWISS, wx.NORMAL, wx.BOLD))
      self.clientCode.SetForegroundColour(wx.RED)

  def OnConsumerCodeTimer(self, event):
    self.showConsumerCode()

