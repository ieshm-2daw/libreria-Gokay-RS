from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField()
    foto = models.ImageField(upload_to='autores/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    sitio_web = models.URLField()

    def __str__(self):
        return self.nombre
    
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ManyToManyField(Autor) #N:M
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE) #N:1
    f_publi = models.DateField()
    genero = models.CharField(max_length=30)
    isbn = models.CharField(max_length=17)
    resumen = models.TextField()
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)

    D_OPC=(('DISP','Disponible'),('PRES','Prestado'),('EPDP','En proceso de préstamo'))
    disponibilidad = models.CharField(max_length=4, choices=D_OPC)

    def __str__(self):
        return self.titulo

class Usuario(AbstractUser):
    dni = models.CharField(max_length=9, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    
    def __str__(self):
        return self.username
    
class Prestamo(models.Model):
    libro_prest = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prest = models.DateField()
    fecha_devl= models.DateField(null=True, blank=True)
    usuario= models.ForeignKey(Usuario, on_delete=models.CASCADE)
    E_OPC=(('PRE','Prestado'),('DEV','Devuelto'))
    estado= models.CharField(max_length=3, choices=E_OPC)

    def __str__(self):
        return f"Prestamo de {self.libro_prest.titulo} a {self.usuario}"