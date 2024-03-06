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

## Instalação do MongoDB no Docker

### Coloque a imagem do MongoDB no Docker
```
sudo docker pull mongodb/mongodb-community-server
```

### Inicie a imagem como container
```
sudo docker run --name mongo -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

### Conecte o MongoDB com mongosh
```
sudo docker exec -it mongo mongosh
```

### Cole o comando abaixo e dê enter
```
db.runCommand(
	{
		hello: 1
	}
)
```

**Digite exit e dê enter para sair**

### Instale o MongoDB Compass
```
https://downloads.mongodb.com/compass/mongodb-compass_1.42.1_amd64.deb
```

### Instale o Visual Studio Code
```
https://code.visualstudio.com/docs/?dv=linux64_deb
```

**Após instalar o VS Code, vá até no ícone de extensões e instale Python (caso não apareça, procure na barra de busca) e instale o Django (procure na barra de busca)**











