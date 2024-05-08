## 6ª Etapa: Criando projeto Doações com BD

### Criação do Banco de Dados

**1.** Abra o programa **pgAdmin 4** buscando pelo menu de início.

**2.** Conecte na conexão postgres criada na 1ª Etapa.

**3.** Clique com o botão direito em **Databases (1)**  e clique em **Create** e depois em **Database…**

**4.** No campo **Database**, dê o nome de `doacoes`.

**5.** Clique em **Save**.

### Criação do projeto integrado ao banco de dados

**1.** Na pasta **Projetos**, crie um projeto chamado `doacoes`.

```
django-admin startproject doacoes
```

**2.** Entre na pasta do projeto e abra o Visual Studio Code.

```
cd doacoes
```
```
code .
```

**3.** Clique com o botão direito em cima do nome do projeto, clique em **New file…** e nomeie o arquivo novo como `models.py`.

**4.** No arquivo `models.py` criado, cole o seguinte código:

``` Python
from django.db import models

class TipoSanguineo(models.TextChoices):
    A = 'A'
    B = 'B'
    AB = 'AB'
    O = 'O'

class RH(models.TextChoices):
    POSITIVO = 'POSITIVO'
    NEGATIVO = 'NEGATIVO'


class Doador(models.Model):
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    contato = models.CharField(max_length=11)
    tipo_sanguineo = models.CharField(max_length=2, choices=TipoSanguineo.choices)
    rh = models.CharField(max_length=8, choices=RH.choices)
    tipo_rh_corretos = models.BooleanField(default=False)
    situacao = models.CharField(max_length=7,default="ATIVO")

    def __str__(self) -> str:
        return self.nome


class Doacao(models.Model):
    codigo = models.AutoField(primary_key=True)
    data = models.DateField()
    hora = models.TimeField()
    volume = models.FloatField()
    situacao = models.CharField(max_length=7,default="ATIVO")
    codigo_doador = models.ForeignKey(Doador, on_delete=models.CASCADE)
```

**5.** Instale o pacote para auxiliar com o banco de dados.

```
pip install psycopg2-binary
```

**6.** No arquivo `settings.py`, localize e altere com os seguintes blocos de cósigos:

``` Python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'doacoes',
]
```
``` Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'doacoes',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**7.** Salve o projeto, rode o programa e verifique as funcionalidades:
```
python3 manage.py makemigrations doacoes
```
```
python3 manage.py migrate
```
```
python3 manage.py runserver 8080
```

Abra no navegador: http://127.0.0.1:8080
