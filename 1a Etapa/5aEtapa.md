# 5ª Etapa: Atualizando formulário

**1.** Vá até o projeto ```Formulario``` para modificá-lo:
```
cd Formulario
```

**2.** Digite ```code .``` para abrir o Visual Studio Code.

**3.** Agora com o Visual Studio Code aberto, abra o ```forms.py```.

**4.** Em ```forms.py```, subtitua todo o código pelo que está abaixo:
``` Python
from django import forms
from django.forms import RadioSelect

   
class FormularioForm(forms.Form):
    select_choices = [
        ("", "Selecione..."),
        ("Opção 1","Opção 1"),
        ("Opção 2", "Opção 2"),
        ("Opção 3", "Opção 3")
    ]
    radio_choices = [
        ("Opção 1","Opção 1"),
        ("Opção 2", "Opção 2"),
        ("Opção 3", "Opção 3")
    ]
    text_field = forms.CharField(max_length=255, min_length=2,
                                 label = "Nome ")
    integer_field = forms.IntegerField(min_value=0, max_value=1000, label = "Idade ")
    boolean_field = forms.BooleanField(required=True, label = "Estuda? ")
    select_field = forms.ChoiceField(required=True, choices=select_choices,
                                     label = "Opções de Select ")
    radio_field = forms.ChoiceField(required=True, choices=radio_choices,
                                    label = "Opções de Radio ",
                                      widget=forms.RadioSelect)
```

**5.** Salve o projeto, rode o programa e verifique as funcionalidades:
```
python3 manage.py runserver 8080
```

Abra no navegador: http://127.0.0.1:8080
