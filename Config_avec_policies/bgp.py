def configureBGP(list_routers, interfaces, hostname, id, AS, liste_rm, file):
    # rédige la partie configuration du protocole BGP dans le fichier file

    texte = "router bgp " + str(AS) + "\n"
    texte += " bgp router-id " + id + "\n"
    texte += " bgp log-neighbor-changes\n"
    texte += " no bgp default ipv4-unicast\n"

    ecriture_fichier(file,texte)

    iBGP, routes_AS = neighbors_iBGP(list_routers, AS, hostname)
    for address in iBGP :
       ecriture_fichier(file," neighbor " + address + " remote-as " + str(AS) + "\n")
       ecriture_fichier(file," neighbor " + address + " update-source Loopback0\n")

    eBGP = []
    for interface in interfaces :
        if interface.routing_protocols != None and "eBGP" in interface.routing_protocols and eBGP == []:
            eBGP = neighbors_eBGP(list_routers, hostname)
            for address in range(0, len(eBGP)-1, 2) :
                ecriture_fichier(file, " neighbor " + eBGP[address] + " remote-as " + str(eBGP[address+1]) + "\n")

    texte = " !\n" + " address-family ipv4\n" 
    texte += " exit-address-family\n"+" !\n"
    texte += " address-family ipv6\n"

    ecriture_fichier(file, texte)

    if eBGP != [] :
        prefixes = networks(routes_AS)
        for u in prefixes : 
            ecriture_fichier(file,"  network " + u + " route-map client-in\n")
    for i in iBGP:
        ecriture_fichier(file,"  neighbor " + i + " activate\n")
        ecriture_fichier(file,"  neighbor " + i + " send-community \n")
        ecriture_fichier(file,"  neighbor " + i + " route-map " + liste_rm[3] + " in\n")
        ecriture_fichier(file,"  neighbor " + i + " route-map " + liste_rm[7] + " out\n")
    for j in range (0,len(eBGP),2):
        ecriture_fichier(file,"  neighbor " + eBGP[j] + " activate\n")

    for interface in interfaces :
        if interface.routing_protocols != None and "eBGP" in interface.routing_protocols:
            if interface.relation == "Client" :
                ecriture_fichier(file, "  neighbor " + eBGP[j] + " send-community" +"\n")
                ecriture_fichier(file, "  neighbor " + eBGP[j] + " " + liste_rm[0] +" in\n")
                ecriture_fichier(file, "  neighbor " + eBGP[j] + " " + liste_rm[4] +" out\n")
            elif interface.relation == "Peer" :
                ecriture_fichier(file, "  neighbor " + eBGP[j] + " send-community" +"\n")
                ecriture_fichier(file, "  neighbor " + eBGP[j] + " " + liste_rm[1] +" in\n")
                ecriture_fichier(file, "  neighbor " + eBGP[j] + " " + liste_rm[5] +" out\n")
            elif interface.relation == "Provider" :
                ecriture_fichier(file, "  neighbor " + eBGP[j] + " send-community" +"\n")
                ecriture_fichier(file, "  neighbor " + eBGP[j] + " " + liste_rm[2] +" in\n")
                ecriture_fichier(file, "  neighbor " + eBGP[j] + " " + liste_rm[6] +" out\n")
    

            

    ecriture_fichier(file," exit-address-family\n"+"!\n")


def neighbors_iBGP(list_routers, AS_host, hostname): #fonctionne
    '''
    retourne une listes qui contient toutes les adresses loopback des routeurs de l'AS de l'hôte dans la liste iBGP (sans l'adresse loopback de l'hôte). 
    retourne dans routes_AS les ad ip des routes de l'AS qui ne sont pas en Loopback
    '''
    iBGP = []
    routes_AS = []
    for i in list_routers:
        if (i.AS == AS_host and hostname != i.hostname):
            interfaces = i.interfaces
            for j in interfaces :
                if (j.name == "Loopback0" and j.ip_address != None) :
                    ip = enleve_masque(j.ip_address)
                    iBGP.append(ip)
                elif (j.name != "Loopback0" and j.ip_address != None and "eBGP" not in j.routing_protocols) : 
                    routes_AS.append(j.ip_address)
    return iBGP, routes_AS

def neighbors_eBGP(list_routers, hostname): #fonctionne
    '''
    retourne une listes qui contient toutes les adresses des routeurs voisins en eBGP de l'AS de l'hôte et le numéro d'AS du voisin
    par exemple : eBGP = ["2001:111:112:34::1/64","112"]
    '''
    eBGP = []
    for i in list_routers:
        if i.hostname != hostname and hostname in i.neighbors:
            for j in i.interfaces:
                if j.routing_protocols != None and "eBGP" in j.routing_protocols and j.connected_to == hostname :
                    ip = enleve_masque(j.ip_address)
                    eBGP.append(ip)
                    eBGP.append(i.AS)
    return eBGP

def ecriture_fichier(file,text):
    file.write(text)

def enleve_masque (ip_masque): #fonctionne
    '''
    prend en paramètre une chaîne de caractère qui correspond à une adresse IP avec un masque 
    retourne l'adresse ip sans le masque
    '''
    indice = ip_masque.find("/")
    ip_sans_masque = ip_masque[:indice]
    return (ip_sans_masque)

def prefixe_ip (ip_masque):
    '''
    prend une adresse ip avec son masque
    retourne seulement le préfixe avec /masque
    '''
    liste_ip = decompose_ip(ip_masque)
    masque = liste_ip[8]
    prefixe = ""
    if masque == "/64" :
        for i in range(0,4,1):
            prefixe += liste_ip[i] + ":"
        prefixe += ":" + masque
    if masque == "/128" :
        prefixe = ip_masque
    return prefixe

def decompose_ip(ip):
    '''
    retourne une liste dont les éléments sont les partis séparées de l'adresse ip avec masque en argument
    '''
    ip_decomposee = []
    indice_precedent = -1
    # récupère les 8 nombres hexadécimaux de l'adresse dans une liste
    for i in range (len(ip)):
        if ip[i] == ":" or ip[i] == "/":
            groupe = ip[indice_precedent+1:i]
            ip_decomposee.append(groupe)
            indice_precedent = i
    # récupère le masque et le met en position 8 dans la liste ip_decomposee
    indice = ip.find("/")
    masque = ip[indice:]
    ip_decomposee.append(masque)
    return ip_decomposee

def networks (routes_AS):
    """
    récupère les adresses ip (pas loopback) de l'AS
    retourne une liste des préfixes de ces adresses sans doublons
    """
    prefixes = []
    for k in routes_AS : 
        prefixe = prefixe_ip(k)
        new = True
        for i in prefixes :
            if i == prefixe : 
                new = False
        if new == True :
            prefixes.append(prefixe)
    return prefixes

