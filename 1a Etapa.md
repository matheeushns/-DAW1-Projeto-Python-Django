# 1ª Etapa

## Instalação do Docker

Antes de começar, atualize o sistema:

```
sudo apt update
```
```
sudo apt upgrade
```


### Instale os pacotes de pré-requisitos:

```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

### Adicione chaves GPG de acesso:

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
### Adicione o repositório do Docker às fotos do APT

```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```


### Atualize o sistema novamente:

```
sudo apt update
```

### Garanta que você está instalando a partir do repositório do Docker, ao invés do repositório padrão do Ubuntu ao usar este comando:

```
apt-cache policy docker-ce
```
### Instale o Docker
```
sudo apt install docker-ce
```

### Verifique se o Docker está funcionando:
```
sudo systemctl status docker
```

## Instalação do Portainer

### Digite o comando para criar um volume para o Portainer
```
sudo docker volume create portainer_data
```

### Digite o comando abaixo para instalar o Portainer dentro do volume criado:

```
sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

### Acesse o endereço no navegador para abrir o Portainer
```
https://localhost:9443
```
**Crie a senha 123456789012 como padrão.**


## Instalação do Python

### Adicione o repositório
```
sudo add-apt-repository ppa:deadsnakes/ppa
```

### Atualize
```
sudo apt update
```

### Instale o Python

```
sudo apt-get install python3.9
```

### Verifique a instalação do Python
```
python3 --version
```

## Instalação do PIP
Instale o PIP para gerenciar os pacotes do Python
```
sudo apt-get install pip
```

### Verifique a instalação do PIP
```
pip -–version
```

## Instalação do Django

### Insira o código para instalar o Django
```
python3 -m pip install Django
```

## Instalação do PostgreSQL no Docker

### Crie um diretório chamado postgresql (por exemplo dentro de Programas)

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

### Crie um arquivo chamado Dockerfile com o seguinte conteúdo:

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

### Criar a imagem do PostgreSQL que usaremos

```
sudo docker build -t="{SEUUSUARIO}/postgresql" .
```

### Criar o container do PostgreSQL

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
{SEUUSUARIO}/postgresql
```
### Instalar o pgagmin4 como aplicação desktop

```
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
```
```
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/jammy pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
```
```
sudo apt update && sudo apt install -y pgadmin4-desktop
```

### Adicione o servidor do PostgreSQL clicando em Add Server

General → Name: PostgreSQL Container

Connection → Host name/address: localhost

Connection → Username: postgres

Connection → Password: 12345


### Instale o Visual Studio Code
```
https://code.visualstudio.com/docs/?dv=linux64_deb
```

**Após instalar o VS Code, vá até no ícone de extensões e instale Python (caso não apareça, procure na barra de busca) e instale o Django (procure na barra de busca)**











