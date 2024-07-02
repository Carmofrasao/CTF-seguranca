# Espufando Alice

Basicamente o que deve ser feito nesse desafio e o seguinte:

1) Considerando o desafio 'Mensagem cifrada', la e dito que a porta 8349 ficara aberta no pc da Alice, e la ela vai usar para baixar uma calculadora.

Usando o netcat temos a seguinte mensagem:

´nc alice\_pc 8349´:

    starting download in 5 seconds...
    --2024-07-02 20:06:43--  http://ftp.br.debian.org/debian/pool/main/g/gnome-calculator/gnome-calculator\_43.0.1-2\_amd64.deb
    Resolving ftp.br.debian.org (ftp.br.debian.org)... 200.236.31.3, 2801:82:80ff:8000::4
    Connecting to ftp.br.debian.org (ftp.br.debian.org)|200.236.31.3|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 993488 (970K) [application/vnd.debian.binary-package]
    Saving to: 'gnome-calculator_43.0.1-2_amd64.deb'

         0K .......... .......... .......... .......... ..........  5% 4.24M 0s
        50K .......... .......... .......... .......... .......... 10% 83.0M 0s
       100K .......... .......... .......... .......... .......... 15% 8.64M 0s
       150K .......... .......... .......... .......... .......... 20% 9.92M 0s
       200K .......... .......... .......... .......... .......... 25% 79.6M 0s
       250K .......... .......... .......... .......... .......... 30% 80.1M 0s
       300K .......... .......... .......... .......... .......... 36% 84.4M 0s
       350K .......... .......... .......... .......... .......... 41% 22.7M 0s
       400K .......... .......... .......... .......... .......... 46% 14.2M 0s
       450K .......... .......... .......... .......... .......... 51% 38.0M 0s
       500K .......... .......... .......... .......... .......... 56% 27.8M 0s
       550K .......... .......... .......... .......... .......... 61% 26.7M 0s
       600K .......... .......... .......... .......... .......... 66% 28.8M 0s
       650K .......... .......... .......... .......... .......... 72% 28.6M 0s
       700K .......... .......... .......... .......... .......... 77% 28.1M 0s
       750K .......... .......... .......... .......... .......... 82% 33.4M 0s
       800K .......... .......... .......... .......... .......... 87% 25.5M 0s
       850K .......... .......... .......... .......... .......... 92% 47.1M 0s
       900K .......... .......... .......... .......... .......... 97% 53.8M 0s
       950K .......... ..........                                 100% 36.9M=0.05s

    2024-07-02 20:06:43 (20.6 MB/s) - 'gnome-calculator_43.0.1-2_amd64.deb' saved [993488/993488]

    starting installation
    (Reading database ... 22501 files and directories currently installed.)
    Preparing to unpack gnome-calculator_43.0.1-2_amd64.deb ...
    Unpacking gnome-calculator (1:43.0.1-2) over (1:43.0.1-2) ...
    dpkg: dependency problems prevent configuration of gnome-calculator:
     gnome-calculator depends on libadwaita-1-0 (>= 1.2~alpha); however:
      Package libadwaita-1-0 is not installed.
     gnome-calculator depends on libc6 (>= 2.34); however:
      Version of libc6:amd64 on system is 2.31-13+deb11u8.
     gnome-calculator depends on libgee-0.8-2 (>= 0.8.3); however:
      Package libgee-0.8-2 is not installed.
     gnome-calculator depends on libglib2.0-0 (>= 2.63.3); however:
      Package libglib2.0-0 is not installed.
     gnome-calculator depends on libgtk-4-1 (>= 4.4.1); however:
      Package libgtk-4-1 is not installed.
     gnome-calculator depends on libgtksourceview-5-0 (>= 5.3.0); however:
      Package libgtksourceview-5-0 is not installed.
     gnome-calculator depends on libsoup-3.0-0 (>= 2.41.90); however:
      Package libsoup-3.0-0 is not installed.
     gnome-calculator depends on libxml2 (>= 2.7.4); however:
      Package libxml2 is not installed.
     gnome-calculator depends on dconf-gsettings-backend | gsettings-backend; however:
      Package dconf-gsettings-backend is not installed.
      Package gsettings-backend is not installed.

    dpkg: error processing package gnome-calculator (--install):
     dependency problems - leaving unconfigured
    Processing triggers for libc-bin (2.31-13+deb11u8) ...
    Processing triggers for mailcap (3.69) ...
    Errors were encountered while processing:
     gnome-calculator
    starting gnome-calculator
    gnome-calculator: error while loading shared libraries: libglib-2.0.so.0: cannot open shared object file: No such file or directory

Ou seja, ela baixa um ´.deb´, que é executado em modo sudo, assim, podemos pensar na possibilidade de sobrescrever esse arquivo com o nosso proprio arquivo!

2) Dado essas informações, temos que pensar como fazer, precisaremos nos passar pela fonte original dos dados, ou seja, ´http://ftp.br.debian.org/debian/pool/main/g/gnome-calculator/gnome-calculator\_43.0.1-2\_amd64.deb´.

Para isso, vamos usar o script ´ARPspoof.py´, ele basicamente fica enviando para a Alice que eu sou o roteador, com isso, quando ela fazer a requisição da calculadora, eu vou receber esse pedido.

3) Agora eu tenho que manipular esse pedido, para isso vamos utilizar o ´IPspoof.py´, ele trata as requisições HTTP (o nome não é muito intuitivo), ele recebe e responde as requisições como se fosse ´ftp.br.debian.org´.

4) agora que temos as requisições, precisamos mandar a noissa calculadora, para isso precisamos de um .deb com nosso codigo malicioso.

Para isso precisamos saber o formato de um .deb, mas isso voce pode pesquisar por conta, eu ja deixei um disponivel aqui. Em ´pacote/usr/bin/gnome-calculator´ esta o codigo python;

Para gerar o .deb, deve rodar os seguintes comandos:

´dpkg-deb --build -Z=xz pacote/´

Mude o nome do arquivo:

´mv pacote.deb gnome-calculator_43.0.1-2_amd64.deb´

Coloque no lugar certo:

´mv gnome-calculator_43.0.1-2_amd64.deb debian/pool/main/g/gnome-calculator/´

5) Agora que temos o .deb, precisamos servir esse arquivo, para isso vamos usar o ´serverHTTP.py´, ele basicamente envia o .deb.

6) Para fazer tudo funcionar, rode o ´serverHTTP.py´, depois rode o ´ARPspoof.py´, depois o ´IPspoof.py´, e por ultimo, rode ´nc alice\_pc 8349´ (em terminais diferentes).
