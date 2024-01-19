
def creation_texte_fin(hostname, id, as_rp, list_interfaces, ip_version, file):
    '''
    fonction qui crée le texte de la fin du fichier de configuration
    paramètres : hostname du routeur, id du routeur, as_rp du routeur, version de IP
    renvoi : texte
    '''
    ecriture_fichier(file, "ip forward-protocol nd\n" + "!\n")

    names = ["50","100","200"] # 50 pour client vers provider ; 100 pour peer vers peer ; 200 pour provider vers client
    values = ["10","20","30"] # 10 pour les routes client ; 20 pour les routes provider ; 30 pour les routes peer

    for name in names :
        for value in values :
            if int(name) > 50 and int(value) > 10 :
                ecriture_fichier(file, "ip community-list " + name + " deny " + value + "\n")
            else :
                ecriture_fichier(file, "ip community-list " + name + " permit " + value + "\n")

    ecriture_fichier(file, "!\nno ip http server\nno ip http secure-server\n!\n")

    if ip_version == 6 :
        if as_rp == "RIP" :
            ecriture_fichier(file, "ipv6 router rip ripng\n redistribute connected\n")
        if as_rp == "OSPF" :
            ecriture_fichier(file, "ipv6 router ospf " + hostname[1:] + "\n router-id " + id + "\n")
            for interface in list_interfaces :
                if interface.routing_protocols != None and "eBGP" in interface.routing_protocols :
                    ecriture_fichier(file, " passive-interface " + interface.name + "\n")
    elif ip_version == 4 :
        ecriture_fichier(file, "JE NE SAIS PAS IL FAUT QUE JE CHERCHE\n")
    else :
        print("ERROR : improper IP version")
        return
    
    ecriture_fichier(file, "!\n"*2)

    names = ["peer-in", "provider-in", "client-in", "peer-out", "provider-out", "client-out"]

    for name in names :
        ecriture_fichier(file, "route-map " + name + " permit 100\n")
        if "in" in name :
            if "peer" in name :
                ecriture_fichier(file, " set local-preference 100\n")
                ecriture_fichier(file, " set community 30\n")
            elif "provider" in name :
                ecriture_fichier(file, " set local-preference 50\n")
                ecriture_fichier(file, " set community 20\n")
            elif "client" in name :
                ecriture_fichier(file, " set local-preference 200\n")
                ecriture_fichier(file, " set community 10\n")
        elif "out" in name :
            if "peer" in name :
                ecriture_fichier(file, " match community 100\n")
            elif "provider" in name :
                ecriture_fichier(file, " match community 50\n")
            elif "client" in name :
                ecriture_fichier(file, " match community 200\n")
        ecriture_fichier(file,"!\n")

    ecriture_fichier(file, "!\n"*3 + "control-plane\n" + "!\n"*2)

    ecriture_fichier(file, "line con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")
    ecriture_fichier(file, "line aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")

    ecriture_fichier(file, "line vty 0 4\n login\n" + "!\n"*2)
    ecriture_fichier(file, "end\n")

    return

def ecriture_fichier(file,text):
    file.write(text)