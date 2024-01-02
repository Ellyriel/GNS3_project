def configureBGP(router, hostname, id, AS, neighbors, interfaces):
    # retourne un texte final du genre 
    """router bgp 123
        bgp router-id 3.3.3.3
        bgp log-neighbor-changes
        no bgp default ipv4-unicast
        neighbor 2001:100::1 remote-as 123
        neighbor 2001:100::1 update-source Loopback0
        neighbor 2001:100::2 remote-as 123
        neighbor 2001:100::2 update-source Loopback0
        neighbor 2001:100:4:3::2 remote-as 456
        !
        address-family ipv4
        exit-address-family
        !
        address-family ipv6
        network 2001:100:4:1::/64
        network 2001:100:4:2::/64
        neighbor 2001:100::1 activate
        neighbor 2001:100::2 activate
        neighbor 2001:100:4:3::2 activate
        exit-address-family
        !"""
    
    texte = "router bgp " + str(AS) + "\n"
    texte += " bgp routeur-id " + id + "\n"
    texte += " bgp log-neighbor-changes\n"
    texte += " no bgp default ipv4-unicast\n"

    iBGP = neighbors_iBGP(router, AS, hostname)
    for address in iBGP :
       texte += " neighbor " + address + " remote-as " + str(AS) + "\n"
       texte += " neighbor " + address + " update-source Loopback0\n"

    eBGP = neighbors_eBGP(router, interfaces)
    for address in range(len(eBGP)-1) :
        texte += " neighbor " + eBGP[address] + " remote-as " + eBGP[address+1] + "\n"
    
    texte += " !\n" + " address-family ipv4\n" 
    texte += " exit-address-family\n"+" !\n"
    
    texte += " address-family ipv6\n"

    if eBGP != [] : 
        ...
    for i in iBGP:
        texte += "  neighbor " + i + " activate\n"
    for j in range (0,len(eBGP),2):
        texte += "  neighbor " + eBGP[j] + " activate\n"

    
    # faire les networks -> trouver comment récupérer seulement le masque des adresses IPv6

    return texte


def neighbors_iBGP(router, AS_host, hostname):
    # retourne une listes qui contient toutes les adresses
    # loopback des routeurs de l'AS de l'hôte 
    # (sans l'adresse loopback de l'hôte). 
    iBGP = []
    for i in router:
        if (i["AS"] == str(AS_host) and hostname != i["hostname"]):
            interfaces = i["interfaces"]
            ip = enleve_masque(interfaces["ip_address"])
            iBGP.append(ip)
    return iBGP

def neighbors_eBGP(router, interfaces):
    # retourne une listes qui contient toutes les adresses
    # des routeurs voisins en eBGP de l'AS de l'hôte et le numéro d'AS du voisin
    # par exemple : eBGP = ["2001:111:112:34::1/64","112"]
    eBGP = []
    for i in interfaces:
        for j in i["routing_protocols"]:
            if i["routing_protocols"][j] == "eBGP" : 
                ip = enleve_masque(i["ip_address"])
                eBGP.append(ip)
                voisin = i["connected_to"]
                for k in router :
                    if k["hostname"] == voisin :
                        AS_neighbor = k["AS"]
                        eBGP.append(AS_neighbor)
    return eBGP

def enleve_masque (ip_masque):
    # prend en paramètre une chaîne de caractère qui correspond à une adresse IP 
    # avec un masque 
    # retourne l'adresse ip sans le masque
    indice = ip_masque.find("/")
    ip_sans_masque = ip_masque[:indice]
    return (ip_sans_masque)

def prefixe_ip (ip_masque):
    # prend une adresse ip avec son masque
    # retourne seulement le préfixe avec /masque
    indice = ip_masque.find("/")
    masque = ip_masque[(indice+1):]
    if masque == "64" :
        ip = ...


