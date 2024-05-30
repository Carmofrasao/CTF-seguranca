# Análise de tráfego 1

Conseguimos recuperar o tráfego de rede que ocorreu (achamos) durante o ataque. O Sérgio comentou que tem indícios de login em um serviço específico. Você consegue ver qual?

Flag no formato: SECRET{serviço}

## Ferramentas

* Wireshark

## Passos

1. Abra o Wireshark (ja com o arquivo que contem o ataque como input) 

        wireshark attack.pcapng

2. Usando a ferramenta de busca do wireshark, configure para buscar por string

3. Busque por "login"

## Resposta

`SECRET{FTP}`
