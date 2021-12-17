from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

TCP = 6
UDP = 17
IP = 0X800

log = core.getLogger()

class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        self.regla_1(event)
        self.regla_2(event)
        self.regla_3(event)

    def regla_1(self,event):
        #Todo lo que vaya al puerto 80 debe descartarse
        block = of.ofp_match()
        block.dl_type=IP
        block.nw_proto=TCP 
        block.tp_dst = 80 #Para poder seleccionar que el puerto sea el 80, deben si o si especificarse las capas anteriores, es decir, IP y TCP
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = block
        event.connection.send(flow_mod)

        block = of.ofp_match()
        block.dl_type=IP
        block.nw_proto=UDP
        block.tp_dst = 80
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = block
        event.connection.send(flow_mod)
        log.debug("Firewall rules 1 installed on %s", dpidToStr(event.dpid))

    def regla_2(self,event):
        #Mensajes provenientes del host 1, UDP, puerto destino 5001 se descartan
        block = of.ofp_match()
        block.dl_type=IP
        block.nw_proto=UDP
        block.tp_dst = 5001
        block.dl_src = EthAddr('00:00:00:00:00:01')
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = block
        event.connection.send(flow_mod)
        log.debug("Firewall rules 1 installed on %s", dpidToStr(event.dpid))

    def regla_3(self,event):
        #Los hosts 1 y 2 no pueden comunicarse
        block = of.ofp_match()
        block.dl_src = EthAddr('00:00:00:00:00:01')
        block.dl_dst = EthAddr('00:00:00:00:00:02')
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = block
        event.connection.send(flow_mod)
        log.debug("Firewall rules 3 installed on %s", dpidToStr(event.dpid))

def launch():
    core.registerNew(Firewall)