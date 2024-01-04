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