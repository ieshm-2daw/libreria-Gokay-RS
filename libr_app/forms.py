from django import forms

class FormBuscarLibro(forms.Form):
    consulta = forms.CharField(label="Busca un libro", max_length=125)
    tipo_filtro = forms.ChoiceField(label="Selecciona por que opción quieres filtrar:",
        choices=[
            ('titulo', 'Titulo'),
            ('autor','Autor'),
            ('editorial','Editorial')
            ],
        widget=forms.RadioSelect
        )