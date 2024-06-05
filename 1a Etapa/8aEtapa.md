## Etapa 8: Criando as páginas "Cadastrar doação" e "Pesquisar doação"

### OBS.: Para iniciar a etapa 8, você precisa ter concluido a Etapa 7

**1.** Abra o terminal 

**2.** Vá até o caminho da pasta do projeto criado na **Etapa 7**.

```
cd Projetos/doacoes
```

**3.** Abra o Visual Studio Code no projeto.

```
code .
```

**4.** Em `forms.py` adicione o seguinte código abaixo do existente.

``` Python
class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['data', 'hora', 'volume']

    data = forms.DateField(
        label='DATA',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        validators=[MinValueValidator(limit_value=datetime.date.today, message='A data não pode ser anterior a hoje.')]
    )

    hora = forms.TimeField(
        label='HORA',
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )

    volume = forms.FloatField(
        label='VOLUME',
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        validators=[MinValueValidator(limit_value=0.1, message='O volume deve ser maior que 0.1.')]
    )

    def clean_data(self):
        data = self.cleaned_data['data']
        if data < datetime.date.today():
            formatted_today = datetime.date.today().strftime('%d/%m/%Y')
            raise forms.ValidationError(f'A data não pode ser anterior a {formatted_today}.')
        return data
    
    def clean_hora(self):
        hora = self.cleaned_data['hora']
        hora_min = datetime.time(8, 0)
        hora_max = datetime.time(18, 0)
        if hora < hora_min or hora > hora_max:
            raise forms.ValidationError('A hora deve estar entre 08:00 e 18:00.')
        return hora

    def clean_volume(self):
        volume = self.cleaned_data['volume']
        if volume < 300:
            raise forms.ValidationError('O volume deve ser maior que 300ml.')
        if volume > 450:
            raise forms.ValidationError('O volume não pode ser maior que 450ml.')
        return volume
    
class DoadorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doador
        fields = ['nome','cpf','tipo_sanguineo','rh']
        

    nome = forms.CharField(
        label='NOME',
         widget=forms.TextInput(attrs={'readonly': True})
    )
    
    cpf = forms.CharField(
        label='CPF',
        widget=forms.TextInput(attrs={'readonly': True})
    )

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
```

**5.** Em `urls.py`, adicione o seguinte código abaixo do existente dentro do bloco `urlpatterns`.

``` Python
    path('cadastrar_doacao/<int:doador_id>/', views.cadastrar_doacao, name='cadastrar_doacao'),
    path('pesquisar_doador_para_doar/', views.pesquisar_doador_para_doar, name='pesquisar_doador_para_doar'),
    path('pesquisar_doacoes/', views.pesquisar_doacoes, name='pesquisar_doacoes'),
    path('doacoes_doador/<int:doador_id>/', views.doacoes_doador, name='doacoes_doador'),
```

**6.** Em `views.py`, adicione o código abaixo no código existente.

