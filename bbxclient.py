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

class Frame(wx.Frame):
    
    def __init__(self, parent=None):  
        wx.Frame.__init__(self, parent)  
        self.panelMain = ImagePanel(self, '/etc/bobox/bobox.jpg', pos=(0, 0), size=(800, 768))  
	self.panelMain.bmp.Bind(wx.EVT_LEFT_UP, self.OnClick)

	self.timer = wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
	self.timer.Start(1000 * 10)

        self.panelQrcode = ImagePanel(self, '/etc/bobox/qrcode.jpg', pos=(800, 0), size=(224, 224))  


    def OnClick(self, event):
	pos = event.GetPosition()
	if pos.x <= 100 and pos.y <= 100:
            os.system("/usr/bin/onboard &")
            os.system("/usr/bin/nm-connection-editor &")

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

