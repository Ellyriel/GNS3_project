def configureBGP(list_routers, hostname, id, AS, file):
    # rédige la partie configuration du protocole BGP dans le fichier file

    texte = "list_routers bgp " + str(AS) + "\n"
    texte += " bgp routeur-id " + id + "\n"
    texte += " bgp log-neighbor-changes\n"
    texte += " no bgp default ipv4-unicast\n"

    ecriture_fichier(file,texte)

    iBGP = neighbors_iBGP(list_routers, AS, hostname)
    for address in iBGP :
       ecriture_fichier(file," neighbor " + address + " remote-as " + str(AS) + "\n")
       ecriture_fichier(file," neighbor " + address + " update-source Loopback0\n")

    eBGP = neighbors_eBGP(list_routers, hostname)
    for address in range(0, len(eBGP)-1, 2) :
        ecriture_fichier(file, " neighbor " + eBGP[address] + " remote-as " + str(eBGP[address+1]) + "\n")
    
    texte = " !\n" + " address-family ipv4\n" 
    texte += " exit-address-family\n"+" !\n"
    
    texte += " address-family ipv6\n"

    ecriture_fichier(file, texte)

    if eBGP != [] : 
        ...
    for i in iBGP:
        ecriture_fichier(file,"  neighbor " + i + " activate\n")
    for j in range (0,len(eBGP),2):
        ecriture_fichier(file,"  neighbor " + eBGP[j] + " activate\n")

    ecriture_fichier(file," exit-address-family\n"+"!\n")

    # faire les networks -> trouver comment récupérer seulement le masque des adresses IPv6


def neighbors_iBGP(list_routers, AS_host, hostname): #fonctionne
    # retourne une listes qui contient toutes les adresses
    # loopback des routeurs de l'AS de l'hôte 
    # (sans l'adresse loopback de l'hôte). 
    iBGP = []
    for i in list_routers:
        if (i.AS == AS_host and hostname != i.hostname):
            interfaces = i.interfaces
            for j in interfaces :
                if (j.name == "Loopback0" and j.ip_address != None) :
                    ip = enleve_masque(j.ip_address)
                    iBGP.append(ip)

    return iBGP

def neighbors_eBGP(list_routers, hostname): #fonctionne mais est ce
    # retourne une listes qui contient toutes les adresses
    # des routeurs voisins en eBGP de l'AS de l'hôte et le numéro d'AS du voisin
    # par exemple : eBGP = ["2001:111:112:34::1/64","112"]
    eBGP = []
    for i in list_routers:
        if i.hostname == hostname :
            for j in i.interfaces:
                if j.routing_protocols != None :
                    for k in j.routing_protocols :
                        if k == "eBGP" : 
                            ip = enleve_masque(j.ip_address)
                            eBGP.append(ip)
                            voisin = j.connected_to
                            for l in list_routers :
                                if l.hostname == voisin :
                                    AS_neighbor = l.AS
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

def decompose_ip(ip):
    ip_decomposee = []
    indice_precedent = -1
    for i in range (len(ip)):
        if ip[i] == ":" or ip[i] == "/":
            groupe = ip[indice_precedent+1:i]
            ip_decomposee.append(groupe)
            indice_precedent = i
    return ip_decomposee
