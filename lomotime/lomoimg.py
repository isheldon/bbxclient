import wx

class ImagePanel(wx.Panel):
  def __init__(self, parent, pos = wx.DefaultPosition, size = wx.DefaultSize, imagePath = None):
    wx.Panel.__init__(self, parent, pos = pos, size = size)
    self.size = size
    self.imagePath = imagePath
    self.LoadImage()

  def LoadImage(self):
    if self.imagePath is not None:
      image = wx.Image(self.imagePath, wx.BITMAP_TYPE_JPEG)  
      image.Rescale(self.size[0], self.size[1])
      self.bmp = wx.StaticBitmap(parent=self, bitmap=image.ConvertToBitmap())  

