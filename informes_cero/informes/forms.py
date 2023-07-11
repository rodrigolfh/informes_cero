from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Usuario





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

"""
class RegistrarUsuarioForm(forms.ModelForm):
   class Meta:
        model = Usuario
        fields = '__all__' 

class RegistrarUsuarioForm(UserCreationForm):
    rut = forms.CharField(max_length=11)
    nombres = forms.CharField(max_length=40)
    apellidos = forms.CharField(max_length=70)
    cargo = forms.ChoiceField(choices=Usuario.cargo_choices)
    establecimiento = forms.ChoiceField(choices=Usuario.establecimiento_choices)
    fono = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=60)

    class Meta:
        model = Usuario
        fields = ('rut', 'nombres', 'apellidos', 'cargo', 'establecimiento', 'fono', 'email')
"""