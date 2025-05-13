from django.urls import path
from . import views

app_name = 'propiedad'

urlpatterns = [
    path('', views.propiedad_mostrar, name='mostrar_propiedad'),
    path('registrar/', views.propiedad_registrar, name='agregar_propiedad'),
    path('modificar/<int:id>/', views.propiedad_modificar, name='modificar_propiedad'),
    path('eliminar/<int:id>/', views.propiedad_eliminar, name='eliminar_propiedad'),
    path('descripcion/<int:id>/', views.propiedad_descripcion, name='descripcion_propiedad'),
    path('eliminar_imagenes/<int:id>/', views.propiedad_modificar, name='eliminar_imagenes'),
    path('casa/', views.propiedad_registrar_casa, name='casa'),
    path('departamento/', views.propiedad_registrar_departamento, name='departamento'),
    path('oficina/', views.propiedad_registrar_oficina, name='oficina'),
    path('local_comercial/', views.propiedad_registrar_local, name='local_comercial'),
    path('bodega/', views.propiedad_registrar_bodega, name='bodega'),
    path('industrial/', views.propiedad_registrar_industrial, name='industrial'),
    path('terreno/', views.propiedad_registrar_terreno, name='terreno'),
    path('parcela/', views.propiedad_registrar_parcela, name='parcela'),
    

]
