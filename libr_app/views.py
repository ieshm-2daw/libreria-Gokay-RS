# Create your views here.
from typing import Any
from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
from .models import Libro


# Create your views here.


'''class ListBookView(ListView):
    model=Libro
    queryset=Libro.objects.filter(disponibilidad="DISP")
'''

class NuevoLibro(CreateView):
    model = Libro
    fields = '__all__'
    template_name = 'libr_app/nuevo_libro.html'
    success_url = reverse_lazy('listar_libros')

class ListarLibros(ListView):
    model = Libro
    template_name = 'libr_app/listar_libros.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad = 'DISP')
        context['libros_prestados'] = Libro.objects.filter(disponibilidad = 'PRES')

class BorrarLibros(DeleteView):
    model = Libro
    template_name = 'libr_app/confirmación_borrado.html'
    success_url = reverse_lazy('listar_libros')

class EditarLibro(UpdateView):
    model = Libro
    fields = '__all__'
    template_name = 'libr_app/libro_editado.html'
    success_url = reverse_lazy('listar_libros')

class DetalleLibro(DetailView):
    model = Libro
    template_name='libr_app/detalle_libro.html'