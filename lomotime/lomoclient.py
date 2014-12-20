#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx, os, subprocess
import lomoimg, lomocode, lomoconf

class Frame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None)
    self.Show()
    self.ShowFullScreen(True)

    #lomohtml.HtmlPanel(self, pos = (0, 0), size = (1370, 1080))
    # left side, a main image and 3 small images (1370, 1080)
    self.leftMainImg = lomoimg.ImagePanel(self,
         pos = (0, 0), size = (1370, 785),
         imagePath = "/etc/lomotime/leftmain.jpg",
         defaultImage = "/etc/lomotime/default/leftmain.jpg")
    self.leftMainImg.indexed = True
    self.leftMainImg.SetTimerInterval(10)

    self.leftBgImg = lomoimg.ImagePanel(self,
         pos = (0, 785), size = (1370, 295),
         imagePath = "/etc/lomotime/leftbg.jpg",
         defaultImage = "/etc/lomotime/default/leftbg.jpg")
    self.leftBgImg.StopTimer()

    self.left1Img = lomoimg.ImagePanel(self,
         pos = (5, 790), size = (450, 285),
         imagePath = "/etc/lomotime/left1.jpg",
         defaultImage = "/etc/lomotime/default/left1.jpg")
    self.left1Img.SetTimerInterval(15)
    self.left2Img = lomoimg.ImagePanel(self,
         pos = (460, 790), size = (450, 285),
         imagePath = "/etc/lomotime/left2.jpg",
         defaultImage = "/etc/lomotime/default/left2.jpg")
    self.left2Img.SetTimerInterval(15)
    self.left3Img = lomoimg.ImagePanel(self,
         pos = (915, 790), size = (450, 285),
         imagePath = "/etc/lomotime/left3.jpg",
         defaultImage = "/etc/lomotime/default/left3.jpg")
    self.left3Img.SetTimerInterval(15)


    # background image, size: (1910-1370=540)*1080
    self.bgrImg = lomoimg.ImagePanel(self,
         pos = (1370, 0), size = (540, 1080),
         imagePath = "/etc/lomotime/background.jpg",
         defaultImage = "/etc/lomotime/default/background.jpg")
    self.bgrImg.SetTimerInterval(lomoconf.backgroupd_interval())

    # QR code image, pos: (1665, 427)
    self.qrCodeImg = lomoimg.ImagePanel(self,
         pos = (1665, 427), size = (210, 210),
         imagePath = "/etc/lomotime/qrcode.jpg",
         defaultImage = "/etc/lomotime/default/qrcode.jpg")
    self.qrCodeImg.SetTimerInterval(lomoconf.qrcode_interval())

    # consumer code, pos: (1665, 427+210=637+2=639)
    self.consumerCode = lomocode.CodePanel(self, pos = (1665, 639), size = (210, 35))

    # current printing image, pos: (1420, 400)
    self.printingImg = lomoimg.ImagePanel(self,
        pos = (1420, 400), size = (210, 280), 
        imagePath = "/tmp/lomoprinting.jpg",
        defaultImage = "/etc/lomotime/default/printing.jpg")
    self.printingImg.SetTimerInterval(lomoconf.current_print_interval())
    # printing indicator, pos: (1420, 400+280=680)
    self.printingGif = lomoimg.AnimatePanel(self,
        pos = (1420, 680), size = (210, 20),
        gifPath = "/etc/lomotime/default/printing.gif")
    self.printingImg.SetAnimate(self.printingGif)

    # call soft board and network config
    self.Bind(wx.EVT_LEFT_UP, self.OnClick)

    # show machine id
    self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

  def OnClick(self, event):
    pos = event.GetPosition()
    if pos.x >= 1911 and pos.y <= 100:
      os.system("/usr/bin/wicd-gtk &")
      os.system("/usr/bin/onboard &")
    if pos.x >= 1911 and pos.y >= 980:
      dialog = OffDialog()
      result = dialog.ShowModal()
      dialog.Destroy()
      if result == wx.ID_OK:
        os.system("sudo halt -p")
      elif result == 111:
        os.system("sudo reboot")
      elif result == 112:
        os.system("~/client/lomorestartprint.sh")

  def OnRightClick(self, event):
    pos = event.GetPosition()
    if pos.x >= 1911 and pos.y <= 100:
      win = MachineIdWin()
      result = win.ShowModal()
      if result == wx.ID_OK:
        upgrade_cmd = "~/client/lomoupgrade.sh " + lomoconf.upgrade_url()
        upgrade_result = subprocess.check_output(upgrade_cmd, shell = True)
        print "upgrade result: " + upgrade_result # debug
        if upgrade_result == "100":
          upgradeMsg = "当前已是最新版本"
        elif upgrade_result == "200":
          upgradeMsg = "升级成功，请重启"
        elif upgrade_result == "1":
          upgradeMsg = "下载升级包失败，请稍后重试"
        else:
          upgradeMsg = "升级失败，请稍后重试"
        upgradeWin = UpgradeWin(upgradeMsg)
        upgradeWin.ShowModal()
        upgradeWin.Destroy()
      win.Destroy()

class OffDialog(wx.Dialog):
  def __init__(self):
    wx.Dialog.__init__(self, None, -1, '请选择您的操作', size=(420, 50))
    okButton = wx.Button(self, wx.ID_OK, "关机", pos=(15, 15))
    rebootButton = wx.Button(self, 111, "重启", pos=(115, 15))
    rebootButton.Bind(wx.EVT_LEFT_UP, self.OnReboot)
    printButton = wx.Button(self, 112, "打印复位", pos=(215, 15))
    printButton.Bind(wx.EVT_LEFT_UP, self.OnPrint)
    cancelButton = wx.Button(self, wx.ID_CANCEL, "取消", pos=(315, 15))
    cancelButton.SetDefault()
  def OnReboot(self, event):
    self.EndModal(111)
  def OnPrint(self, event):
    self.EndModal(112)
  def OnUpgrade(self, event):
    self.EndModal(113)

class MachineIdWin(wx.Dialog):
  def __init__(self):
    wx.Dialog.__init__(self, None, -1, '系统信息', size=(300, 100))
    machineId = wx.StaticText(self, -1, '机器码: ' + lomoconf.machine_id(), (5,5))
    machineId.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
    ver_txt = subprocess.check_output("cat ~/client/VER", shell = True)
    version = wx.StaticText(self, -1, '版本: ' + ver_txt, (5,35))
    version.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
    okButton = wx.Button(self, wx.ID_OK, "系统升级", pos=(5, 65))
    cancelButton = wx.Button(self, wx.ID_CANCEL, "取消", pos=(100, 65))
    cancelButton.SetDefault()

class PrintResetDialog(wx.Dialog):
 def __init__(self):
    wx.Dialog.__init__(self, None, -1, '请选择您的操作', size=(250, 50))
    okButton = wx.Button(self, wx.ID_OK, "打印复位", pos=(15, 15))
    cancelButton = wx.Button(self, wx.ID_CANCEL, "取消", pos=(115, 15))
    cancelButton.SetDefault()

class UpgradeWin(wx.Dialog):
  def __init__(self, upgradeMsg):
    wx.Dialog.__init__(self, None, -1, "升级结果", size=(300, 80))
    info = wx.StaticText(self, -1, upgradeMsg, (5,5))
    info.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
    info.SetForegroundColour(wx.BLACK)
    okButton = wx.Button(self, wx.ID_OK, "OK", pos=(100, 45))
    okButton.SetDefault()

if __name__ == '__main__':
  app = wx.App()
  fm = Frame()
  app.SetTopWindow(fm)  
  app.MainLoop()