``` Python

def cadastrar_doacao(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)
    if request.method == 'POST':
        doacao_form = DoacaoForm(request.POST)
        doador_form = DoadorUpdateForm(request.POST, instance=doador)
        if doacao_form.is_valid() and doador_form.is_valid():
            doacao = doacao_form.save(commit=False)
            doacao.codigo_doador = doador
            doacao.save()
            doador = doador_form.save(commit=False)
            doador.tipo_rh_corretos = True
            doador.tipo_sanguineo = doador_form.cleaned_data['tipo_sanguineo']
            doador.rh = doador_form.cleaned_data['rh']
            doador.save()
            messages.success(request, f'A doação para o(a) doador(a) {doador.nome} foi realizada com sucesso!')
            return redirect('pesquisar_doador_para_doar')
        else:
            messages.error(request, 'Erro ao realizar doação. Verifique os dados.')
    else:
        doacao_form = DoacaoForm()
        doador_form = DoadorUpdateForm(instance=doador)
    
    context = {'doacao_form': doacao_form, 'doador_form': doador_form}
    return render(request, 'cadastrar_doacao.html', context)

def pesquisar_doador_para_doar(request):
    if request.method == 'GET':
        nome = request.GET.get('nome')
        cpf = request.GET.get('cpf')

        doadores = Doador.objects.filter(situacao='ATIVO').order_by('codigo')

        if nome:
            doadores = doadores.filter(nome__icontains=nome)
        if cpf:
            doadores = doadores.filter(cpf=cpf)

        paginator = Paginator(doadores, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if not page_obj:
            messages.error(request, 'Não foram encontrados doadores com os critérios informados.')

        context = {
            'page_obj': page_obj,
            'nome': nome,
            'cpf': cpf
        }

        return render(request, 'pesquisar_doador_para_doar.html', context)
    
    doador_id = request.POST.get('doador_id')
    if doador_id:
        return redirect('cadastrar_doacao', doador_id=doador_id)
    
    return redirect('pesquisar_doador_para_doar')

def pesquisar_doacoes(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    doacoes = Doacao.objects.select_related('codigo_doador').order_by('data')

    if data_inicio:
        doacoes = doacoes.filter(data__gte=data_inicio)
    if data_fim:
        doacoes = doacoes.filter(data__lte=data_fim)

    paginator = Paginator(doacoes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj:
        messages.error(request, 'Não foram encontradas doações com os critérios informados.')

    context = {
        'page_obj': page_obj,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'pesquisar_doacoes.html', context)


def doacoes_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)
    doacoes = Doacao.objects.filter(codigo_doador=doador_id).order_by('-data')
    return render(request, 'doacoes_doador.html', {'doador': doador, 'doacoes': doacoes})
```

**7.** Na pasta **templates**, crie a página `cadastrar_doacao.html` e cole o código abaixo.
``` HTML
{% extends 'base.html' %}

{% block title %}CADASTRO DE DOAÇÕES{% endblock title %}

{% block content %}

<section class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote><span class="card-title">CADASTRAR NOVA DOAÇÃO</span></blockquote>
            <div class="divider red darken-2"></div>
            <div class="py-3 mt-3 mb-3"><br></div>
            <form action="" method="POST" class="row" novalidate>
                {% csrf_token %}
                <div class="row">

                    <blockquote><span class="card-title">DADOS DO DOADOR</span></blockquote>
                    <div class="divider red darken-2"></div>
                    <div class="input-field col s12 m6">
                        <span>{{ doador_form.nome.label_tag }}</span>
                        {{ doador_form.nome }}
                    </div>
                    <div class="input-field col s12 m6">
                        <span>{{ doador_form.cpf.label_tag }}</span>
                        {{ doador_form.cpf }}
                    </div>
                    <div class="input-field col s12 m6">
                        <div class="col s12 m6">
                            <label>TIPO SANGUÍNEO:</label>
                            <div class="input-field">
                                {% for tipo_sangue in doador_form.tipo_sanguineo %}
                                <p>
                                    <label>
                                        {{ tipo_sangue.tag }}
                                        <span>{{ tipo_sangue.choice_label }}</span>
                                    </label>
                                </p>
                                {% endfor %}
                                {% if doador_form.errors.tipo_sanguineo %}
                                <span class="helper-text red-text">{{ doador_form.errors.tipo_sanguineo }}</span>
                                {% endif %}
                            </div>
                        </div>
                        <div class="col s12 m6">
                            <label>RH:</label>
                            <div class="input-field">
                                {% for rh in doador_form.rh %}
                                <p>
                                    <label>
                                        {{ rh.tag }}
                                        <span>{{ rh.choice_label }}</span>
                                    </label>
                                </p>
                                {% endfor %}
                                {% if doador_form.errors.rh %}
                                <span class="helper-text red-text">{{ doador_form.errors.rh }}</span>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="divider red darken-2"></div>
                    <blockquote><span class="card-title">DADOS DA DOAÇÃO</span></blockquote>
                    <div class="divider red darken-2"></div>
                    <div class="input-field col s12 m6">
                        <span>{{ doacao_form.data.label_tag }}</span>
                        {{ doacao_form.data }}
                        {% if doacao_form.data.errors %}
                        {% for error in doacao_form.data.errors %}
                        <span class="helper-text red-text">{{ error }}</span>
                        {% endfor %}
                        {% endif %}
                    </div>
                    <div class="input-field col s12 m6">
                        <span>{{ doacao_form.hora.label_tag }}</span>
                        {{ doacao_form.hora }}
                        {% if doacao_form.hora.errors %}
                        {% for error in doacao_form.hora.errors %}
                        <span class="helper-text red-text">{{ error }}</span>
                        {% endfor %}
                        {% endif %}
                    </div>
                    <div class="input-field col s12 m6">
                        <span>{{ doacao_form.volume.label_tag }}</span>
                        {{ doacao_form.volume }}
                        {% if doacao_form.volume.errors %}
                        {% for error in doacao_form.volume.errors %}
                        <span class="helper-text red-text">{{ error }}</span>
                        {% endfor %}
                        {% endif %}
                    </div>
                </div>

                <div class="input-field col s12">
                    <button type="submit" class="waves-effect waves-light btn">
                        REALIZAR DOAÇÃO
                        <i class="material-icons left">opacity</i>
                    </button>
                    <a href="{% url 'pesquisar_doador_para_doar' %}" class="btn red">
                        VOLTAR À TELA ANTERIOR
                        <i class="material-icons left">arrow_back</i>
                    </a>
                </div>
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

{% endblock content %}
```

