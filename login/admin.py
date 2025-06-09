from django.contrib import admin
from .models import corredor
# Register your models here.

@admin.register(corredor)

class LoginAdmin(admin.ModelAdmin):
    list_display = ('correo', 'fecha_creacion')