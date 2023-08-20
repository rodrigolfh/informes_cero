from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Usuario, Paciente





class RegistrarUsuarioForm(UserCreationForm): # hereda del formulario usercreationform

    rut = forms.CharField(max_length=12)
    nombre = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=30)
    fono = forms.CharField(max_length=30)
    mail = forms.EmailField
 
    cargo_choices = [('ODO', 'Odontólogo'), ('ENC', 'Encargado de Programa en CESFAM'), ('STA', 'Estadístico'), ('ASE', 'Asesor'), ('STF', 'Staff')]
    cargo = forms.ChoiceField(choices=cargo_choices)
    
    establecimiento_choices = [('EST', 'Cesfam Estación'), ('BAQ', 'Cesfam Baquedano'), ('JC', 'Cesfam Joan Crawford'), ('HC', 'Cesfam Hermanos Carrera'), ('DEP', 'Departamento de Salud')]
    establecimiento = forms.ChoiceField(choices=establecimiento_choices)
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('rut', 'nombre', 'apellidos', 'fono')

class SubirArchivoForm(forms.Form): #formulario subida archivo
    title = forms.CharField(max_length=50)
    file = forms.FileField() #debe tener un FileField

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['fono_1', 'fono_2', 'fono_3', 'fono_4', 'establecimiento']
