## 7ª Etapa: Criando as páginas "Cadastrar doador" e "Pesquisar doador"

**1.** Abra o terminal 

**2.** Vá até o caminho da pasta do projeto criado na **Etapa 6**.

```
cd Projetos/doacoes
```

**3.** Abra o Visual Studio Code no projeto.

```
code .
```

Abaixo está o esquema de diretórios após todo o projeto pronto. Caso tenha dúvidas, poderá retornar aqui para verificar a hierarquia de pastas.
```
/home/seu_usuario/Projetos/doacoes/
│
├── doacoes/
│   ├── __init__.py
│   ├── forms.py
│   ├── migrations/
│   │   └── (arquivos de migração)
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── settings.py
│   ├── wsgi.py
│   └── asgi.py
│
├── static/
│   ├── css/
│   │   └── (arquivos CSS)
│   └── js/
│        └── (arquivos JavaScript)
│
└── templates/
│   ├── base.html
│   ├── cadastrar_doador.html
│   ├── excluir_doador.html
│   ├── main_page.html 
│   └── pesquisar_doador.html
│
├── manage.py
```

**4.** Crie uma pasta chamada templates por fora de todas as pastas do projeto.

**5.** Em `settings.py`, procure pelo bloco de código semelhante e substitua completamente pelo o que está abaixo.

``` Python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

**6.** Ainda em `settings.py`, substitua `LANGUAGE_CODE` para o seguinte código.

``` Python
LANGUAGE_CODE = 'pt-BR'
```

**7.** Ainda em `settings.py`, adicione o seguinte bloco de código abaixo da última linha.

``` Python
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

**8.** Crie (dentro da pasta **doacoes**) os arquivos `views.py` e `forms.py`.

**9.** Cole o código abaixo dentro de `views.py`.

``` Python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Doador
from .forms import DoadorForm
from django.urls import reverse

def cadastrar_doador(request):
    if request.method == 'POST':
        form = DoadorForm(request.POST)
        if form.is_valid():
            if Doador.objects.filter(cpf=form.cleaned_data['cpf']).exists():
                cpf=form.cleaned_data['cpf']
                messages.error(request, f'CPF {cpf} já cadastrado!')
            else:
                nome = form.cleaned_data['nome']
                form.save()
                messages.success(request, f'Doador(a) {nome} cadastrado(a) com sucesso!')
                form = DoadorForm()
                doadores = Doador.objects.all().order_by('codigo')
                context = {'form': form, 'doadores': doadores}
                return render(request, 'cadastrar_doador.html', context)
        else:
            messages.error(request, 'Erro ao cadastrar doador. Verifique os dados.')
    else:
        form = DoadorForm()
    
    doadores = Doador.objects.all()
    context = {'form': form, 'doadores': doadores}
    return render(request, 'cadastrar_doador.html', context)

def editar_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)

    if request.method == 'POST':
        form = DoadorForm(request.POST, instance=doador)
        if form.is_valid():
            form.save()
            messages.success(request, f"Doador(a) {doador.nome} editado(a) com sucesso.")
            return redirect(reverse('pesquisar_doador') + f'?nome={doador.nome}&cpf={doador.cpf}&tipo_sanguineo=Todos&rh=Todos')
    else:
        form = DoadorForm(instance=doador)
    context = {'form': form, 'doador': doador}
    return render(request, 'editar_doador.html', context)

def excluir_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)

    if request.method == 'POST':
        doador.situacao = 'INATIVO'
        doador.save()
        messages.success(request, f"O(A) doador(a) {doador.nome} foi excluído(a) com sucesso.")
        return redirect(reverse('pesquisar_doador') + f'?tipo_sanguineo=Todos&rh=Todos')

    return render(request, 'excluir_doador.html', {'doador': doador})

def pesquisar_doador(request):
    doadores = None

    if request.method == 'GET':
        tipo_sanguineo = request.GET.get('tipo_sanguineo')
        rh = request.GET.get('rh')
        nome = request.GET.get('nome')
        cpf = request.GET.get('cpf')
        doadores = Doador.objects.filter(situacao='ATIVO').order_by('codigo')

        if tipo_sanguineo and tipo_sanguineo != 'Todos':
            doadores = doadores.filter(tipo_sanguineo=tipo_sanguineo)
        if rh and rh != 'Todos':
            doadores = doadores.filter(rh=rh)
        if nome:
            doadores = doadores.filter(nome__icontains=nome)
        if cpf:
            doadores = doadores.filter(cpf=cpf)

    context = {
        'doadores': doadores,
        'nome': nome,
        'cpf': cpf,
        'tipo_sanguineo': tipo_sanguineo,
        'rh': rh
    }

    if doadores is None or not doadores.exists():
        messages.error(request,'Não foram encontrados doadores com os critérios informados.')
        return render(request, 'pesquisar_doador.html', context)
    
    return render(request, 'pesquisar_doador.html', context)

def reativar_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)

    if doador.situacao == 'INATIVO':
        doador.situacao = 'ATIVO'
        doador.save()
        messages.success(request, f'O doador {doador.nome} teve o status alterado para "ATIVO".')
    
    return render(request, 'pesquisar_doador.html')

def main_page(request):
    return render(request, 'main_page.html')
```

