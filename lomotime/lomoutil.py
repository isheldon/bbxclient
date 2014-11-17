import socket, lomoconf

def internet_on():
  try:
    socket.create_connection((lomoconf.check_url(), 80), 5)
    return True
  except Exception, e:
    pass
  return False

