# Create your views here.
from datetime import date
from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import *
from django.urls import reverse_lazy
from .models import Libro, Prestamo
from .forms import FormBuscarLibro


# Create your views here.
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
        return context

class BorrarLibros(DeleteView):
    model = Libro
    template_name = 'libr_app/borrar_libro.html'
    success_url = reverse_lazy('listar_libros')

class EditarLibro(UpdateView):
    model = Libro
    fields = '__all__'
    template_name = 'libr_app/libro_editado.html'
    success_url = reverse_lazy('listar_libros')

class DetalleLibro(DetailView):
    model = Libro
    template_name='libr_app/detalle_libro.html'

class ReservarLibro(View):
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
class DevolverLibro(View):
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
    
class ListarPrestamos(ListView):
    model = Libro
    template_name = "libr_app/listar_libros_usuario.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['libros_prestados_usuario'] = Prestamo.objects.filter(usuario=self.request.user,estado="PRE")
        context['libros_devuelto_usuario'] = Prestamo.objects.filter(usuario=self.request.user,estado="DEV")
        return context
class DetallesPrestamo(DetailView):
    model=Prestamo
    template_name = "libr_app/detalle_prestamo.html"

"""class buscarLibro(View):
    def get(self, request):
        form = FormBuscarLibro()
        return render(request, 'libr_app/listar_libros.html', {'form', form})
    
    def post(self, request):
        form = FormBuscarLibro(request.POST)
        if form.is_valid():
            consulta = form.cleaned_data['consulta']
            resultados = Libro.objects.filter(titulo__icontains = consulta) | Libro.objects.filter(autor__icontains = consulta) | Libro.objects.filter(editorial__icontains = consulta)
            form.save()
            return render(request, "libr_app/filtrado.html", {'resultados':resultados, 'consulta':consulta, 'form':form})
        else:
            form = FormBuscarLibro()
        return render(request, "libr_app/filtrado.html", {'form':form})
"""

def buscar_libros(request):
    form = FormBuscarLibro(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        consulta = form.cleaned_data['consulta']
        resultados = Libro.objects.filter(titulo__icontains=consulta) | Libro.objects.filter(autor__icontains=consulta) | Libro.objects.filter(categoria__icontains=consulta)
        return render(request, 'libr_app/filtrado.html', {'resultados': resultados, 'consulta': consulta, 'form': form})
    else:
        return render(request, 'libr_app/filtrado.html', {'form': form})