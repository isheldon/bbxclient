import requests, lomoconf

def internet_on():
  try:
    requests.get(lomoconf.check_url(), timeout = 2)
    return True
  except Exception, e:
    return False

