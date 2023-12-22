import json

def configureBGP(name, AS_id, neighbors):
    # retourne un texte final du genre
    """router bgp 111
        bgp router-id 1.1.1.1
        bgp log-neighbor-changes
        no bgp default ipv4-unicast
        neighbor 2001:0:0:2::1 remote-as 111
        neighbor 2001:0:0:2::1 update-source Loopback1
        neighbor 2001:0:0:3::1 remote-as 111
        neighbor 2001:0:0:3::1 update-source Loopback1
        !
        address-family ipv4
        exit-address-family
        !
        address-family ipv6
        neighbor 2001:0:0:2::1 activate
        neighbor 2001:0:0:3::1 activate
        exit-address-family"""
    texte = ""
    n_iBGP, n_eBGP = neighbors_iBGP_ou_eBGP(liste_routeurs[0][3])
    return texte


def neighbors_iBGP_ou_eBGP(neighbors):
    # retourne deux listes, une avec les voisins eBGP 
    # et une avec les voisins iBGP
    for i in range (len(neighbors)):
        print (neighbors[i])
    iBGP = []
    eBGP = []
    return iBGP, eBGP



# code qui sera dans le fichier principal seulement mais
# qu'on garde pour faire les tests.
fichier_data = "GNS3\GNS3_project\data.json"
with open(fichier_data) as mon_fichier:
    data = json.load(mon_fichier)

    routeurs = data["router"]
    liste_routeurs = []
    i = 0
    for v in routeurs : 
        routeur_name = v["name"]
        AS_id = v["AS_id"]
        Loopback = v["Loopback"]
        neighbors = v["neighbors"]
        attributs = [routeur_name, AS_id, Loopback, neighbors]
        liste_routeurs.append(attributs)


ha, ho = neighbors_iBGP_ou_eBGP(liste_routeurs[0][3])
ha, ho = neighbors_iBGP_ou_eBGP(liste_routeurs[1][3])
# affiche la liste des voisins et leurs attributs du routeur 3
#print(liste_routeurs[2][3])
        