**10.** Já em `forms.py` cole o código abaixo.

``` Python
from django import forms
from .models import Doador, TipoSanguineo, RH
from django.core.validators import RegexValidator
from django.forms.widgets import RadioSelect


class DoadorForm(forms.ModelForm):
    class Meta:
        model = Doador
        exclude = ['situacao','tipo_rh_corretos']
        fields = '__all__'

    nome = forms.CharField(min_length=2, label='NOME',validators=[RegexValidator(r'^[A-Za-zÀ-ÖØ-öø-ÿÇç\s]*$', 
                                                                                message='Nome deve conter apenas letras.')],
                                                                                error_messages={'required': 'Por favor, informe um nome.',
                                                                                                'invalid': 'Nome inválido. Por favor, use apenas letras.',
                                                                                                'min_length': 'O nome não pode ter menos de 2 caracteres.'
                           })


    cpf = forms.CharField(min_length=11, max_length=11, label='CPF',validators=[RegexValidator(r'^[0-9]*$', message='CPF deve conter apenas números.')],
                          error_messages={
                                  'required': 'Por favor, informe um CPF.',
                                  'unique': 'Este CPF já está cadastrado e não pode ser inserido novamente.',
                                  'invalid': 'CPF inválido. Por favor, use apenas números',
                                  'min_length': 'CPF deve conter 11 números.',
                                  'max_length': 'CPF deve conter 11 números.'
                              })


    contato = forms.CharField(min_length=11, max_length=11, label='CONTATO',validators=[RegexValidator(r'^[0-9]*$', message='Contato deve conter apenas números.')],
                              error_messages={
                                  'required': 'Por favor, informe um número para contato.',
                                  'invalid': 'Número para contato inválido. Por favor, use apenas números',
                                  'min_length': 'O número para contato deve conter 11 números.',
                                  'max_length': 'O número para contato deve conter 11 números.'
                              })

    tipo_sanguineo = forms.ChoiceField(
        label='TIPO SANGUÍNEO',
        choices=TipoSanguineo.choices,
        widget=RadioSelect(attrs={'class': 'with-gap'})
    )

    rh = forms.ChoiceField(
        label='RH',
        choices=RH.choices,
        widget=RadioSelect(attrs={'class': 'with-gap'})
    )

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        return ''.join(filter(str.isdigit, cpf)) 

    def clean_contato(self):
        contato = self.cleaned_data['contato']
        return ''.join(filter(str.isdigit, contato))
```

**11.** Após isso, localize o arquivo `urls.py` e substitua o código que está lá pelo abaixo.

```Python
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='main_page'), name='index'),
    path('main_page/', views.main_page, name='main_page'),
    path('cadastrar_doador/', views.cadastrar_doador, name='cadastrar_doador'),
    path('editar_doador/<int:doador_id>/', views.editar_doador, name='editar_doador'),
    path('excluir_doador/<int:doador_id>/', views.excluir_doador, name='excluir_doador'),
    path('pesquisar_doador/', views.pesquisar_doador, name='pesquisar_doador'),
    path('reativar_doador/<int:doador_id>/', views.reativar_doador, name='reativar_doador'),
]
```

**12.** Agora, crie os seguintes arquivos dentro da pasta **templates**: `base.html`, `cadastrar_doador.html`, `editar_doador.html`, `excluir_doador.html`, `main_page.html` e `pesquisar_doador.html`.

