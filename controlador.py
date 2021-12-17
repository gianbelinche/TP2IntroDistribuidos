from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

log = core.getLogger()

class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        #regla 1
        #block = of.ofp_match()
        #block.tp_dst = 80 #Por alguna razon hay error con esta linea y no funciona
        #flow_mod = of.ofp_flow_mod()
        #flow_mod.match = block
        #event.connection.send(flow_mod)
        #log.debug("Firewall rules 1 installed on %s", dpidToStr(event.dpid))

        #regla 3
        block = of.ofp_match()
        block.dl_src = EthAddr('00:00:00:00:00:01')
        block.dl_dst = EthAddr('00:00:00:00:00:02')
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = block
        event.connection.send(flow_mod)
        log.debug("Firewall rules 3 installed on %s", dpidToStr(event.dpid))

def launch():
    core.registerNew(Firewall)