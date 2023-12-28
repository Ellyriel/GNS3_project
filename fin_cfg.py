
def creation_texte_fin(hostname, id, as_rp, ip_version):
    '''
    fonction qui crée le texte de la fin du fichier de configuration
    paramètres : hostname du routeur, id du routeur, as_rp du routeur, version de IP
    renvoi : texte
    '''

    texte = ""
    texte += "ip forward-protocol nd\n" + "!\n"*2
    texte += "no ip http server\nno ip http secure-server\n!\n"

    if ip_version == 6 :
        if as_rp == "RIP" :
            texte += "ipv6 router rip ripng\n redistribute connected\n"
        if as_rp == "OSPF" :
            texte += "ipv6 router ospf " + hostname[1:] + "\n router-id " + id + "\n"
    elif ip_version == 4 :
        texte += "JE NE SAIS PAS IL FAUT QUE JE CHERCHE\n"
    else :
        print("ERROR : improper IP version")
        return
    
    texte += "!\n"*4 + "control-plane\n" + "!\n"*2

    texte += "line con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n"
    texte += "line aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\n"

    texte += "line vty 0 4\n login\n" + "!\n"*2
    texte += "end\n"

    return texte







# A DEPLACER DANS LE FICHIER PRINCIPAL PLUS TARD
'''
import fin_cfg

def creation_fichier(hostname):
    name = "config_"+ hostname + ".cfg"
    f = open(name,"w")
    return f

def ecriture_fichier(file,text):
    file.write(text)

for router in list_routers:

    #fonctions intermédiaires

    texte_config = fin_cfg.creation_texte_fin(router.hostname, router.id, router.AS_RP, ip_version)
    ecriture_fichier(fichier_config, texte_config)
'''
