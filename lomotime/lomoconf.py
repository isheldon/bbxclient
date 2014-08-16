class LomoConfig:

  def __init__(self):
    prop_file = open("/etc/lomotime/config", 'r')
    self.props = {}
    for line in prop_file:
      if line.find('=') > 0:
        strs = line.replace('\n', '').split('=')
        self.props[strs[0]] = strs[1]
    prop_file.close()

  def getProp(self, key):
    return self.props[key]

def inst():
    global instance
    try:
      instance
    except:
      instance = LomoConfig()
    return instance

def machine_id():
  return inst().getProp("machine_id")
