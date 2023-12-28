import datetime

hostname = "R1"

def creation_fichier(hostname):
    name = "config_"+ hostname + ".cfg"
    f = open(name,"w")

def recuperer_date():
    x = datetime.datetime.now()
    date = x.strftime("%H:%M:%S UTC %a %b %d %Y")
    return date