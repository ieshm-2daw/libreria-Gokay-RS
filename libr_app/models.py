from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Usuario(AbstractUser):
    dni = models.CharField(max_length=9, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    
    def __str__(self):
        return self.dni
    
class Libro(models.Model):
    titulo = models.CharField(max_length=120)
    autor = models.CharField(max_length=255)
    editorial = models.CharField(max_length=255)
    f_publi = models.DateField()
    genero = models.CharField(max_length=30) 