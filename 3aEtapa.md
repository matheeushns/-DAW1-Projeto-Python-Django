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

**3.3.** Acessando a rota

**3.3.1.** Abra um navegador web e acesse a URL: ```http://localhost:8080/teste1/```

Você verá a mensagem *Teste 1: Rota executou com sucesso!* na tela.

### 4. Teste 2: Usando parâmetros na URL

**4.1.** Configurando a URL
**4.1.1.** Abra o arquivo ```urls.py``` do seu projeto e substitua o código presente pelo código abaixo:
``` Python
from rotas.views import teste1, teste2

urlpatterns = [
    path('teste1/', teste1, name='rota_teste1'),
    path('teste2/<int:parametro>', teste2, name='rota_teste2'),
]
```

**4.1.2.** No arquivo ```views.py```, substitua o código presente pelo código abaixo:
``` Python
from django.shortcuts import render

def teste2(request, parametro):
    mensagem = f"Teste 2: Rota executou com sucesso recebendo o valor {parametro}!"
    return render(request, 'template.html', {'mensagem': mensagem})
```

**4.2.** Acessando a rota

**4.2.1.** Abra um navegador web e acesse a URL: ```http://localhost:8080/teste2/10```

Você verá a mensagem *Rota executou com sucesso recebendo o valor 10!* na tela.

### 5. Teste 3: Processando valores na query String

**5.1.** Configurando a URL
**5.1.1.** Abra o arquivo ```urls.py``` do seu projeto e substitua o código presente pelo código abaixo:
``` Python
from rotas.views import teste1, teste2, teste3

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teste1/', teste1, name='rota_teste1'),
    path('teste2/<int:parametro>', teste2, name='rota_teste2'),
    path('teste3/', teste3, name='rota_teste3'),
]
```

**5.1.2.** No arquivo ```views.py```, substitua o código presente pelo código abaixo:
``` Python
from django.shortcuts import render
from django.http import QueryDict

def teste3(request):
    # Extrai os valores da query string
    valor = request.GET.get('valor')
    quantidade = request.GET.get('quantidade')

    # Gera a mensagem com base nos valores extraídos
    if valor and quantidade:
        mensagem = f"Teste 3: Rota executou com sucesso recebendo o valor {valor} e quantidade {quantidade}!"
    else:
        mensagem = "Teste 3: Rota precisa de 'valor' e 'quantidade' na query string!"

    return render(request, 'template.html', {'mensagem': mensagem})
```

**5.2.** Acessando a rota

**5.2.1.** Abra um navegador web e acesse a URL: ```http://localhost:8080/teste3/?valor=10&quantidade=5```