**8.** Substitua o código de `main_page.html` pelo o que está abaixo.

``` HTML
{% extends 'base.html' %}

{% block title %}MAIN PAGE{% endblock title %}

{% block content %}
<main role="main" class="container center-align">
    <header>
        <h1 class="center-align teal-text lighten-1">MAIN PAGE</h1>
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
    <section class="row">
        <article class="col s12 m6">
            <section class="card blue lighten-2">
                <div class="card-content white-text">
                    <h2 class="card-title center-align"><i class="large material-icons left">opacity</i>ÁREA PARA REALIZAR DOAÇÃO</h2>
                </div>
                <footer class="card-action center-align">
                    <a href="{% url 'pesquisar_doador_para_doar' %}" class="btn white-text">
                        <i class="material-icons left">opacity</i>PESQUISAR DOADOR PARA DOAR
                    </a>
                </footer>
            </section>
        </article>
        <article class="col s12 m6">
            <section class="card green lighten-2">
                <div class="card-content white-text">
                     <h2 class="card-title center-align"><i class="large material-icons left">search</i>ÁREA PARA PESQUISAR DOAÇÃO</h2>
                </div>
                <footer class="card-action center-align">
                     <a href="{% url 'pesquisar_doacoes' %}" class="btn white-text">
                        <i class="material-icons left">search</i>PESQUISAR DOAÇÕES REALIZADAS
                    </a>
                </footer>
            </section>
        </article>
    </section>
</main>

{% endblock content %}
```

**9.** Crie a página `doacoes_doador.html` dentro da pasta templates e cole o código abaixo.

``` HTML
{% extends 'base.html' %}

{% block title %}DETALHES DO DOADOR E SUAS DOAÇÕES{% endblock title %}

{% block content %}

<section class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">DADOS DO DOADOR</span>
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
        </div>
    </div>
</section>

{% if doacoes %}
<section class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">DOAÇÕES DO DOADOR</span>
            </blockquote>
            <div class="divider red darken-2"></div>
            <div class="py-3 mt-3 mb-3"><br></div>
            <div class="row">
                {% for doacao in doacoes %}
                <div class="col s12 m6">
                    <div class="card blue-grey darken-1">
                        <div class="card-content white-text">
                            <span class="card-title">Doação realizada em {{ doacao.data }}</span>
                            <p><strong>Hora da doação:</strong> {{ doacao.hora }}</p>
                            <p><strong>Volume doado:</strong> {{ doacao.volume }} ml</p>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            <a href="{% url 'pesquisar_doador_para_doar' %}" class="btn red">
                VOLTAR À TELA ANTERIOR
                <i class="material-icons left">arrow_back</i>
            </a>
        </div>
    </div>
</section>
{% else %}
<div class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">NENHUMA DOAÇÃO REALIZADA</span>
            </blockquote>
            <div class="divider red darken-2"></div>
            <div class="py-3 mt-3 mb-3"><br></div>
            <p>O(A) doador(a) <strong>{{ doador.nome }}</strong> ainda não realizou nenhuma doação de sangue.</p>
        </div>        
    </div>
    
</div>
<div class="container">
    <a href="{% url 'pesquisar_doador_para_doar' %}" class="btn red">
        VOLTAR À TELA ANTERIOR
        <i class="material-icons left">arrow_back</i>
    </a>
</div>
{% endif %}

{% endblock content %}
```

