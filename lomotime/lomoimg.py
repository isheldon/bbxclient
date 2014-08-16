import wx, wx.animate

class ImagePanel(wx.Panel):
  def __init__(self, parent, pos = wx.DefaultPosition, size = wx.DefaultSize, imagePath = None):
    wx.Panel.__init__(self, parent, pos = pos, size = size)
    self.size = size
    self.imagePath = imagePath
    self.LoadImage()
    # timer, refresh the image
    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
    self.timer.Start(1000 * 3600)

  def LoadImage(self):
    if self.imagePath is not None:
      image = wx.Image(self.imagePath, wx.BITMAP_TYPE_JPEG)  
      image.Rescale(self.size[0], self.size[1])
      self.bmp = wx.StaticBitmap(parent=self, bitmap=image.ConvertToBitmap())  

  def SetImagePath(self, imagePath = None):
    self.imagePath = imagePath

  def SetTimerInterval(self, sec):
    self.timer.Start(1000 * sec)

  def OnTimer(self, event):
    self.LoadImage()


class AnimatePanel(wx.Panel):
  def __init__(self, parent, id = -1, pos = wx.DefaultPosition, size = wx.DefaultSize, gifPath = None):
    wx.Panel.__init__(self, parent, pos = pos, size = size)
    self.SetBackgroundColour("white")
    gif_fname = gifPath
    gif = wx.animate.GIFAnimationCtrl(self, id, gif_fname)
    gif.GetPlayer().UseBackgroundColour(True)
    self.gif = gif

  def Play(self):
    self.gif.Play()

  def Stop(self):
    self.gif.Stop()

