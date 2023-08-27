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
    paginate_by = 10
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        paciente_form = PacienteForm()
        context['paciente_form'] = paciente_form
        context['cesfams'] = Establecimiento.objects.all
        context['dentistas'] = Usuario.objects.all
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        ### Primero filtrar los GET que sean 'todos', para que no se busque filtrar por un cesfam 'todos', que obviamente no existe
        cesfam_filter = self.request.GET.get('cesfam_filter')
        if cesfam_filter == 'todos':
            cesfam_filter = False
        else: 
            cesfam_filter = Establecimiento.objects.get(establecimiento = cesfam_filter)
            
        dentista_filter = self.request.GET.get('dentista_filter')
            
        if dentista_filter == 'todos':
            dentista_filter = False
           
        completitud_filter = self.request.GET.get('completitud_filter')
        if completitud_filter == 'todos':
            completitud_filter == False
        
        
        riesgo_filter = self.request.GET.get('riesgo_filter')
        if riesgo_filter == 'todos':
            completitud_filter = False
        
        ### Ahora, lógica condicional para determinar el queryset de acuerdo a lo que venga en el GET
        
               
        if cesfam_filter and dentista_filter and completitud_filter and riesgo_filter:
            queryset = queryset.filter(cesfam = cesfam_filter, usuario = dentista_filter, riesgo = riesgo_filter, completo = completitud_filter)
            return queryset
        
        if cesfam_filter and dentista_filter and completitud_filter:
            queryset = queryset.filter(cesfam = cesfam_filter, usuario = dentista_filter, completo = completitud_filter)
            return queryset
        
        elif cesfam_filter and dentista_filter and riesgo_filter:
            queryset = queryset.filter(cesfam = cesfam_filter, usuario = dentista_filter, riesgo = riesgo_filter)
            return queryset
        elif cesfam_filter and completitud_filter and riesgo_filter:
            queryset = queryset.filter(cesfam = cesfam_filter, riesgo = riesgo_filter, completo = completitud_filter)
            return queryset
        
        elif dentista_filter and completitud_filter and riesgo_filter:
            queryset = queryset.filter(usuario = dentista_filter, riesgo = riesgo_filter, completo = completitud_filter)
            return queryset
        
        elif cesfam_filter and dentista_filter:
            queryset = queryset.filter(cesfam = cesfam_filter, usuario = dentista_filter)
            return queryset
        
        elif cesfam_filter and completitud_filter:
            queryset = queryset.filter(cesfam = cesfam_filter, completo = completitud_filter)
            return queryset
        
        elif dentista_filter and completitud_filter:
            queryset = queryset.filter(usuario = dentista_filter, completo = completitud_filter)
            return queryset
        
        elif cesfam_filter and riesgo_filter:
            queryset = queryset.filter(cesfam = cesfam_filter, riesgo = riesgo_filter)
            return queryset
        
        elif completitud_filter and riesgo_filter:
            queryset = queryset.filter(riesgo = riesgo_filter, completo = completitud_filter)
            return queryset
        
        elif dentista_filter and riesgo_filter:
            queryset = queryset.filter(usuario = dentista_filter, riesgo = riesgo_filter)
            return queryset
        
        
        elif cesfam_filter:
            queryset = queryset.filter(cesfam = cesfam_filter)
            return queryset
        
        elif completitud_filter:
            queryset = queryset.filter(completo = completitud_filter)
            return queryset
        
        elif dentista_filter:
            queryset = queryset.filter(usuario = dentista_filter)
            return queryset
        else:
            return queryset
        
        return queryset
        
        
    