**10.** Crie a página `pesquisar_doacoes.html` dentro da pasta **templates** e cole o código abaixo.

``` HTML
{% extends 'base.html' %}

{% block title %}PESQUISAR DOAÇÕES{% endblock title %}

{% block content %}
<section id="search-form" class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">PESQUISAR DOAÇÕES REALIZADAS</span>
            </blockquote>            
            <div class="divider red darken-2"></div>
            <br>
            <form action="{% url 'pesquisar_doacoes' %}" method="GET" novalidate>
                <div class="row">
                    <div class="input-field col s12 m6">
                        <input type="date" name="data_inicio" id="data_inicio" class="validate" value="{{ data_inicio|default:'' }}">
                        <label for="data_inicio" class="active">DATA INÍCIO:</label>
                    </div>
                    <div class="input-field col s12 m6">
                        <input type="date" name="data_fim" id="data_fim" class="validate" value="{{ data_fim|default:'' }}">
                        <label for="data_fim" class="active">DATA FIM:</label>
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

{% if page_obj %}
<section id="search-results" class="container py-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">RESULTADO(S) DA PESQUISA</span>
            </blockquote>
            
            <div class="divider red darken-2"></div>
            <table class="striped centered responsive-table">
                <thead>
                    <tr>
                        <th>CÓDIGO</th>
                        <th>DATA</th>
                        <th>HORA</th>
                        <th>VOLUME(Em ml)</th>
                        <th>DOADOR</th>
                    </tr>
                </thead>
                <tbody>
                    {% for doacao in page_obj %}
                    <tr>
                        <td>{{ doacao.codigo }}</td>
                        <td>{{ doacao.data }}</td>
                        <td>{{ doacao.hora }}</td>
                        <td>{{ doacao.volume }} ml</td>
                        <td>{{ doacao.codigo_doador.nome }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="center-align">
                <ul class="pagination">
                    {% if page_obj.has_previous %}
                        <li class="waves-effect">
                            <a href="?{% if data_inicio %}data_inicio={{ data_inicio }}&{% endif %}{% if data_fim %}data_fim={{ data_fim }}&{% endif %}page={{ page_obj.previous_page_number }}">
                                <i class="material-icons">chevron_left</i>
                            </a>
                        </li>
                    {% else %}
                        <li class="disabled">
                            <a href="#!">
                                <i class="material-icons">chevron_left</i>
                            </a>
                        </li>
                    {% endif %}
                    {% for num in page_obj.paginator.page_range %}
                        {% if page_obj.number == num %}
                            <li class="active">
                                <a href="#!">{{ num }}</a>
                            </li>
                        {% else %}
                            <li class="waves-effect">
                                <a href="?{% if data_inicio %}data_inicio={{ data_inicio }}&{% endif %}{% if data_fim %}data_fim={{ data_fim }}&{% endif %}page={{ num }}">{{ num }}</a>
                            </li>
                        {% endif %}
                    {% endfor %}
                    {% if page_obj.has_next %}
                        <li class="waves-effect">
                            <a href="?{% if data_inicio %}data_inicio={{ data_inicio }}&{% endif %}{% if data_fim %}data_fim={{ data_fim }}&{% endif %}page={{ page_obj.next_page_number }}">
                                <i class="material-icons">chevron_right</i>
                            </a>
                        </li>
                    {% else %}
                        <li class="disabled">
                            <a href="#!">
                                <i class="material-icons">chevron_right</i>
                            </a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </div>
</section>
{% else %}
<div class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">NENHUMA DOAÇÃO A SER PESQUISADA</span>
            </blockquote>
            <div class="divider red darken-2"></div>
            <div class="py-3 mt-3 mb-3"><br></div>
            <p>Ainda não tivemos doações realizadas no nosso sistema para serem pesquisadas.</p>
        </div>        
    </div>
</div>
{% endif %}
{% endblock content %}
```

