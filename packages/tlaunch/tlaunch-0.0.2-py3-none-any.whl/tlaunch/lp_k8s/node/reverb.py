import launchpad as lp
from launchpad.nodes import base
from launchpad import address as lp_address
from absl import logging

class ReverbHandle(base.Handle):

  def __init__(self, address: lp_address.Address, Client):
    self._address = address
    self.Client = Client

  def dereference(self):
    address = self._address.resolve()
    logging.info('Reverb client connecting to: %s', address)
    return self.Client(address)

class ReverbNode(lp.ReverbNode):
  """Inherits `ReverbNode` from launchpad and remove `worker_manager` from it."""
