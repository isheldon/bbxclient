#!/usr/bin/env python

import wx, os

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
        self.panelMain = ImagePanel(self, '/etc/bobox/bobox.jpg', pos=(0, 0), size=(800, 768))  
	self.panelMain.bmp.Bind(wx.EVT_LEFT_UP, self.OnClick)

	# timer, refresh main image
	self.timer = wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
	self.timer.Start(1000 * 20)

	# qrcode image
        self.panelQrcode = ImagePanel(self, '/etc/bobox/qrcode.jpg', pos=(800, 0), size=(224, 224))  

	# static text for client code
	self.clientCodeLabel = wx.StaticText(self, -1, "CLIENT CODE", (820, 300))
	self.clientCodeLabel.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

	# client code
	cCode = "123456"
	self.clientCode = wx.StaticText(self, -1, cCode, (820, 350))
	self.clientCode.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
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
	self.panelMain.LoadImage()


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