**11.** Crie uma página chamada `pesquisar_doador_para_doar.html` dentro da pasta **templates** e cole o código abaixo.

``` HTML
{% extends 'base.html' %}

{% block title %}PESQUISAR DOADOR{% endblock title %}

{% block content %}
<section id="search-form" class="container py-4 mb-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">PESQUISAR DOADOR PARA DOAR SANGUE</span>
            </blockquote>
            
            <div class="divider red darken-2"></div>
            <form action="{% url 'pesquisar_doador_para_doar' %}" method="GET" novalidate>
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

{% if page_obj %}
<section id="search-results" class="container py-4">
    <div class="card border">
        <div class="card-content">
            <blockquote>
                <span class="card-title">RESULTADO DA PESQUISA</span>
            </blockquote>
            
            <div class="divider red darken-2"></div>
            <table class="striped centered responsive-table">
                <thead>
                    <tr>
                        <th>CÓDIGO</th>
                        <th>NOME</th>
                        <th>CPF</th>
                        <th>CONTATO</th>
                        <th>TIPO SANGUÍNEO</th>
                        <th>RH</th>
                        <th>DOAR</th>
                        <th>VER DOAÇÕES</th>
                    </tr>
                </thead>
                <tbody>
                    {% for doador in page_obj %}
                    <tr>
                        <td>{{ doador.codigo }}</td>
                        <td>{{ doador.nome }}</td>
                        <td>{{ doador.cpf }}</td>
                        <td>{{ doador.contato }}</td>
                        <td>{{ doador.get_tipo_sanguineo_display }}</td>
                        <td>{{ doador.get_rh_display }}</td>
                        <td>
                            <a href="{% url 'cadastrar_doacao' doador.codigo %}" class="waves-effect waves-light btn">DOAR
                                <i class="material-icons left">opacity</i>
                            </a>
                        </td>
                        <td>
                            <a href="{% url 'doacoes_doador' doador.codigo %}" class="btn white red-text">VER DOAÇÕES
                                <i class="material-icons left">assignment</i>
                            </a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="center-align">
                <ul class="pagination">
                    {% if page_obj.has_previous %}
                        <li class="waves-effect">
                            <a href="?{% if nome %}nome={{ nome }}&{% endif %}{% if cpf %}cpf={{ cpf }}&{% endif %}page={{ page_obj.previous_page_number }}">
                                <i class="material-icons">chevron_left</i>
                            </a>
                        </li>
                    {% else %}
                        <li class="disabled">
                            <a href="#!">
                                <i class="material-icons">chevron_left</i>
                            </a>
                        </li>
                    {% endif %}
                    {% for num in page_obj.paginator.page_range %}
                        {% if page_obj.number == num %}
                            <li class="active">
                                <a href="#!">{{ num }}</a>
                            </li>
                        {% else %}
                            <li class="waves-effect">
                                <a href="?{% if nome %}nome={{ nome }}&{% endif %}{% if cpf %}cpf={{ cpf }}&{% endif %}page={{ num }}">{{ num }}</a>
                            </li>
                        {% endif %}
                    {% endfor %}
                    {% if page_obj.has_next %}
                        <li class="waves-effect">
                            <a href="?{% if nome %}nome={{ nome }}&{% endif %}{% if cpf %}cpf={{ cpf }}&{% endif %}page={{ page_obj.next_page_number }}">
                                <i class="material-icons">chevron_right</i>
                            </a>
                        </li>
                    {% else %}
                        <li class="disabled">
                            <a href="#!">
                                <i class="material-icons">chevron_right</i>
                            </a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </div>
</section>
{% endif %}
{% endblock content %}
```

**12.** Salve todas as modificações e teste todas as funcionalidades adicionadas.

```
python3 manage.py runserver 8080
```
http://127.0.0.1:8080/
