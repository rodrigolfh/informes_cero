from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegistrarUsuarioForm(UserCreationForm): # hereda del formulario
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=64)
    
    class Meta(UserCreationForm.Meta):
        model = User
  
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'group')