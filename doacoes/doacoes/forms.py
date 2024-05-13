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