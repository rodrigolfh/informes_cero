from typing import Any, Dict
from django.db.models.query import QuerySet
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
from .forms import SubirArchivoForm, PacienteForm
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
            print("----------------instancia borrada")
      
        
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


class FormulariosBajoControlListView(ListView):
    model = InformeFormularios
    template_name = 'informes/listview_formularios.html'
    #paginate_by = 10
    
    
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        paciente_form = PacienteForm()
        context['paciente_form'] = paciente_form
        context['cesfams'] = Establecimiento.objects.all
        context['dentistas'] = Usuario.objects.all
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        lookups = {}
        
        
        if 'todos' != self.request.GET.get('cesfam_filter') != None:
            cesfam_codigo = self.request.GET.get('cesfam_filter')
            cesfam_buscado = Establecimiento.objects.get(establecimiento = cesfam_codigo)
            lookups['cesfam'] = cesfam_buscado.id
            
            
        dentista_filter = self.request.GET.get('dentista_filter')
        
        if 'todos' != dentista_filter != None:
            lookups['usuario_id'] = dentista_filter
        
            
        completo = self.request.GET.get('completitud_filter')
        if 'todos' != completo != None:
            lookups['completo'] = completo
            
        riesgo = self.request.GET.get('riesgo_filter')
        if 'todos' != riesgo != None:
            lookups['riesgo'] = riesgo
        
        vigencia = self.request.GET.get('vigencia_filter')
        if 'todos' != vigencia != None:
            lookups['vigente'] = vigencia
            
        
    
                
        
        queryset = InformeFormularios.objects.filter(**lookups).order_by()
       
        
        return queryset.order_by('-tiempo_restante_real')
   
       
        
        
    