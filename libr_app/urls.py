"""
URL configuration for libr_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ListarLibros.as_view(), name='listar_libros'),
    path('nuevoLibro/', NuevoLibro.as_view(), name='nuevo_libro'),
    path('detalles/<int:pk>', DetalleLibro.as_view(), name='detalle_libro'),
    path('borrar/<int:pk>', BorrarLibros.as_view(), name='borrar_libro'),
    path('editar/<int:pk>', EditarLibro.as_view(), name='editar_libro'),
    path('mislibros/', ListarPrestamos.as_view(), name='libros_usuario'),
    path('reservar/<int:pk>', ReservarLibro.as_view(), name='reservar_libro'),
    path('devolver/<int:pk>', DevolverLibro.as_view(), name='devolver_libro'),
    path('prestamo/detalles/<int:pk>', DetallesPrestamo.as_view(), name='detalle_prestamo'),
    path('resultados_busqueda/', BuscarLibros.as_view(), name='filtrar')
]


#path('reservar/<int:pk>', ReservarLibro.as_view(), name='reservar_libro'),