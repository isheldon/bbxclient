import base64

class LomoConfig:

  def __init__(self):
    prop_file = open("/etc/lomotime/config", 'r')
    try:
      self.props = {}
      for line in prop_file:
        if line.find('=') > 0:
          strs = line.replace('\n', '').split('=')
          if strs[1].find('@@') > 0:
            strs[1] = strs[1].replace("@@", "=")
          self.props[strs[0]] = strs[1]
    finally:
      prop_file.close()

    idfile = open('/etc/lomotime/machineid', "r")
    try:
      device_id = idfile.read().rstrip('\n')
      self.props["machine_id"] = device_id
    finally:
      idfile.close()

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
  encoded = inst().getProp("machine_id")
  return base64.decodestring(encoded + "\n")

def img_base_url():
  return inst().getProp("img_base_url")

def wximg_base_url():
  return inst().getProp("wximg_base_url")

def leftimg_base_url():
  return inst().getProp("leftimg_base_url")
  
def db_host():
  encoded = inst().getProp("db_host")
  return base64.decodestring(encoded + "=\n")
  
def db_usr():
  encoded = inst().getProp("db_usr")
  return base64.decodestring(encoded + "3\n")
  
def db_pwd():
  encoded = inst().getProp("db_pwd")
  return base64.decodestring(encoded + "4\n")
  
def db_name():
  encoded = inst().getProp("db_name")
  return base64.decodestring(encoded + "==\n")
  
def db_port():
  encoded = inst().getProp("db_port")
  return int(base64.decodestring(encoded + "==\n"))

def info_url():
  return inst().getProp("info_url")

def print_interval():
  return int(inst().getProp("print_interval"))

def consumer_code_interval():
  return int(inst().getProp("consumer_code_interval"))

def check_url():
  return inst().getProp("check_url")

def local_url():
  return inst().getProp("local_url")

def remote_url():
  return inst().getProp("remote_url")

def logo_url():
  return inst().getProp("logo_url")

def html_refresh_interval():
  return int(inst().getProp("html_refresh_interval"))

def backgroupd_interval():
  return int(inst().getProp("backgroupd_interval"))

def current_print_interval():
  return int(inst().getProp("current_print_interval"))

def qrcode_interval():
  return int(inst().getProp("qrcode_interval"))

def upgrade_url():
  return inst().getProp("upgrade_url")

