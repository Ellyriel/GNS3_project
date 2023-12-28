import json

with open("data.json") as file:
    data = json.load(file)

ip_version = int(data["ip_version"])


# classe définissant un routeur
class Router :

    def __init__ (self, hostname, id, AS, AS_RP, neighbors, interfaces) :
        self.hostname = hostname
        self.id = id
        self.AS = AS
        self.AS_RP = AS_RP
        self.neighbors = neighbors
        self.interfaces = interfaces
        
    def __str__(self):
        return f'[{self.hostname} : AS n°{self.AS} with {self.AS_RP} routing protocol, Router ID {self.id}, {len(self.neighbors)} neighbor(s), {len(self.interfaces)} interface(s)]'
    
    def __repr__(self):
        return f'Router {self.hostname}'


# classe définissant une interface d'un routeur
class Interface :

    def __init__ (self, name, ip_address, routing_protocols, connected_to) :
        self.name = name
        self.ip_address = ip_address
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
    AS = int(router["AS"])
    AS_RP = router["AS_RP"]
    id = router["id"]
    neighbors = router["neighbors"]

    list_interfaces = []
    for interface in router["interfaces"]:
        name = interface["name"]
        ip_address = interface["ip_address"]
        routing_protocols = interface["routing_protocols"]
        connected_to = interface["connected_to"]
        list_interfaces.append(Interface(name, ip_address, routing_protocols, connected_to))

    list_routers.append(Router(hostname,id,AS,AS_RP,neighbors,list_interfaces))


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