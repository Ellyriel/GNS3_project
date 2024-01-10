def num_ip(router1, router2):
    num_router1 = int(router1.hostname[1:])
    num_router2 = int(router2.hostname[1:])
    if num_router1 < num_router2:
        numero = num_router1*10 + num_router2
    else :
        numero = num_router2*10 + num_router1
    return str(numero)
    
#création de la fonction qui automatise les @ ipv6 selon si c'est une loopback ou une interface "normale"
def generer_ip_network(router1,router2):
    numero = num_ip(router1, router2)
    address_ip = "2001:100:" + router1.AS + ":" + numero + ":0:0:0:" + router1.hostname[1:] + "/64"
    network = "2001:100:" + router1.AS + ":" + numero + ":0:0:0:0" + "/64"
    return address_ip, network

def generer_ip_network_loopback(router):
    address_ip = "2001:100:0:0:0:0:0:"+ router.hostname[1:] + "/128"
    network = "2001:100:0:0:0:0:0:0/128"
    return address_ip, network
