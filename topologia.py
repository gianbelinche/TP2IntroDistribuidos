from mininet.topo import Topo

class Topologia(Topo):
    def build(self, switches=2):
        
        switches = max(switches, 1)

        swtches = []
        
        for i in range(0,switches):
            swtches.append(self.addSwitch("switch_{}".format(i)))
    
        h1 = self.addHost("host_1")
        h2 = self.addHost("host_2")
        h3 = self.addHost("host_3")
        h4 = self.addHost("host_4")

        self.addLink(h1,swtches[0])
        self.addLink(h2,swtches[0])
        self.addLink(h3,swtches[-1])
        self.addLink(h4,swtches[-1])

        for i in range(0,switches-1):
            self.addLink(swtches[i],swtches[i+1])


class Ejemplo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create switch
        s1 = self.addSwitch("switch_1")
        s2 = self.addSwitch("switch_2")

        # Create hosts
        h1 = self.addHost("host_1")
        h2 = self.addHost("host_2")
        h3 = self.addHost("host_3")

        # Add links between switches and hosts 
        self.addLink(s1, s2)
        self.addLink(s1, h1)
        self.addLink(s1, h2)
        self.addLink(s2, h3)


topos = { "tp2": Topologia ,"ejemplo" : Ejemplo}
