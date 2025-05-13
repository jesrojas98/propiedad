from django.urls import path
from . import views

app_name = 'comisiones'

urlpatterns = [
    path('', views.listado_vales_vista, name='listado_vales_vista'),
    path("listado/", views.listado_comisiones, name="listado_comisiones"),
    path('crear-comision/<int:documento_id>/', views.crear_comision, name='crear_comision'),
    path('crear_egreso/', views.crear_egreso, name='crear_egreso' ),
    path("editar/<int:comision_id>/", views.editar_comision, name="editar_comision"),
    path("eliminar/<int:comision_id>/", views.eliminar_comision, name="eliminar_comision"),

    ]