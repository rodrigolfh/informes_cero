from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", views.index, name = "index"),
    path("registro", views.registrar_usuario, name='registro'),
    path("login", views.login_view, name='login'),
    path("login/", RedirectView.as_view(pattern_name='login', permanent=True)),
    path("hola", views.hola, name="hola"),
    path("logout", views.logout_view, name="logout"),
    path("informes/subir.html", views.subir_archivo, name="subir" ),
    path("informes/subir_exito.html", views.subir_exito, name="subir_exito" )
]