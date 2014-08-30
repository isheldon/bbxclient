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
  return inst().getProp("machine_id")

def img_base_url():
  return inst().getProp("img_base_url")

def wximg_base_url():
  return inst().getProp("wximg_base_url")
  
def db_host():
  return inst().getProp("db_host")
  
def db_usr():
  return inst().getProp("db_usr")
  
def db_pwd():
  return inst().getProp("db_pwd")
  
def db_name():
  return inst().getProp("db_name")
  
def db_port():
  return int(inst().getProp("db_port"))

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

def html_refresh_interval():
  return int(inst().getProp("html_refresh_interval"))

def backgroupd_interval():
  return int(inst().getProp("backgroupd_interval"))

def current_print_interval():
  return int(inst().getProp("current_print_interval"))

def qrcode_interval():
  return int(inst().getProp("qrcode_interval"))

