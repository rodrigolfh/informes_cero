from django.db import models

from django.contrib.auth.models import User

from django.db import models



class Establecimiento(models.Model): #creado directamente en admin
    establecimiento_choices = [('EST', 'Cesfam Estación'), ('BAQ', 'Cesfam Baquedano'), ('JC', 'Cesfam Joan Crawford'), ('HC', 'Cesfam Hermanos Carrera'), ('DEP', 'Departamento de Salud')]
    establecimiento = models.CharField(max_length=3, choices=establecimiento_choices)
    comuna = models.CharField(max_length=20)
    
    def __str__(self):
        return self.establecimiento
    
class Usuario(models.Model): #usuario del sistema, no un paciente
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)   
    rut = models.CharField(primary_key=True, max_length=12, unique=True) #con primary key
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=70)
    cargo_choices = [('ODO', 'Odontólogo'), ('ENC', 'Encargado de Programa en CESFAM'), ('STA', 'Estadístico'), ('ASE', 'Asesor'), ('STF', 'Staff')]
    cargo = models.CharField(max_length=3, choices=cargo_choices)
    fono = models.CharField(max_length=15)
    mail = models.EmailField(max_length=60)
    establecimiento = models.ManyToManyField(Establecimiento)
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    
    

class ArchivoInformeFormularios(models.Model):
    id_archivo_informe = models.AutoField(primary_key=True, default = 0)
    title = models.CharField(max_length=50)
    file = models.FileField() #este filefield es la ubicación
    is_validated = models.BooleanField(default=False)

class ArchivoRemDetallado(models.Model):
    id_archivo_rem = models.AutoField(primary_key=True, default=0)
    title = models.CharField(max_length=50)
    file = models.FileField() #este filefield es la ubicación
    is_validated = models.BooleanField(default=False)
    
class Paciente(models.Model): #unopor cada paciente que aparece por primera vez en el informe de formularios
    rut_sin_dv = models.CharField(max_length=12, primary_key=True, default=0)
    dv = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    fecha_nac = models.DateField(null=True)
    sexo = models.CharField(max_length=10)
    fono_1 = models.CharField(max_length=12, null=True) #fono extraido de formulario
    fono_2 = models.CharField(max_length=12, null=True) #fono extraido de formulario
    fono_3 = models.CharField(max_length=12, default='Sin Número')
    fono_4 = models.CharField(max_length=12, default='Sin Número')
    
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.DO_NOTHING) #que se actualice cada vez que aparezca en un formulario (cambios de cesfam)
    bajo_control = models.BooleanField(default = False)

class InformeFormularios(models.Model):
    informe_formularios_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, null = False)
    paciente = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING, null=False)
    fecha_formulario = models.DateField()
    riesgo_choices = [('ALTO', 'Riesgo Alto'),('BAJO', 'Riesgo Bajo')]
    riesgo = models.CharField(max_length=4, choices=riesgo_choices, null=True)
    estado_control_choices = [('ING', 'Ingreso'), ('PRI', 'Primer Control del Año')]
    estado_control = models.CharField(max_length=3, choices=estado_control_choices, null=True)
    fecha_prox_control = models.DateField(null = True) # el campo viene como datetime
    
#class RemA09Detallado(models.Model):
#    paciente = models.ForeignKey(Paciente) #en este xlsx viene el rut con DV,sin puntos ni guión
#    ceo = 0
    
    #paciente (fk)
    #mes rem a09
    #cesfam
    
    
    
    
