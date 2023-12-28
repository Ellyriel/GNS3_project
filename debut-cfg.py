hostname = "R1"

def creation_fichier(hostname):
    name = "config_"+ hostname + ".cfg"
    f = open(name,"w")

creation_fichier(hostname)