**13.** Crie uma pasta chamada **static**. Lembrando que essa pasta será criada no mesmo nível das pastas **doacoes** e **templates**.

**14.** Faça o download do Materialize. Ele será nosso frontend do nosso projeto.

https://github.com/Dogfalo/materialize/releases/download/1.0.0/materialize-v1.0.0.zip

**15.** Após o download, extraia e coloque as pastas **css** e **js** dentro da pasta **static** criada no projeto.

**16.** Vá até `base.html` e cole o bloco de código abaixo.

``` HTML
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema de Doações{% endblock title %}</title>
    {% load static %}
    <link href="{% static 'css/materialize.min.css' %}" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
</head>

<body>
    <main>
        {% block content %}

        {% endblock content %}
    </main>
    <script src="{% static 'js/materialize.min.js' %}"></script>
</body>

</html>
```


**17.** Vá até `cadastrar_doador.html` e coloque o código abaixo.

``` HTML
{% extends 'base.html' %}

{% block title %}CADASTRO DE DOADORES{% endblock title %}

{% block content %}
<section id="cadastro" class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote><span class="card-title">CADASTRAR NOVO DOADOR</span></blockquote>
            <div class="divider red darken-2"></div>
            <form action="{% url 'cadastrar_doador' %}" method="POST" class="row" novalidate>
                {% csrf_token %}
                <div class="input-field col s12 m6">
                    {{ form.nome.label_tag }}
                    {{ form.nome }}
                    {% if form.nome.errors %}
                    {% for error in form.nome.errors %}
                    <span class="helper-text red-text">{{ error }}</span>
                    {% endfor %}
                    {% endif %}
                </div>
                <div class="input-field col s12 m6">
                    {{ form.cpf.label_tag }}
                    {{ form.cpf }}
                    {% if form.cpf.errors %}
                    {% for error in form.cpf.errors %}
                    <span class="helper-text red-text">{{ error }}</span>
                    {% endfor %}
                    {% endif %}
                </div>
                <div class="input-field col s12 m6">
                    {{ form.contato.label_tag }}
                    {{ form.contato }}
                    {% if form.contato.errors %}
                    {% for error in form.contato.errors %}
                    <span class="helper-text red-text">{{ error }}</span>
                    {% endfor %}
                    {% endif %}
                </div>
                <div class="input-field col s12 m6">
                    <div class="col s12 m6">
                        <label>TIPO SANGUÍNEO:</label>
                        <div class="input-field">
                            {% for tipo_sangue in form.tipo_sanguineo %}
                            <p>
                                <label>
                                    {{ tipo_sangue.tag }}
                                    <span>{{ tipo_sangue.choice_label }}</span>
                                </label>
                            </p>
                            {% endfor %}
                            {% if form.tipo_sanguineo.errors %}
                            <span class="helper-text red-text">{{ form.tipo_sanguineo.errors }}</span>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col s12 m6">
                        <label>RH:</label>
                        <div class="input-field">
                            {% for rh in form.rh %}
                            <p>
                                <label>
                                    {{ rh.tag }}
                                    <span>{{ rh.choice_label }}</span>
                                </label>
                            </p>
                            {% endfor %}
                            {% if form.rh.errors %}
                            <span class="helper-text red-text">{{ form.rh.errors }}</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="input-field col s12">
                    <button type="submit" class="waves-effect waves-light btn">
                        CADASTRAR
                        <i class="material-icons left">person_add</i>
                    </button>
                    <a href="{% url 'main_page' %}" class="btn red">
                        VOLTAR À TELA PRINCIPAL
                        <i class="material-icons left">arrow_back</i>
                    </a>
                </div>
            </form>
        </div>
    </div>
</section>


{% if messages %}
<div class="container">
    <div class="row">
        <div class="col s12">
            {% for message in messages %}
            <div
                class="card-panel {% if message.tags == 'error' %}red lighten-2{% elif message.tags == 'success' %}teal lighten-2{% endif %}">
                <span class="white-text">{{ message }}</span>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endif %}



<section id="doadores" class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote><span class="card-title">DOADORES CADASTRADOS</span></blockquote>
            <div class="divider red darken-2"></div>
            {% if doadores %}
            <table class="striped bordered centered">
                <thead>
                    <tr>
                        <th>CÓDIGO</th>
                        <th>NOME</th>
                        <th>CPF</th>
                        <th>CONTATO</th>
                        <th>TIPO SANGUÍNEO</th>
                        <th>RH</th>
                        <th>SITUAÇÃO</th>
                    </tr>
                </thead>
                <tbody>
                    {% for doador in doadores %}
                    <tr>
                        <td>{{ doador.codigo }}</td>
                        <td>{{ doador.nome }}</td>
                        <td>{{ doador.cpf }}</td>
                        <td>{{ doador.contato }}</td>
                        <td>{{ doador.get_tipo_sanguineo_display }}</td>
                        <td>{{ doador.get_rh_display }}</td>
                        <td>{{ doador.situacao }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="card-panel">
                <p>Nenhum doador cadastrado ainda.</p>
            </div>
            {% endif %}
        </div>
    </div>
</section>

{% endblock content %}
```

