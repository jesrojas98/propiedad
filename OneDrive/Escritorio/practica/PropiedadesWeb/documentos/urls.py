# urls.py
from django.urls import path
from . import views

app_name = 'documentos'

urlpatterns = [
    path('docu_venta/<int:propiedad_id>/', views.registrar_docu_venta, name='docu_venta'),
    path('mostrar_documentos/<int:propiedad_id>/', views.documento_mostrar, name='mostrar_documentos'),
]
