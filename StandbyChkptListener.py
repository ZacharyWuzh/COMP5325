import threading
import socket
import sys
import json
from BalanceHandler import BalanceHandler
from GlobVar import Globvar


class StandbyChkptListener(threading.Thread):
  def __init__(self):
    super(StandbyChkptListener, self).__init__()
    self._stop_event = threading.Event()
    self.handler = BalanceHandler()
    self.pause_cond = threading.Condition(threading.Lock())
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.server_address = ('localhost', Globvar.SYNC_PORT)
    print('starting up on %s port %s' % self.server_address)
    self.sock.bind(self.server_address)

  def run(self):
    while True:
      if self._stop_event.is_set():
        break
      data, server = self.sock.recvfrom(4096)
      datalist = data.decode("utf-8").split(";")
      json_data = json.loads(datalist[0])
      action_id = int(datalist[1])
      self.handler.synchronize(json_data, action_id)

  def stop(self):
      self._stop_event.set()

  def stopped(self):
      return self._stop_event.is_set()

if __name__ == "__main__":
  server = StandbyChkptListener()
  server.run()