**18.** Vá até `editar_doador.html` e cole o bloco de código abaixo.

``` HTML
{% extends 'base.html' %}

{% block title %}EDITAR DOADOR{% endblock title %}

{% block content %}

<!-- Bloco de Dados Atuais do Doador -->
<section class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">DADOS ATUAIS DO DOADOR</span>
            </blockquote>
            <div class="divider red darken-2"></div>
            <div class="py-3 mt-3 mb-3"><br></div>    
            <div class="row">
                <div class="col s12 m6">                   
                    <p><strong>NOME:</strong> {{ doador.nome }}</p>
                    <p><strong>CPF:</strong> {{ doador.cpf }}</p>
                    <p><strong>CONTATO:</strong> {{ doador.contato }}</p>
                </div>
                <div class="col s12 m6">
                    <p><strong>TIPO SANGUÍNEO:</strong> {{ doador.get_tipo_sanguineo_display }}</p>
                    <p><strong>RH:</strong> {{ doador.get_rh_display }}</p>
                </div>
            </div>
            {% if doador.situacao == 'INATIVO' %}
            <a href="{% url 'reativar_doador' doador.codigo %}" class="btn waves-effect waves-light">Reativar Doador</a>

            {% endif %}
        </div>
    </div>
</section>

{% if doador.situacao == 'ATIVO' %}
<!-- Formulário de Edição do Doador -->

<section class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">EDITAR DOADOR</span>
            </blockquote>
            <div class="divider red darken-2"></div>
            <div class="py-3 mt-3 mb-3"><br></div>          
            <form method="POST" class="row" novalidate>
                {% csrf_token %}
                <div class="input-field col s12 m6">
                    {{ form.nome.label_tag }}
                    {{ form.nome }}
                    {% if form.nome.errors %}
                    {% for error in form.nome.errors %}
                    <span class="helper-text red-text">{{ error }}</span>
                    {% endfor %}
                    {% endif %}
                </div>
                <div class="input-field col s12 m6">
                    {{ form.cpf.label_tag }}
                    {{ form.cpf }}
                    {% if form.cpf.errors %}
                    {% for error in form.cpf.errors %}
                    <span class="helper-text red-text">{{ error }}</span>
                    {% endfor %}
                    {% endif %}
                </div>
                <div class="input-field col s12 m6">
                    {{ form.contato.label_tag }}
                    {{ form.contato }}
                    {% if form.contato.errors %}
                    {% for error in form.contato.errors %}
                    <span class="helper-text red-text">{{ error }}</span>
                    {% endfor %}
                    {% endif %}
                </div>
                <div class="input-field col s12 m6">
                    <div class="col s12 m6">
                        <label>TIPO SANGUÍNEO:</label>
                        <div class="input-field">
                            {% for tipo_sangue in form.tipo_sanguineo %}
                            <p>
                                <label>
                                    {{ tipo_sangue.tag }}
                                    <span>{{ tipo_sangue.choice_label }}</span>
                                </label>
                            </p>
                            {% endfor %}
                            {% if form.tipo_sanguineo.errors %}
                            <span class="helper-text red-text">{{ form.tipo_sanguineo.errors }}</span>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col s12 m6">
                        <label>RH:</label>
                        <div class="input-field">
                            {% for rh in form.rh %}
                            <p>
                                <label>
                                    {{ rh.tag }}
                                    <span>{{ rh.choice_label }}</span>
                                </label>
                            </p>
                            {% endfor %}
                            {% if form.rh.errors %}
                            <span class="helper-text red-text">{{ form.rh.errors }}</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col s12">
                        <button type="submit" class="waves-effect waves-light btn">SALVAR
                            <i class="material-icons left">save</i>
                        </button>
                        <a href="{% url 'pesquisar_doador' %}" class="btn red">CANCELAR E VOLTAR
                            <i class="material-icons left">arrow_back</i>
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>

</section>
{% endif %}
{% endblock content %}
```

