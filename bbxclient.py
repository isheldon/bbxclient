#!/usr/bin/env python

import wx, os

class Frame(wx.Frame):
    
    def __init__(self, image, parent=None):  
        wx.Frame.__init__(self, parent)  
        self.panel = wx.Panel(self)  
        self.bmp = wx.StaticBitmap(parent=self.panel, bitmap=image.ConvertToBitmap())  
	self.bmp.Bind(wx.EVT_LEFT_UP, self.onClick)

    def onClick(self, event):
        os.system("/usr/bin/onboard &")


class App(wx.App):  
    def OnInit(self):  
        image = wx.Image('/etc/bobox/bobox.jpg', wx.BITMAP_TYPE_JPEG)  
	image.Rescale(600, 1024)
        self.frame = Frame(image)  
        self.frame.Show()  
        self.frame.ShowFullScreen(True)  
#        self.SetTopWindow(self.frame)  
        return True  

def main():  
    app = App()  
    app.MainLoop()  

if __name__ == '__main__':  
    main() 

