# 1ª Etapa: Instalações

## 1. Instalação do Docker

**1.1.** Antes de começar, atualize o sistema:
```
sudo apt update
```
```
sudo apt upgrade
```

**1.2.** Instale os pacotes de pré-requisitos:
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

**1.3.** Adicione chaves GPG de acesso:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

**1.4.** Adicione o repositório do Docker às fotos do APT:
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```

**1.5.** Atualize o sistema novamente:
```
sudo apt update
```

**1.6.** Garanta que você está instalando a partir do repositório do Docker, ao invés do repositório padrão do Ubuntu ao usar este comando:
```
apt-cache policy docker-ce
```

**1.7.** Instale o Docker
```
sudo apt install docker-ce
```

**1.8.** Verifique se o Docker está funcionando:
```
sudo systemctl status docker
```

## 2. Instalação do Portainer

**2.1.** Digite o comando para criar um volume para o Portainer
```
sudo docker volume create portainer_data
```

**2.2.** Digite o comando abaixo para instalar o Portainer dentro do volume criado:
```
sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

**2.3.** Acesse o endereço no navegador para abrir o Portainer
```
https://localhost:9443
```

**Crie a senha ```123456789012``` como padrão.**


## 3. Instalação do Python

**3.1.** Adicione o repositório
```
sudo add-apt-repository ppa:deadsnakes/ppa
```

**3.2.** Atualize
```
sudo apt update
```

**3.3.** Instale o Python

```
sudo apt-get install python3.9
```

**3.4.** Verifique a instalação do Python
```
python3 --version
```

## 4. Instalação do PIP

**4.1.** Instale o PIP para gerenciar os pacotes do Python
```
sudo apt-get install pip
```

**4.2.** Verifique a instalação do PIP
```
pip --version
```

## 5. Instalação do Django

**5.1.** Insira o código para instalar o Django
```
sudo apt install python3-django
```

## 6. Instalação do PostgreSQL no Docker

**6.1.** Crie um diretório chamado postgresql (por exemplo dentro de Programas)

```
mkdir Programas
```
```
cd ~/Programas
```
```
mkdir postgresql
```
```
cd postgresql
```

**6.2.** Crie um arquivo chamado Dockerfile com o seguinte conteúdo:

```
xed Dockerfile
```
```
# Version: 1.0
FROM postgres:latest
ENV REFRESHED_AT 2022-07-30
RUN apt-get update && apt-get install -y locales
RUN touch /usr/share/locale/locale.alias
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8
RUN sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && locale-gen && update-locale LANG=pt_BR.UTF-8
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
```

**6.3.** Criar a imagem do PostgreSQL que usaremos
```
sudo docker build -t="SEUUSUARIO/postgresql" .
```

**6.4.** Crie o container do PostgreSQL:
```
sudo docker network create rede_postgresql
```
```
sudo docker volume create --name postgresql_data
```
```
sudo docker run -i -t -d --name postgresql --net=rede_postgresql -p 5432:5432 \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=12345 \
--volume postgresql_data:/var/lib/postgresql/data \
SEUUSUARIO/postgresql
```

**6.5.** Instale o pgagmin4 como aplicação desktop
```
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
```
```
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/jammy pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
```
```
sudo apt update && sudo apt install -y pgadmin4-desktop
```

**6.6.** Adicione o servidor do PostgreSQL clicando em Add Server

General → Name: PostgreSQL Container

Connection → Host name/address: localhost

Connection → Username: postgres

Connection → Password: 12345


## 7. Instale o Visual Studio Code

**7.1.** Utilize o link direto abaixo para baixar o Visual Studio Code:

https://code.visualstudio.com/docs/?dv=linux64_deb

O Linux Mint e KDE neon possuem programas para instalar arquivos ```.deb```. Para isso, basta apenas clicar duas vezes no arquivo baixado (localizado na pasta ```Downloads```) e clicar em *Instalar*.

**Após instalar o VS Code, vá até no ícone de extensões e instale Python (caso não apareça, procure na barra de busca) e instale o Django (procure na barra de busca)**











