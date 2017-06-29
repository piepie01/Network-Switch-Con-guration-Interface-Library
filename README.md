# Network-Switch-Con-guration-Interface-Library

## Quick View
$./switch_start 172.16.215.6
Cisco[c] or Hp[h]?c
Username:admin
Try ssh to  172.16.215.6
Success!
password :
127isgod>
Type exit/forceexit to quit, help for help.
127isgod>


127isgod>showintstat

Port      Name               Status       Vlan       Duplex  Speed Type                Trunk
Gi0/1                        connected    1          a-full a-1000 10/100/1000BaseTX
Gi0/2                        notconnect   1            auto   auto 10/100/1000BaseTX
Gi0/3                        notconnect   1            auto   auto 10/100/1000BaseTX
Gi0/4                        notconnect   1            auto   auto 10/100/1000BaseTX
Gi0/5                        notconnect   1            auto   auto 10/100/1000BaseTX


127isgod>showarp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  172.16.0.1              0   0012.80be.b343  ARPA   Vlan1
Internet  172.16.215.6            -   0018.b94b.6cc0  ARPA   Vlan1

## Install
You may need to install "pexpect (4.2.1)."


