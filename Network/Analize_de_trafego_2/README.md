# Análise de tráfego 2

Utilizando o pcap da `Análise de tráfego 1`, qual usuário foi comprometido? Se a senha foi descoberta, você consegue ver qual foi?

Flag no formato: SECRET{user:pass}

## Ferramentas

* Wireshark

## Passos

1. Ainda utilizando a busca no wirechark, busque por login successful

2. Pode haver dois resultados, olhe o que contem `USER` e `PASS` logo antes dele

## Resposta

`SECRET{jenny:password123}`
