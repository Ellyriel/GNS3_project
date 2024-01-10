import json
import bgp
import interface_function
import debut_cfg
import fin_cfg

with open("data.json") as file:
    data = json.load(file)
    
ip_version = int(data["ip_version"])

# classe définissant un routeur
class Router :

    def __init__ (self, hostname, id, AS, AS_RP, Area, neighbors, interfaces) :
        self.hostname = hostname
        self.id = id
        self.AS = AS
        self.AS_RP = AS_RP
        self.Area = Area
        self.neighbors = neighbors
        self.interfaces = interfaces
        
    def __str__(self):
        return f'[{self.hostname} : AS n°{self.AS} with {self.AS_RP} routing protocol, Router ID {self.id}, {len(self.neighbors)} neighbor(s), {len(self.interfaces)} interface(s)]'
    
    def __repr__(self):
        return f'Router {self.hostname}'


# classe définissant une interface d'un routeur
class Interface :

    def __init__ (self, name, ip_address, network, routing_protocols, connected_to) :
        self.name = name
        self.ip_address = ip_address
        self.network = network
        self.routing_protocols = routing_protocols
        self.connected_to = connected_to

    def __str__(self):
        return f'[Interface {self.name} : IP Address {self.ip_address}, Routing Protocols {self.routing_protocols}, Connected to {(self.connected_to)}]'
    
    def __repr__(self):
        return f'Interface {self.name}'



# mise en forme des données de chacun des routeurs
list_routers = []
for router in data["router"]:
    hostname = router["hostname"]
    AS = router["AS"]
    AS_RP = router["AS_RP"]
    Area = router["Area"]
    id = router["id"]
    neighbors = router["neighbors"]

    list_interfaces = []
    for interface in router["interfaces"]:
        name = interface["name"]
        ip_address = None
        network = None
        routing_protocols = interface["routing_protocols"]
        connected_to = interface["connected_to"]
        list_interfaces.append(Interface(name, ip_address, network, routing_protocols, connected_to))

    list_routers.append(Router(hostname,id,AS,AS_RP,Area,neighbors,list_interfaces))

#création de la fonction qui automatise les @ ipv6

def num_ip(router1, router2):
    num_router1 = int(router1.hostname[1:])
    num_router2 = int(router2.hostname[1:])
    if num_router1 < num_router2:
        numero = num_router1*10 + num_router2
    else :
        numero = num_router2*10 + num_router1
    return str(numero)
    

def generer_ip_network(router1,router2):
    numero = num_ip(router1, router2)
    address_ip = "2001:100:" + router1.AS + ":" + numero + ":0:0:0:" + router.hostname[1:] + "/64"
    network = "2001:100:" + router1.AS + ":" + numero + ":0:0:0:0" + "/64"
    return address_ip, network

def generer_ip_network_loopback(router):
    address_ip = "2001:100:0:0:0:0:0:"+ router.hostname[1:] + "/128"
    network = "2001:100:0:0:0:0:0:0/128"
    return address_ip, network



for router in list_routers:
    for interface in router.interfaces:
        if interface.name == "Loopback0":
            interface.ip_address, interface.network= generer_ip_network_loopback(router)
        if interface.connected_to != None and interface.name != "Loopback0":
            a = 0
            router2 = list_routers[a]
            while router2.hostname != interface.connected_to and a < len(list_routers):
                a += 1
                router2 = list_routers[a]
            interface.ip_address, interface.network= generer_ip_network(router,router2)



# affiche la liste des routeurs, leurs interfaces et leurs voisins
def affichage(list_routers):
    for router in list_routers:
        print(router)
        print("List of neighbor(s) :")
        print(f'    {router.neighbors}')
        print("List of interface(s) :")
        for interface in router.interfaces:
            print(f'    {interface}')
        print("------------")
    print(list_routers)

# génération des fichiers de configuration
def creation_fichier(hostname):
    name = "config_"+ hostname + ".cfg"
    f = open(name,"w")
    return f

for router in list_routers:
    fichier_config = creation_fichier(router.hostname)
    debut_cfg.creation_texte_debut(router.hostname, ip_version, fichier_config)
    interface_function.configureinterface(router, fichier_config)
    bgp.configureBGP(list_routers, router.hostname, router.id, router.AS, fichier_config)
    fin_cfg.creation_texte_fin(router.hostname, router.id, router.AS_RP, router.interfaces, ip_version, fichier_config)