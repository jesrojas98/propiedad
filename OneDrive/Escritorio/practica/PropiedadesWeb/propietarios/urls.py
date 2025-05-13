from django.urls import path
from . import views

app_name = 'propietarios'

urlpatterns = [
    path('', views.listado_propietarios, name='lista_propietarios'),
    path('registrar_propietario/', views.registrar_propietario, name='registrar_propietario'),
    path('editar_propietario/<int:id>/', views.editar_propietario, name='editar_propietario'), 
    path('eliminar_propietario/<int:id>/', views.eliminar_propietario, name='eliminar_propietario'),
]