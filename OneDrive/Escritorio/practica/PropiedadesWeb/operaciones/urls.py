from django.urls import path
from . import views

app_name = 'operaciones'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('publicaciones/filtradas/', views.publicaciones_filtradas, name='publicaciones_filtradas'),
    path('crear_publicacion/', views.crear_publicacion, name='crear_publicacion'),
    path('lista_publicaciones/', views.lista_publicaciones, name='lista_publicaciones'),
    path("editar-publicacion/<int:publicacion_id>/", views.editar_publicacion, name="editar_publicacion"),
    path("cambiar-estado/<int:publicacion_id>/", views.cambiar_estado_publicacion, name="cambiar_estado_publicacion"),
    path("destacar-publicacion/<int:publicacion_id>/", views.destacar_publicacion, name="destacar_publicacion"),
    path("detalle_publicacion/<int:id>/", views.detalle_publicacion, name="detalle_publicacion"),
    path("listado_operaciones", views.listado_operaciones, name='listado_operaciones'),
    path('crear_operacion_venta/<int:propiedad_id>', views.crear_operacion_venta, name='crear_operacion_venta'),
    path('eliminar_operacion/<int:operacion_id>', views.eliminar_operacion, name='eliminar_operacion'),
    path('credito/',views.simular_credito, name='credito'),
]
