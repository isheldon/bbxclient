import wx, wx.animate
import os.path

class ImagePanel(wx.Panel):
  def __init__(self, parent, pos = wx.DefaultPosition, size = wx.DefaultSize,
         imagePath = None, defaultImage = None):
    wx.Panel.__init__(self, parent, pos = pos, size = size)
    self.size = size
    self.SetBackgroundColour(wx.WHITE)
    self.animate = None
    self.imagePath = imagePath
    self.defaultImage = defaultImage

    self.indexed = False
    self.currentIndex = 1;

    self.LoadImage()
    # timer, refresh the image
    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
    self.timer.Start(1000 * 3600)

  def LoadImage(self):
    theImg = self.imagePath
    if self.indexed:
      indexImg = theImg + str(self.currentIndex)
      if os.path.isfile(indexImg):
        theImg = indexImg
        self.currentIndex = self.currentIndex + 1
      else:
        if self.currentIndex > 1:
          theImg = theImg + "1"
        self.currentIndex = 1

    if theImg == None or (not os.path.isfile(theImg)):
      theImg = self.defaultImage
      if self.animate != None:
        self.animate.Stop()
    else:
      if self.animate != None:
        self.animate.Play()

    image = wx.Image(theImg, wx.BITMAP_TYPE_JPEG)  
    image.Rescale(self.size[0], self.size[1])
    self.bmp = wx.StaticBitmap(parent=self, bitmap=image.ConvertToBitmap())  
    

  def SetImagePath(self, imagePath = None):
    self.imagePath = imagePath

  def SetTimerInterval(self, sec):
    self.timer.Start(1000 * sec)

  def OnTimer(self, event):
    self.LoadImage()

  def StopTimer(self):
    self.timer.Stop()

  def SetAnimate(self, animate):
    self.animate = animate


class AnimatePanel(wx.Panel):
  def __init__(self, parent, id = -1, pos = wx.DefaultPosition, size = wx.DefaultSize, gifPath = None):
    wx.Panel.__init__(self, parent, pos = pos, size = size)
    self.SetBackgroundColour("white")
    gif_fname = gifPath
    gif = wx.animate.GIFAnimationCtrl(self, id, gif_fname, pos=(-16, 0))
    gif.GetPlayer().UseBackgroundColour(True)
    self.gif = gif
    self.playing = False;

  def Play(self):
    if not self.playing:
      self.gif.Play()
      self.playing = True

  def Stop(self):
    if self.playing:
      self.gif.Stop()
      self.playing = False

