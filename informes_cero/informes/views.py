from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from .models import Usuario, ArchivoInformeFormularios
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import RegistrarUsuarioForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from .forms import SubirArchivoForm
from .analisis import *
from django.template import loader
import os




# Create your views here.

def index(request):
    return render(request, 'informes/index.html')



def login_view(request): #el form está directo en el template login.html
    if 'next' in request.GET:
        #si en la url está la palabra "next", generada al redirigir desde @login_required, enviar mensaje.
        messages.add_message(request, messages.INFO, 'Debe ingresar para acceder a las funcionalidades.')

    if request.method == "POST":
        username = request.POST["usuario"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            
            login(request, user)
            return HttpResponseRedirect(reverse("hola"))
        else:
            context= ["Credenciales Inválidas"]#si no lo hago como lista, itera por cada caracter del string.
            return render(request, "informes/login.html", {"messages": context})

    return render(request, "informes/login.html") #view del login


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            
            user = form.save() #guardar formulario
            

            usuario = Usuario(
                user=user,
                nombre=form.cleaned_data['nombre'],
                apellidos=form.cleaned_data['apellidos'],
                rut=form.cleaned_data['rut'],
                cargo = form.cleaned_data['cargo'],
                fono=form.cleaned_data['fono'],
                establecimiento=form.cleaned_data['establecimiento'],
                mail = form.cleaned_data['mail']
                
                
            )

            usuario.save()
            messages.success(request, 'Usuario ingresado exitosamente')
            return redirect('login')
    else:
        form = RegistrarUsuarioForm()
        
    return render(request, "informes/registro.html", {'form': form})


def hola(request):
    return render(request,"informes/hola.html")

def archivo_incorrecto(request):
    return render(request,"informes/archivo_incorrecto.html")

def logout_view(request):
    
    logout(request)
    return render(request, "informes/logout.html")





def subir_archivo(request):
    #context = {}
    if request.method == "POST":#si viene POST, es porque viene el archivo
        
        nombre_archivo = './archivos/' + str(request.FILES["file"]) #se asigna variable para revisar nombre de archivo
        nombre_archivo = os.path.normpath(nombre_archivo)
        print(nombre_archivo)
        if not nombre_archivo.lower().endswith(".xlsx"): #si no termina en .xlsx
            return HttpResponseRedirect("/informes/archivo_incorrecto.html") #redirige a este template
           
            
        form = SubirArchivoForm(request.POST, request.FILES) #se trae la instancia del formulario
        
        instance = ArchivoInformeFormularios(file=request.FILES["file"]) #se instancia un objeto Archivo
        #VALIDACIONES. Se le cargarán al sessions, para poder cargarlas al redirigir. Averiguar si existe una forma mejor.

        instance.save() #se guarda
        print("instancia archivo------------------------------------:", instance)
        archivo_df = Validar(nombre_archivo) #para vincular al archivo subido
        print("-----------------------nombre archivo:", nombre_archivo)
        informe_df = ingreso(nombre_archivo)
        print("informe_Df::::::::::::::::::::::::::::", informe_df)
        context = generar_contexto_validacion(archivo_df)
        if context['validaciones'] == False:
            instance.delete()
      
        
        #return HttpResponse(t.render(c, request), content_type="application/xhtml")
        return render(request,"informes/subir.html", {"context" : context, 'objeto_archivo' : instance})
    else:
        form = SubirArchivoForm() #formulario vacío
    return render(request, "informes/subir.html", {"form": form})

class ValidarArchivoDetailView(DetailView):
    model = ArchivoInformeFormularios
    template_name = 'informes/validado.html'

    def get_object(self):
        self.id_archivo = self.request.GET.get('id_archivo')
        #print("request-------------------------:", self.request)
        #print("request.GET.get-------------------------", self.request.GET.get)
        #print("id_archivo---------------------------------------------:", self.id_archivo)
        obj = ArchivoInformeFormularios.objects.get(id=int(self.id_archivo))
        return obj
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archivo"] = ArchivoInformeFormularios.objects.get(id=self.id_archivo)
        return context


"""
def validaciones(request):
   

    return render(request,"informes/validaciones.html")
"""