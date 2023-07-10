from django.db import models
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
class RegistrarUsuarioForm(UserCreationForm): # hereda del formulario UserCreationForm. Este
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=64) #sólo se definen algunos campos
  
    class Meta(UserCreationForm.Meta): #con Meta se define cuáles se mostrarán
        model = User
  
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')