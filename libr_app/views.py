# Create your views here.
from datetime import date
from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Libro, Prestamo
from .forms import FormBuscarLibro


# Create your views here.

class NuevoLibro(LoginRequiredMixin, CreateView):
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
        return context

class BorrarLibros(LoginRequiredMixin,DeleteView):
    model = Libro
    template_name = 'libr_app/borrar_libro.html'
    success_url = reverse_lazy('listar_libros')

class EditarLibro(LoginRequiredMixin, UpdateView):
    model = Libro
    fields = '__all__'
    template_name = 'libr_app/libro_editado.html'
    success_url = reverse_lazy('listar_libros')

class DetalleLibro(DetailView):
    model = Libro
    template_name='libr_app/detalle_libro.html'

class ReservarLibro(LoginRequiredMixin, View):
    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        return render(request, 'libr_app/reserva_libro.html', {"libro":libro})
    def post(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        libro.disponibilidad = "PRES"
        libro.save()

        Prestamo.objects.create(
            libro_prest = libro,
            fecha_prest = date.today(),
            usuario = request.user,
            estado = "PRE"

        )
        return redirect('listar_libros')
class DevolverLibro(LoginRequiredMixin, View):
    def get(self, request, pk):
        libro_prestado = get_object_or_404(Libro, pk=pk, disponibilidad="PRES")
        prestamo = Prestamo.objects.filter(libro_prest = libro_prestado,usuario=request.user, estado = "PRE")
        return render(request, 'libr_app/devolver_libro.html', {"prestamo":prestamo})
    def post(self, request, pk):
        libro_prestado = get_object_or_404(Libro, pk=pk, disponibilidad="PRES")
        prestamo = Prestamo.objects.filter(libro_prest = libro_prestado,usuario=request.user, estado = "PRE").first()
        prestamo.estado = "DEV"
        prestamo.fecha_devl = date.today()
        prestamo.save()
        libro_prestado.disponibilidad="DISP"
        libro_prestado.save()

        return redirect('listar_libros')
    
class ListarPrestamos(LoginRequiredMixin, ListView):
    model = Libro
    template_name = "libr_app/listar_libros_usuario.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['libros_prestados_usuario'] = Prestamo.objects.filter(usuario=self.request.user,estado="PRE")
        context['libros_devuelto_usuario'] = Prestamo.objects.filter(usuario=self.request.user,estado="DEV")
        return context
class DetallesPrestamo(LoginRequiredMixin, DetailView):
    model=Prestamo
    template_name = "libr_app/detalle_prestamo.html"

""" En funcion, objetivo, hacerlo en clase
def buscar_libros(request):
    if request.method == 'POST':
        form = FormBuscarLibro(request.POST)
        if form.is_valid():
            consulta = form.cleaned_data['consulta']
            libros_encontrados = Libro.objects.filter(titulo__icontains=consulta)  
            return render(request, 'libr_app/filtrado.html', {'form': form, 'libros_encontrados': libros_encontrados})
    else:
        form = FormBuscarLibro()

    return render(request, 'libr_app/filtrado.html', {'form': form})
"""

class BuscarLibros(FormView):
    template_name = 'libr_app/filtrado.html'
    form_class = FormBuscarLibro

    def form_valid(self, form):
        consulta = form.cleaned_data['consulta']
        tipo_filtro = form.cleaned_data['tipo_filtro']

        if tipo_filtro == 'titulo':
            libros_encontrados = Libro.objects.filter(titulo__icontains=consulta)
        elif tipo_filtro == 'autor':
            libros_encontrados = Libro.objects.filter(autor__nombre__icontains=consulta)
        elif tipo_filtro == 'editorial':
            libros_encontrados = Libro.objects.filter(editorial__nombre__icontains=consulta)
        else:
            libros_encontrados = []

        return self.render_to_response({'form': form, 'libros_encontrados': libros_encontrados})

    def form_invalid(self, form):
        return self.render_to_response({'form': form})

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response({'form': form})
    