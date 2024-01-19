import json
import bgp
import interface_function
import debut_cfg
import fin_cfg
import automatic_ip

with open("data_policies.json") as file:
    data = json.load(file)
    
ip_version = int(data["ip_version"])


# classe définissant un routeur
class Router :

    def __init__ (self, hostname, id, AS, AS_RP, area, neighbors, interfaces) :
        self.hostname = hostname
        self.id = id
        self.AS = AS
        self.AS_RP = AS_RP
        self.area = area
        self.neighbors = neighbors
        self.interfaces = interfaces
        
    def __str__(self):
        return f'[{self.hostname} : AS n°{self.AS} with {self.AS_RP} routing protocol, Router ID {self.id}, {len(self.neighbors)} neighbor(s), {len(self.interfaces)} interface(s)]'
    
    def __repr__(self):
        return f'Router {self.hostname}'


# classe définissant une interface d'un routeur
class Interface :

    def __init__ (self, name, ip_address, routing_protocols, metric,  connected_to, relation) :
        self.name = name
        self.ip_address = ip_address
        self.routing_protocols = routing_protocols
        self.metric = metric
        self.connected_to = connected_to
        self.relation = relation

    def __str__(self):
        return f'[Interface {self.name} : IP Address {self.ip_address}, Routing Protocols {self.routing_protocols}, Metric : {self.metric}, Connected to {self.connected_to} ({self.relation})]'
    
    def __repr__(self):
        return f'Interface {self.name}'


# mise en forme des données de chacun des routeurs
list_routers = []
for router in data["router"]:
    hostname = router["hostname"]
    AS = router["AS"]
    AS_RP = router["AS_RP"]
    area = router["area"]
    id = router["id"]
    neighbors = router["neighbors"]

    list_interfaces = []
    for interface in router["interfaces"]:
        name = interface["name"]
        ip_address = None
        routing_protocols = interface["routing_protocols"]
        metric = interface["metric"]
        connected_to = interface["connected_to"]
        relation = interface["relation"]
        list_interfaces.append(Interface(name, ip_address, routing_protocols, metric, connected_to, relation))

    list_routers.append(Router(hostname, id, AS, AS_RP, area, neighbors, list_interfaces))


# création des adresses ipv6 pour chaque interface des routeurs
for router in list_routers:
    for interface in router.interfaces:
        if interface.name == "Loopback0":
            interface.ip_address = automatic_ip.generer_ip_loopback(router)
        if interface.connected_to != None and interface.name != "Loopback0":
            a = 0
            router2 = list_routers[a]
            while router2.hostname != interface.connected_to and a < len(list_routers):
                a += 1
                router2 = list_routers[a]
            interface.ip_address = automatic_ip.generer_ip(router,router2)


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
    name = "i"+ hostname[1:] + "_startup-config.cfg"
    f = open(name,"w")
    return f

for router in list_routers:
    fichier_config = creation_fichier(router.hostname)
    debut_cfg.creation_texte_debut(router.hostname, ip_version, fichier_config)
    interface_function.configureinterface(router, fichier_config)
    bgp.configureBGP(list_routers,router.interfaces, router.hostname, router.id, router.AS, fichier_config)
    fin_cfg.creation_texte_fin(router.hostname, router.id, router.AS_RP, router.interfaces, ip_version, fichier_config)

