from django.urls import path
from . import views

app_name = 'cliente'

urlpatterns =[
    path('add_cliente', views.Cliente_registrar, name='add_cliente'),
    path('',views.listado_cliente, name='listado_cliente'),
    path('edit_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_client/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'), 
]