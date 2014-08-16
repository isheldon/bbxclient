#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx, lomohtml, lomoimg, os

class Frame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None)
    self.Show()
    self.ShowFullScreen(True)
    lomohtml.HtmlPanel(self, pos = (0, 0), size = (1700, 1080))
    self.bgrImg = lomoimg.ImagePanel(self,
         pos = (1700, 0), size = (210, 1080), imagePath = "/etc/lomotime/default/background.jpg")
    self.qrCodeImg = lomoimg.ImagePanel(self,
         pos = (1725, 300), size = (150, 150), imagePath = "/etc/lomotime/default/qrcode.jpg")
    self.qrCodeImg.SetTimerInterval(60)

    self.printingImg = lomoimg.ImagePanel(self,
         pos = (1700, 830), size = (210, 210), imagePath = "/etc/lomotime/default/printing.jpg")
    self.printingGif = lomoimg.AnimatePanel(self,
        pos = (1700, 1030), size = (210, 50), gifPath = "/etc/lomotime/default/printing.gif")

    # call soft board and network config
    self.Bind(wx.EVT_LEFT_UP, self.OnClick)

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

class OffDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '确定要关机吗？', size=(300, 50))
        okButton = wx.Button(self, wx.ID_OK, "确定", pos=(15, 15))
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, "取消", pos=(115, 15))


if __name__ == '__main__':
  app = wx.App()
  fm = Frame()
  app.SetTopWindow(fm)  
  app.MainLoop()

