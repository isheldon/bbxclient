#!/usr/bin/env python

import wx, os

class Frame(wx.Frame):
    
    def __init__(self, parent=None):  
        wx.Frame.__init__(self, parent)  
        self.panel = wx.Panel(self)  
	self.LoadImage()
	self.bmp.Bind(wx.EVT_LEFT_UP, self.OnClick)

	self.timer = wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
	self.timer.Start(1000 * 60 * 5)

    def LoadImage(self):
        image = wx.Image('/etc/bobox/bobox.jpg', wx.BITMAP_TYPE_JPEG)  
	image.Rescale(600, 1024)
        self.bmp = wx.StaticBitmap(parent=self.panel, bitmap=image.ConvertToBitmap())  

    def OnClick(self, event):
	pos = event.GetPosition()
	if pos.x <= 100 and pos.y <= 100:
            os.system("/usr/bin/onboard &")
            os.system("/usr/bin/nm-connection-editor &")

    def OnTimer(self, event):
	self.LoadImage()


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

