import socket, lomoconf

def internet_on():
  try:
    host = socket.gethostbyname(lomoconf.check_url())
    socket.create_connection((host, 80), 5)
    return True
  except Exception, e:
    pass
  return False

