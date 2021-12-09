from mininet.topo import Topo

class Topologia(Topo):
    def __init__(self,n=2):

        Topo.__init__(self)

        switches = []

        for i in range(0,n):
            switches.append(self.addSwitch("switch_{}".format(i)))

        h1 = self.addHost("host_1")
        h2 = self.addHost("host_2")
        h3 = self.addHost("host_3")
        h4 = self.addHost("host_4")

        self.addLink(h1,switches[0])
        self.addLink(h2,switches[0])
        self.addLink(h3,switches[-1])
        self.addLink(h4,switches[-1])

        for i in range(0,n-1):
            self.addLink(switches[i],switches[i+1])



topos = { "tp2": Topologia }

#Topologia se grafica bien, a partir de 5 switches empieza a fallar pingall (usando controlador pox, con controlador default anda bien)