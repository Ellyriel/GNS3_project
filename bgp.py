def configureBGP(router, hostname, id, AS, file):
    # retourne un texte final du genre :
    """router bgp 123
        bgp router-id 3.3.3.3
        bgp log-neighbor-changes
        no bgp default ipv4-unicast
        neighbor 2001:100::1 remote-as 123
        neighbor 2001:100::1 update-source Loopback0
        neighbor 2001:100::2 remote-as 123
        neighbor 2001:100::2 update-source Loopback0
        neighbor 2001:100:4:3::2 remote-as 456 #ici il n'y a bien que les routeurs eBGP reliés directement qui sont affichés?
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

    eBGP = neighbors_eBGP(router, hostname)
    for address in range(0, len(eBGP)-1, 2) :
        texte += " neighbor " + eBGP[address] + " remote-as " + eBGP[address+1] + "\n"
    
    texte += " !\n" + " address-family ipv4\n" 
    texte += " exit-address-family\n"+" !\n"
    
    texte += " address-family ipv6\n"


# jusque là ça marche

    if eBGP != [] : 
        ...
    for i in iBGP:
        texte += "  neighbor " + i + " activate\n"
    for j in range (0,len(eBGP),2):
        texte += "  neighbor " + eBGP[j] + " activate\n"

    ecriture_fichier(file, texte)



    # faire les networks -> trouver comment récupérer seulement le masque des adresses IPv6

    


def neighbors_iBGP(router, AS_host, hostname): #fonctionne
    # retourne une listes qui contient toutes les adresses
    # loopback des routeurs de l'AS de l'hôte 
    # (sans l'adresse loopback de l'hôte). 
    iBGP = []
    for i in router:
        if (i["AS"] == str(AS_host) and hostname != i["hostname"]):
            interfaces = i["interfaces"]
            for j in interfaces :
                if (j["name"]== "Loopback0" and j["ip_address"] != None) :
                    ip = enleve_masque(j["ip_address"])
                    iBGP.append(ip)

    return iBGP

def neighbors_eBGP(router, hostname): #fonctionne mais est ce
    # retourne une listes qui contient toutes les adresses
    # des routeurs voisins en eBGP de l'AS de l'hôte et le numéro d'AS du voisin
    # par exemple : eBGP = ["2001:111:112:34::1/64","112"]
    eBGP = []
    for i in router:
        if i["hostname"] == hostname :
            for j in i["interfaces"]:
                if j["routing_protocols"] != None :
                    for k in j["routing_protocols"] :
                        if k == "eBGP" : 
                            ip = enleve_masque(j["ip_address"])
                            eBGP.append(ip)
                            voisin = j["connected_to"]
                            for l in router :
                                if l["hostname"] == voisin :
                                    AS_neighbor = l["AS"]
                                    eBGP.append(AS_neighbor)
    return eBGP

def enleve_masque (ip_masque): #fonctionne
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

def ecriture_fichier(file,text):
    file.write(text)

