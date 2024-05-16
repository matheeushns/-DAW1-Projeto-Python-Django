from django import forms
from .models import Doador, TipoSanguineo, RH, Doacao
from django.core.validators import RegexValidator, MinValueValidator
from django.forms.widgets import RadioSelect
import datetime
from django.utils import timezone

class DoadorForm(forms.ModelForm):
    class Meta:
        model = Doador
        exclude = ['situacao','tipo_rh_corretos']
        fields = '__all__'

    nome = forms.CharField(min_length=2,
                           label='NOME',
                           validators=[RegexValidator(r'^[A-Za-zÀ-ÖØ-öø-ÿÇç\s]*$', message='Nome deve conter apenas letras.')],
                           error_messages={
                               'required': 'Por favor, informe um nome.',
                               'invalid': 'Nome inválido. Por favor, use apenas letras.',
                               'min_length': 'O nome não pode ter menos de 2 caracteres.'})


    cpf = forms.CharField(min_length=11,
                          max_length=11,
                          label='CPF',validators=[RegexValidator(r'^[0-9]*$', message='CPF deve conter apenas números.')],
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