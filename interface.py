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
def configureinterface(router):
    text = ""
    for interface in router.interfaces:
        text += "interface " + interface.name + "\n"
        text += " no ip address \n"
        if interface.ip_address == None:
            text += " shutdown \n"
        if interface.name == "FastEthernet0/0":
                text += " duplex full \n"
        elif interface.name != "Loopback0":
            text += " negociation auto \n"
        if interface.ip_address != None :
            ip_ad = str(interface.ip_address)
            text += " ipv6 address " + ip_ad + "\n"
            text += " ipv6 enable\n"
            if interface.routing_protocols[0] == 'RIP' :
                text += " ipv6 rip ripng enable \n"
            #else:
                # soucis ospf : process_id + area number à configurer
        text += "!\n"

    return text