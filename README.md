# GNS3_project
Projet 3TC GNS3

Membres du groupe : Louise Marc 3TC2, Anne-Gaëlle Mauger 3TC2, Nelly Nguyen 3TC2

## Configuration de base

Dans le dossier config-de-base, vous pourrez retrouver une configuration de 14 routeurs avec une architecture semblable à celle de l'énoncé du projet. 
Tous les routeurs peuvent se ping entre eux. 
eBGP, iBGP, OSPF et RIP sont implémentés. 

## Configuration avec BGP Policies et OSPF Metric

Dans le dossier config-avec-policies, vous retrouverez une configuration à 14 routeurs répartis dans 5 AS. Grâce à cette architecture, nous avons pu simuler un AS principal (AS 100) qui possède un provider (AS 500), deux AS client (AS 300 et 400) et un AS peer (AS 200). Nous y avons également appliqué des changements de métriques OSPF.

Chaque dossier contient un zip avec le fichier GNS3 correspond à la configuration décrite plus haut ainsi qu'avec les routeurs qui contienent les fichiers configs générés avec notre code.

## Description des fichiers

Dans chacun des dossiers, on retrouve les fichiers suivants : 
*  code_gns3 : Il s'agit du programme qui définit les classes Router et Interfaces, qui crée les listes de routeurs et les listes des interfaces et qui contient une fonction pour générer les fichiers de configuration (creation_fichier). Il suffit de lancer ce fichier pour générer les fichiers de configuration.

*  automatic_ip : ce fichier contient les fonctions nécéssaires pour générer une addresse ip de la forme : 2001 : nb_AS : nb_AS_2 : R1R2 :: R avec nb_AS le numéro d'AS le plus petit, nb_AS_2 le numéro d'AS de l'autre routeur, R1R2 les numéros des deux routeurs connectés avec R1 le numéro le plus petit des routeurs (généré par la fonction num_ip) et R numéro du routeur sur lequel on configure l'@ IP. 
  
*  debut_cfg et fin_cfg : les fichiers qui comporte respectivement le début du texte de configuration et la fin du texte de configuration qui contient notamment la configuration de l'interface passive pour OSPF et la "redistribute connected" pour rip. Notons que le fichier fin_cfg est différent dans le dossier config_avec_policies puisqu'il contient le texte pour configurer les routes map, les communities et les local-pref.

*  interface_function : identique dans les deux dossiers, il s'agit du fichier qui contient la fonction qui sert à déclarer toutes les interfaces physiques et l'interface Loopback avec les addreses IP ainsi que les protocoles de routages associés. (Notons que l'interface Loopback est utilisée pour le protocole iBGP pour éviter qu'il soit relier à une interface physique et qu'en cas de panne sur un lien, il puisse converger rapidement grâce au protocole unicast).

*  bgp.py : le fichier contient toutes les fonctions nécessaires à la configuration du protocole BGP. Il contient la fonciton principale configureBGP qui sera le programme appelé par code_gns3 et qui sert à écrire toute la configuration BGP. D'autres fontions sont également présentes dont le fonctionnement est précisé dans les commentaires du fichier.

*  data_policies.json / data_extent.json : fichier json qui contient les configurations que l'on souhaite donner aux routeurs.
