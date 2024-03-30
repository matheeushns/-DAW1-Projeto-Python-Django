## 4ª Etapa: Formulários

**1.** Crie um novo projeto dentro da pasta Projetos.
```
cd Projetos
```
```
django-admin startproject Formulario
```

**2.** Vá até o projeto criado.
```
cd Formulario
```

**3.** Abra o projeto no Visual Studio Code com ```code .```.


**4.** No Visual Studio Code, clique com o botão direito na pasta *Formulario* e clique em *New file…*

**5.** Nomeie o novo arquivo como ```views.py```.

**6.** Cole o código abaixo em ```views.py```.
``` Python
from django.shortcuts import render, redirect
from .forms import FormularioForm

formulario_list = []

def index(request):
    form = FormularioForm()
    if request.method == 'POST':
        form = FormularioForm(request.POST)
        if form.is_valid():
            formulario_data = {
                'text_field': form.cleaned_data['text_field'],
                'integer_field': form.cleaned_data['integer_field'],
                'boolean_field': form.cleaned_data['boolean_field'],
                'select_field': form.cleaned_data['select_field'],
                'radio_field': form.cleaned_data['radio_field'],
            }
            
            formulario_list.append(formulario_data)
            context = {'form': FormularioForm(), 'formulario_list': formulario_list}
            return render(request, 'index.html', context)
    else:
        context = {'form': FormularioForm()}
        return render(request, 'index.html', context)
```

**7.** No arquivo ```urls.py```, substitua todo o código por este abaixo.
``` Python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

**8.** Em uma área vazia da estrutura do projeto, clique com o botão direito e clique *New folder…* e nomeie como ```templates```

**9.** Na pasta ```templates```, clique com o botão direito, clique em *New file…* e nomeie como ```index.html```.

**10.** No arquivo index.html, cole o código abaixo:
``` HTML
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulário</title>
</head>
<body>
    <form action="" method="post">
        {% csrf_token %}
        {{ form.as_p }}

        <input type="submit">
    </form>

    <h2>Dados dos Formulários</h2>
    <ul>
        {% for formulario_data in formulario_list %}
        <li>
            Nome: {{ formulario_data.text_field }}<br>
            Idade: {{ formulario_data.integer_field }}<br>
            Estuda?: {{ formulario_data.boolean_field }}<br>
            Opção do Select: {{ formulario_data.select_field }}<br>
            Opção do Radio: {{ formulario_data.radio_field }}<br>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
```

**11.** Em settings.py, encontre o seguinte código:
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
e substitua pelo código abaixo:
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

**12.** Clique com o botão direito na pasta ```Formulario```, clique em *New file…* e nomeie como ```forms.py```.

**13.** Em ```forms.py```, cole o código abaixo:
``` Python
from django import forms
from django.forms import RadioSelect

   
class FormularioForm(forms.Form):
    select_choices = [
        ("Opção 1","Opção 1"),
        ("Opção 2", "Opção 2"),
        ("Opção 3", "Opção 3")
    ]
    radio_choices = [
        ("Opção 1","Opção 1"),
        ("Opção 2", "Opção 2"),
        ("Opção 3", "Opção 3")
    ]
    text_field = forms.CharField(max_length=50,
                                 label = "Nome ")
    integer_field = forms.IntegerField(label = "Idade ")
    boolean_field = forms.BooleanField(label = "Estuda? ")
    select_field = forms.ChoiceField(choices=select_choices,
                                     label = "Opções de Select ")
    radio_field = forms.ChoiceField(choices=radio_choices,
                                    label = "Opções de Radio ",
                                      widget=forms.RadioSelect)
```

**14.** Salve o projeto, rode o programa e verifique as funcionalidades:
```
python3 manage.py runserver 8080
```
Acesse pelo navegador: http://127.0.0.1:8080
