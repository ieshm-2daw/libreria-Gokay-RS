from django import forms

class FormBuscarLibro(forms.Form):
    consulta = forms.CharField(label="Busca un libro", max_length=255)