**19.** Vá até `excluir_doador.html` e cole o código abaixo.

``` HTML
{% extends 'base.html' %}

{% block title %}EXCLUIR DOADOR{% endblock title %}

{% block content %}
<main role="main" class="container">
    <div class="row">
        <div class="col s12 m6 offset-m3 valign-wrapper" style="min-height: 100vh;">
            <div class="card-panel grey lighten-5 z-depth-1" style="width: 100%;">
                <h3 class="center-align">CONFIRMAÇÃO DE EXCLUSÃO</h3>
                <p class="center-align">Tem certeza que deseja excluir o doador <strong>{{ doador.nome }}</strong>?</p>

                <form method="POST" class="center-align">
                    {% csrf_token %}
                    <button type="submit" class="btn red">CONFIRMAR</button>
                    <a href="{% url 'pesquisar_doador' %}" class="btn blue">CANCELAR</a>
                </form>
            </div>
        </div>
    </div>
</main>
{% endblock content %}
```

**19.** Em `main_page.html` cole o bloco de código abaixo.

``` HTML
{% extends 'base.html' %}

{% block title %}MAIN PAGE{% endblock title %}

{% block content %}
<main role="main" class="container center-align">
    <header>
        <h1 class="center-align">MAIN PAGE</h1>
    </header>
    <section class="row">
        <article class="col s12 m6">
            <section class="card blue lighten-2">
                <div class="card-content white-text">
                    <h2 class="card-title center-align"><i class="large material-icons left">person_add</i>ÁREA PARA INSERIR DOADOR</h2>
                </div>
                <footer class="card-action center-align">
                    <a href="{% url 'cadastrar_doador' %}" class="btn white-text">
                        <i class="material-icons left">person_add</i>CADASTRAR DOADOR
                    </a>
                </footer>
            </section>
        </article>
        <article class="col s12 m6">
            <section class="card green lighten-2">
                <div class="card-content white-text">
                    <h2 class="card-title center-align"><i class="large material-icons left">search</i>ÁREA PARA PESQUISAR DOADOR</h2>
                </div>
                <footer class="card-action center-align">
                    <a href="{% url 'pesquisar_doador' %}" class="btn white-text">
                        <i class="material-icons left">search</i>PESQUISAR DOADOR
                    </a>
                </footer>
            </section>
        </article>
    </section>
</main>

{% endblock content %}
```

**20.** Em `pesquisar_doador.html` cole o código abaixo.

