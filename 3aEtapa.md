## 3ª Etapa

### 1. Criando a base para o projeto "Rotas"

**1.1.** Primeiramente crie, no diretório de *Projetos* o projeto *rotas*
```
cd Projetos
```
```
django.admin startproject rotas
```

**1.2.** Depois acesse a pasta do projeto
```
cd rotas
```

**1.3.**  Ainda no terminal, abra o Visual Studio Code com o projeto
```
code .
```

**1.4.** E após isso, digite no terminal
```
python3 manage.py runserver 8080
```

Após isso, na pasta raiz de *rotas* crie a pasta chamada *templates*

### 2. Configurando o Template

**2.1.** Crie um arquivo *template.html* dentro do diretório *templates*.
```
cd ~/Projetos/Projetos/rotas
```
```
mkdir templates
```
```
cd templates
```
```
cd ..
```
```
code .
```

Após o comando ```code.```, você que o Visual Studio Code abrirá. Nele, será criado o arquivo ```template.html``` dentro da pasta *template* criada anteriormente.

**2.2.** Para isso, clique com o botão direito e clique em *New file...*. e nomeie ele como ```template.html```

**2.3.** No arquivo ```template.html```, adicione o seguinte código:
``` HTML
<!DOCTYPE html>
<html>
<head>
    <title>Teste 1</title>
</head>
<body>
    <h1>{{ mensagem }}</h1>
</body>
</html>
```

Antes de configurar as rotas faça o seguinte:

**2.4.** Vá até o arquivos ```settings.py``` até encontrar esta parte do código

``` Python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Onde está ```'DIRS': []``` você irá colocar preencher os colchetes com ```BASE_DIR / 'templates'``` e deverá ficar assim:

``` Python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Agora, vamos configurar as rotas.

### 3. Teste 1: Rota simples

**3.1.** Configurando a URL
**3.1.1.** Abra o arquivo ```urls.py``` do seu projeto e adicione o código abaixo
``` Python
from rotas.views import teste1

urlpatterns = [
    path('teste1/', teste1, name='rota_teste1'),
]
```

**3.2.** Implementando a função de visualização

**3.2.1.** Crie o arquivo ```views.py``` no seu projeto (caso não exista) na raiz do mesmo.

**3.2.2.** Adicione o seguinte código
``` Python
from django.shortcuts import render

def teste1(request):
    mensagem = "Teste 1: Rota executou com sucesso!"
    return render(request, 'template.html', {'mensagem': mensagem})]
```



