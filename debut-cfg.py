import json

with open('data.json', 'r', encoding='utf-8') as file:
    data_router = json.load(file)

    routeurs = data_router["router"]
    liste_routeurs = []
    
    for v in routeurs : 
        routeur_name = v["name"]
        AS_id = v["AS_id"]
        Loopback = v["Loopback"]
        neighbors = v["neighbors"]
        attributs = [routeur_name, AS_id, Loopback, neighbors]
        liste_routeurs.append(attributs)


# affiche la liste des voisins et leurs attributs du routeur 3
for i in range (len(liste_routeurs)):
    for j in range (len(liste_routeurs[i])):
        print(liste_routeurs[i][j])
    print("\n")