```HTML
{% extends 'base.html' %}

{% block title %}PESQUISAR DOADOR{% endblock title %}

{% block content %}
<section id="search-form" class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">PESQUISAR DOADOR(ES)</span>
            </blockquote>
            
            <div class="divider red darken-2"></div>
            <form action="{% url 'pesquisar_doador' %}" method="GET" novalidate>
                <div class="row">
                    <div class="input-field col s12 m6">
                        <label for="nome">NOME:</label>
                        <input type="text" name="nome" id="nome" class="validate" value="{{ nome|default:'' }}">
                    </div>
                    <div class="input-field col s12 m6">
                        <label for="cpf">CPF:</label>
                        <input type="text" name="cpf" id="cpf" class="validate" maxlength="11" value="{{ cpf|default:'' }}">
                    </div>
                </div>
                <div class="row">
                    <div class="col s12 m6">
                        <label>TIPO SANGUÍNEO:</label>
                        <div class="input-field">
                            <p>
                                <label>
                                    <input name="tipo_sanguineo" type="radio" value="A" class="with-gap" {% if tipo_sanguineo == 'A' %}checked{% endif %}/>
                                    <span>A</span>
                                </label>
                            </p>
                            <p>
                                <label>
                                    <input name="tipo_sanguineo" type="radio" value="B" class="with-gap" {% if tipo_sanguineo == 'B' %}checked{% endif %}/>
                                    <span>B</span>
                                </label>
                            </p>
                            <p>
                                <label>
                                    <input name="tipo_sanguineo" type="radio" value="AB" class="with-gap" {% if tipo_sanguineo == 'AB' %}checked{% endif %}/>
                                    <span>AB</span>
                                </label>
                            </p>
                            <p>
                                <label>
                                    <input name="tipo_sanguineo" type="radio" value="O" class="with-gap" {% if tipo_sanguineo == 'O' %}checked{% endif %}/>
                                    <span>O</span>
                                </label>
                            </p>
                            <p>
                                <label>
                                    <input name="tipo_sanguineo" type="radio" value="Todos" class="with-gap" {% if tipo_sanguineo == 'Todos' %}checked{% endif %}/>
                                    <span>Todos</span>
                                </label>
                            </p>
                        </div>
                    </div>
                    <div class="col s12 m6">
                        <label>RH:</label>
                        <div class="input-field">
                            <p>
                                <label>
                                    <input name="rh" type="radio" value="POSITIVO" class="with-gap" {% if rh == 'POSITIVO' %}checked{% endif %}/>
                                    <span>POSITIVO</span>
                                </label>
                            </p>
                            <p>
                                <label>
                                    <input name="rh" type="radio" value="NEGATIVO" class="with-gap" {% if rh == 'NEGATIVO' %}checked{% endif %}/>
                                    <span>NEGATIVO</span>
                                </label>
                            </p>
                            <p>
                                <label>
                                    <input name="rh" type="radio" value="Todos" class="with-gap" {% if rh == 'Todos' %}checked{% endif %}/>
                                    <span>Todos</span>
                                </label>
                            </p>
                        </div>
                    </div>
                </div>                                
                <div class="input-field">
                    <button type="submit" class="waves-effect waves-light btn">
                        PESQUISAR
                        <i class="material-icons left">search</i>
                    </button>
                    <a href="{% url 'main_page' %}" class="btn red">
                        VOLTAR À TELA PRINCIPAL
                        <i class="material-icons left">arrow_back</i>
                    </a>
                </div>
            </form>
        </div>
    </div>
</section>

{% if messages %}
{% if messages %}
<div class="container py-4">
    <div class="card-content">
        {% for message in messages %}
            {% if message.tags == 'error' %}
                <div class="card-panel red lighten-2">
                    <span class="white-text">{{ message }}</span>
                </div>
            {% elif message.tags == 'success' %}
                <div class="card-panel teal lighten-2">
                    <span class="white-text">{{ message }}</span>
                </div>
            {% endif %}
        {% endfor %}
    </div>
</div>
{% endif %}
{% else %}
{% if doadores %}
<section id="search-results" class="container py-4">

    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">RESULTADO(S) DA PESQUISA</span>
            </blockquote>
            
            <div class="divider red darken-2"></div>
            <table class="striped centered">
                <thead>
                    <tr>
                        <th>CÓDIGO</th>
                        <th>NOME</th>
                        <th>CPF</th>
                        <th>CONTATO</th>
                        <th>TIPO SANGUÍNEO</th>
                        <th>RH</th>
                        <th>ALTERAR</th>
                        <th>REMOVER</th>
                    </tr>
                </thead>
                <tbody>
                    {% for doador in doadores %}
                    <tr>
                        <td>{{ doador.codigo }}</td>
                        <td>{{ doador.nome }}</td>
                        <td>{{ doador.cpf }}</td>
                        <td>{{ doador.contato }}</td>
                        <td>{{ doador.get_tipo_sanguineo_display }}</td>
                        <td>{{ doador.get_rh_display }}</td>
                        <td><a href="{% url 'editar_doador' doador.codigo %}" class="btn blue">ALTERAR
                                <i class="material-icons left">edit</i>
                            </a></td>
                        <td><a href="{% url 'excluir_doador' doador.codigo %}" class="btn red">REMOVER
                                <i class="material-icons left">remove_circle_outline</i>
                            </a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

</section>
{% endif %}
{% endif %}
{% endblock content %}
```

**21.** Salve todas as modificações e teste todas as funcionalidades adicionadas.

```
python3 manage.py runserver 8080
```
http://127.0.0.1:8080/
