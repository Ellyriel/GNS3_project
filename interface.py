"""
Le code doit renvoyer le texte suivant

interface Loopback0
 no ip address
 ipv6 address 2001:100::1/128
 ipv6 enable
!
interface FastEthernet0/0
 no ip address
 shutdown
 duplex full
!
interface GigabitEthernet1/0
 no ip address
 negotiation auto
 ipv6 address 2001:100:4:1::1/64
 ipv6 enable
 ipv6 rip ripng enable
!
interface GigabitEthernet2/0
 no ip address
 shutdown
 negotiation auto
!
"""

def ecriture_fichier(file,text):
    file.write(text)

def configureinterface(router, file):
    for interface in router.interfaces:
        ecriture_fichier(file, "interface " + interface.name + "\n")
        ecriture_fichier(file," no ip address \n")
        if interface.ip_address == None:
            ecriture_fichier(file," shutdown \n")
        if interface.name == "FastEthernet0/0":
                ecriture_fichier(file," duplex full \n")
        elif interface.name != "Loopback0":
            ecriture_fichier(file," negociation auto \n")
        if interface.ip_address != None :
            ip_ad = str(interface.ip_address)
            ecriture_fichier(file, " ipv6 address " + ip_ad + "\n")
            ecriture_fichier(file," ipv6 enable\n")
            if interface.routing_protocols[0] == 'RIP' :
                ecriture_fichier(file,"ipv6 rip ripng enable \n")
            #else:
                # soucis ospf : process_id + area number à configurer
        ecriture_fichier(file,"!\n")