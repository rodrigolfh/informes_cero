from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Usuario)
# Register your models here.
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = "usuario"


# Define a new User admin
class CustomizedUserAdmin(UserAdmin):
    inlines = (UsuarioInline,)


# Re-register UserAdmin

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)