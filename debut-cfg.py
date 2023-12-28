import datetime

hostname = "R1"
ip_version = 6

def creation_fichier(hostname):
    name = "config_"+ hostname + ".cfg"
    f = open(name,"w")
    return f

def recuperer_date():
    x = datetime.datetime.now()
    date = x.strftime("%H:%M:%S UTC %a %b %d %Y")
    return date

def ecriture_debut(hostname, ip_version):
    fichier_config = creation_fichier(hostname)
    fichier_config.write("!\n"*3)
    fichier_config.write("! Last configuration change at " + recuperer_date() + "\n")

    texte = "!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\n"
    fichier_config.write(texte)
    fichier_config.write("hostname "+ hostname + "\n!\n")

    texte = "boot-start-marker\nboot-end-marker\n"
    fichier_config.write(texte + "!\n"*3)

    texte = "no aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n"
    fichier_config.write(texte + "!\n"*6)

    if ip_version == 6 :
        texte = "no ip domain lookup\nipv6 unicast-routing\nipv6 cef\n"
    elif ip_version == 4 :
        texte = "JE NE SAIS PAS POUR LE MOMENT, A RECHERCHER\n"
    else :
        print("ERROR : improper IP version")
        return
    
    fichier_config.write(texte + "!\n"*2)

    texte = "multilink bundle-name authenticated\n"
    fichier_config.write(texte + "!\n"*9)

    texte = "ip tcp synwait-time 5\n"
    fichier_config.write(texte + "!\n"*12)

ecriture_debut(hostname, ip_version)