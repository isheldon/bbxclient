#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx, os, memcache, time

class ImagePanel(wx.Panel):
    def __init__(self, parent, imagePath, pos=wx.DefaultPosition, size=wx.DefaultSize):
	wx.Panel.__init__(self, parent, pos=pos, size=size)
	self.imagePath = imagePath
	self.size = size
	self.LoadImage()

    def LoadImage(self):
        image = wx.Image(self.imagePath, wx.BITMAP_TYPE_JPEG)  
	image.Rescale(self.size[0], self.size[1])
        self.bmp = wx.StaticBitmap(parent=self, bitmap=image.ConvertToBitmap())  

    def LoadSpecImage(self, imagePath):
        image = wx.Image(imagePath, wx.BITMAP_TYPE_JPEG)  
	image.Rescale(self.size[0], self.size[1])
        self.bmp = wx.StaticBitmap(parent=self, bitmap=image.ConvertToBitmap())  

class OffDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'Are you sure to power off?', size=(300, 50))
        okButton = wx.Button(self, wx.ID_OK, "OK", pos=(15, 15))
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel", pos=(115, 15))

class Frame(wx.Frame):
    
    def __init__(self, parent=None):  
        wx.Frame.__init__(self, parent)  

	# main image
        self.panelMain = ImagePanel(self, '/etc/bobox/bobox.jpg', pos=(0, 0), size=(600, 768))  
	self.panelMain.bmp.Bind(wx.EVT_LEFT_UP, self.OnClick)
	self.logoPics = []
	self.lastLogo = -1

	# timer, refresh main image
	self.timer = wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
	self.timer.Start(1000 * 10)

	# qrcode image
        self.panelQrcode = ImagePanel(self, '/etc/bobox/qrcode.jpg', pos=(800, 0), size=(224, 224))  
	self.qrcodeCache = memcache.Client(['127.0.0.1:11211'], debug=0)

	# timer, refresh qrcode
	self.qctimer = wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.OnQrCodeTimer, self.qctimer)
	self.qctimer.Start(1000 * 60)

	# static text for consumer code
	self.clientCodeLabel = wx.StaticText(self, -1, "消费码:", (820, 300))
	self.clientCodeLabel.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD))

	# consumer code
	self.cctimer = wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.OnConsumerCodeTimer, self.cctimer)
	self.cctimer.Start(1000 * 5)
	#self.showConsumerCode()

    def showConsumerCode(self):
	self.clientCode = wx.StaticText(self, -1, "████", (820, 350))
	self.clientCode.SetFont(wx.Font(22, wx.SWISS, wx.NORMAL, wx.BOLD))
	self.clientCode.SetForegroundColour(wx.WHITE)
	cCode = self.qrcodeCache.get('ConsumerCode')
        if cCode != None:
	    self.clientCode = wx.StaticText(self, -1, cCode, (820, 350))
	    self.clientCode.SetFont(wx.Font(22, wx.SWISS, wx.NORMAL, wx.BOLD))
	    self.clientCode.SetForegroundColour(wx.RED)


    def OnClick(self, event):
	pos = event.GetPosition()
	if pos.x <= 100 and pos.y <= 100:
            os.system("/usr/bin/onboard &")
            os.system("/usr/bin/nm-connection-editor &")
	if pos.x <= 50 and pos.y >= 718:
	    dialog = OffDialog()
            result = dialog.ShowModal()
            dialog.Destroy()
            if result == wx.ID_OK:
                os.system("sudo halt -p")

    def OnTimer(self, event):
        logos = os.listdir("/etc/bobox/logos/")
	if len(logos) == 0: # empty folder, display the defautl picture
	    self.panelMain.LoadImage()
	    self.logoPics = []
	    self.lastLogo = -1
        else: 
	    if self.logoPics == logos:  # means pictures not changed
                self.lastLogo = self.lastLogo + 1 # to display next picture
                if self.lastLogo >= len(logos): # need to start from the firt one
                    self.lastLogo = 0
	    else: # means pictures changed
                self.logoPics = logos
                self.lastLogo = 0 # to display the first one
	    self.panelMain.LoadSpecImage('/etc/bobox/logos/' + logos[self.lastLogo])

    def OnQrCodeTimer(self, event):
	self.panelQrcode.LoadImage()

    def OnConsumerCodeTimer(self, event):
	self.showConsumerCode()



class App(wx.App):  
    def OnInit(self):  
        self.frame = Frame()  
        self.frame.Show()  
        self.frame.ShowFullScreen(True)  
        self.SetTopWindow(self.frame)  
        return True  

def main():  
    app = App()  
    app.MainLoop()  

if __name__ == '__main__':  
    main() 

