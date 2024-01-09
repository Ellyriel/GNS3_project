
def creation_texte_fin(hostname, id, as_rp, ip_version, file):
    '''
    fonction qui crée le texte de la fin du fichier de configuration
    paramètres : hostname du routeur, id du routeur, as_rp du routeur, version de IP
    renvoi : texte
    '''
    ecriture_fichier(file, "ip forward-protocol nd\n" + "!\n"*2)
    ecriture_fichier(file, "no ip http server\nno ip http secure-server\n!\n")

    if ip_version == 6 :
        if as_rp == "RIP" :
            ecriture_fichier(file, "ipv6 router rip ripng\n redistribute connected\n")
        if as_rp == "OSPF" :
            ecriture_fichier(file, "ipv6 router ospf " + hostname[1:] + "\n router-id " + id + "\n")
    elif ip_version == 4 :
        ecriture_fichier(file, "JE NE SAIS PAS IL FAUT QUE JE CHERCHE\n")
    else :
        print("ERROR : improper IP version")
        return
    
    ecriture_fichier(file, "!\n"*4 + "control-plane\n" + "!\n"*2)

    ecriture_fichier(file, "line con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")
    ecriture_fichier(file, "line aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n")

    ecriture_fichier(file, "line vty 0 4\n login\n" + "!\n"*2)
    ecriture_fichier(file, "end\n")

    return

def ecriture_fichier(file,text):
    file.write(text)

