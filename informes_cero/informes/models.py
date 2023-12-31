from django.db import models

from django.contrib.auth.models import User

from django.db import models

from datetime import datetime, timedelta




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
    estado_choices = [('VENC', 'Vencido'),
                      ('VHOY', 'Vence Hoy'),
                      ('V2SM', 'Vence en menos de 2 semanas'),
                      ('VMES', 'Vence en menos de un mes'),
                      ('V5SM', 'Vence en menos de 6 semanas'),
                      ('VGTE', 'Vigente')
                      ]
    estado = models.CharField(max_length=4, choices = estado_choices, default='VGTE')
    
    def edad_hoy(self):
        hoy = datetime.now().date()
        fecha_nacimiento = self.fecha_nac
    
        # Calcular la diferencia entre las fechas
        
        try:
            edad = hoy - fecha_nacimiento
    
        # Calcular años, meses y días
            años = edad.days // 365
            dias_restantes = edad.days % 365
            meses = dias_restantes // 30
            dias = dias_restantes % 30
    
        # Formatear la edad como 'AAa, MMm, DDd'
            edad_formateada = f"{años}a, {meses}m, {dias}d"
            return edad_formateada
    
        except TypeError:
            return "Faltan Datos"
    
    def __str__(self):
        
        return f"{self.nombre}, {self.rut_sin_dv}-{self.dv}, {self.establecimiento}"

class InformeFormularios(models.Model):
    informe_formularios_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, null = False)
    paciente = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING, null=False)
    cesfam = models.ForeignKey(Establecimiento, on_delete=models.DO_NOTHING)
    fecha_formulario = models.DateField()
    riesgo_choices = [('ALTO', 'Riesgo Alto'),('BAJO', 'Riesgo Bajo')]
    riesgo = models.CharField(max_length=4, choices=riesgo_choices, null=True)
    estado_control_choices = [('ING', 'Ingreso'), ('PRI', 'Primer Control del Año')]
    estado_control = models.CharField(max_length=3, choices=estado_control_choices, null=True)
    fecha_prox_control = models.DateField(null = True)
    completo = models.BooleanField(default=True)
    campos_faltantes = models.CharField(max_length=64, default="")
    prox_control_segun_riesgo = models.DateField(null = True)
    fecha_sale = models.DateField(null=True)
    vigente = models.BooleanField(default=True)
    tiempo_restante_real = models.IntegerField(null=True)
    
    @property
    def edad_form(self):
        
        try:
            fecha_form = self.fecha_formulario
            fecha_nacimiento = self.paciente.fecha_nac
    
            # Calcular la diferencia entre las fechas
            edad = fecha_form - fecha_nacimiento
    
            # Calcular años, meses y días
            años = edad.days // 365
            dias_restantes = edad.days % 365
            meses = dias_restantes // 30
            dias = dias_restantes % 30
  
    
            # Formatear la edad como 'AAa, MMm, DDd'
            edad_formateada = f"{años}a, {meses}m, {dias}d"
        
            return edad_formateada
        except TypeError:
            return "Faltan datos"
    
    @property    
    def edad_años(self):
       
        try:
            fecha_form = self.fecha_formulario
            fecha_nacimiento = self.paciente.fecha_nac
    
            # Calcular la diferencia entre las fechas
            edad = fecha_form - fecha_nacimiento
    
            # Calcular años
            años = edad.days // 365
            return años
        except TypeError:
            pass
        
    @property
    def tiempo_restante(self):
        hoy = datetime.now().date()
        
        
        tiempo_restante = self.fecha_formulario - hoy
    
       
        dias_restantes = tiempo_restante
    
        
        
        return dias_restantes.days
    

            

    """
    ======

Corresponde a los niños(as) bajo control que no acudieron a su control con odontólogo(a) en la fecha establecida y que según edad y riesgo alcanzado en el corte, su inasistencia a control supera los plazos máximos especificados a continuación    (2023-07-14 23:22:20)
- 1 a 2 años: 
  Bajo riesgo: 12 Meses de inasistencia desde el último control asistente con registro en Formulario.
  Alto riesgo: 6 Meses de inasistencia desde el último control asistente con registro en Formulario.

- 3 a 9 años:
  Bajo riesgo: 12 Meses de inasistencia desde el último control asistente con registro en Formulario.
  Alto riesgo: 4 Meses de inasistencia desde el último control asistente con registro en Formulario.
    """
    

    
    def __str__(self):
        return f"Odontólog@: {self.usuario}, Paciente: {self.paciente}, Fecha Formulario: {self.fecha_formulario}"
    
    

    
    
