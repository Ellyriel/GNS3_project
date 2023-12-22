import json

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


# affiche la liste des voisins et leurs attributs du routeur 3
print(liste_routeurs[2][3])