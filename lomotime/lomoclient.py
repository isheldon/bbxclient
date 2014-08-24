#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx, os
import lomohtml, lomoimg, lomocode, lomoconf

class Frame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None)
    self.Show()
    self.ShowFullScreen(True)

    # HTML page, size: 1350*1080
    lomohtml.HtmlPanel(self, pos = (0, 0), size = (1350, 1080))

    # background image, size: (1910-1350=560)*1080
    self.bgrImg = lomoimg.ImagePanel(self,
         pos = (1350, 0), size = (560, 1080),
         imagePath = "/etc/lomotime/background.jpg",
         defaultImage = "/etc/lomotime/default/background.jpg")
    self.bgrImg.SetTimerInterval(lomoconf.backgroupd_interval())

    # QR code image, pos: (1680, 450)
    self.qrCodeImg = lomoimg.ImagePanel(self,
         pos = (1680, 450), size = (200, 200),
         imagePath = "/etc/lomotime/qrcode.jpg",
         defaultImage = "/etc/lomotime/default/qrcode.jpg")
    self.qrCodeImg.SetTimerInterval(lomoconf.qrcode_interval())

    # consumer code, pos: (1680, 450+200=650)
    self.consumerCode = lomocode.CodePanel(self, pos = (1680, 650), size = (200, 50))

    # current printing image, pos: (1400, 400)
    self.printingImg = lomoimg.ImagePanel(self,
        pos = (1400, 400), size = (210, 280), 
        imagePath = "/tmp/lomoprinting.jpg",
        defaultImage = "/etc/lomotime/default/printing.jpg")
    self.printingImg.SetTimerInterval(lomoconf.current_print_interval())
    # printing indicator, pos: (1400, 400+280=680)
    self.printingGif = lomoimg.AnimatePanel(self,
        pos = (1400, 680), size = (210, 20),
        gifPath = "/etc/lomotime/default/printing.gif")
    self.printingImg.SetAnimate(self.printingGif)

    # call soft board and network config
    self.Bind(wx.EVT_LEFT_UP, self.OnClick)

  def OnClick(self, event):
    pos = event.GetPosition()
    if pos.x >= 1911 and pos.y <= 100:
      os.system("/usr/bin/onboard &")
      os.system("/usr/bin/wicd-gtk &")
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

