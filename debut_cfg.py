import datetime

def recuperer_date_heure():
    '''
    fonction qui récupère la date et l'heure actuelle à laquelle elle est exécutée
    paramètres : none
    renvoi : date et heure sous forme d'une chaîne de caractères
    '''
    x = datetime.datetime.now()
    date_heure = x.strftime("%H:%M:%S UTC %a %b %d %Y")
    return date_heure

def creation_texte_debut(hostname, ip_version, file):
    '''
    fonction qui crée un texte. Dans notre cas, ce texte sera réécrit plus tard dans le fichier de configuration, et il correspond au début du fichier de configuration
    paramètres : hostname du routeur, version de IP utilisée pour notre réseau
    renvoi : texte
    '''

    texte = ""

    texte += "!\n"*3
    texte += "! Last configuration change at " + recuperer_date_heure() + "\n"

    ecriture_fichier(file, texte)

    texte = "!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\n"
    texte += "hostname "+ hostname + "\n!\n"

    ecriture_fichier(file, texte)

    texte = "boot-start-marker\nboot-end-marker\n" + "!\n"*3

    texte += "no aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n" + "!\n"*6

    ecriture_fichier(file, texte)

    if ip_version == 6 :
        texte = "no ip domain lookup\nipv6 unicast-routing\nipv6 cef\n"
    elif ip_version == 4 :
        texte = "JE NE SAIS PAS POUR LE MOMENT, A RECHERCHER\n"
    else :
        print("ERROR : improper IP version")
        return
    
    texte += "!\n"*2

    ecriture_fichier(file, texte)

    texte = "multilink bundle-name authenticated\n" + "!\n"*9
    texte += "ip tcp synwait-time 5\n" + "!\n"*12

    ecriture_fichier(file, texte)
    
    return

def ecriture_fichier(file,text):
    file.write(text)

# A DEPLACER DANS LE FICHIER PRINCIPAL PLUS TARD
'''
import debut_cfg

def creation_fichier(hostname):
    name = "config_"+ hostname + ".cfg"
    f = open(name,"w")
    return f

for router in list_routers:
    fichier_config = creation_fichier(router.hostname)
    debut_cfg.creation_texte_debut(router.hostname, ip_version, fichier_config)
'''