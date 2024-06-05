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
    situacao = models.CharField(max_length=7, default="ATIVO")
    codigo_doador = models.ForeignKey(Doador, on_delete=models.CASCADE)

    