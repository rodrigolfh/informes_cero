from django.db import models

from django.contrib.auth.models import User

from django.db import models



class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)   
    rut = models.CharField(max_length=11, primary_key=True) #con primary key
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=70)
    cargo_choices = [('ODO', 'Odontólogo'), ('ENC', 'Encargado de Programa en CESFAM'), ('STA', 'Estadístico'), ('ASE', 'Asesor'), ('STF', 'Staff')]
    cargo = models.CharField(max_length=3, choices=cargo_choices)
    establecimiento_choices = [('EST', 'Cesfam Estación'), ('BAQ', 'Cesfam Baquedano'), ('JC', 'Cesfam Joan Crawford'), ('HC', 'Cesfam Hermanos Carrera'), ('DEP', 'Departamento de Salud')]
    establecimiento = models.CharField(max_length=3, choices=establecimiento_choices)
    fono = models.CharField(max_length=15)
    dirección = models.CharField(max_length=50)
    mail = models.EmailField(max_length=60)

