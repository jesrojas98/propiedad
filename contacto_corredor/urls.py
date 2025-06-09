from django.urls import path
from . import views

app_name = 'contacto_corredor'

urlpatterns = [
    path('', views.contactos_a_corredor, name='contactos_a_corredor'),
    path('contactar_corredor/', views.contactar_corredor, name='contactar_corredor'),
    path('detalle_contacto/<int:id>/<str:tipo_contacto>/', views.detalle_contacto, name='detalle_contacto'),
    path('contacto_interesado/<int:publicacion_id>/', views.contacto_interesado_view, name='contacto_interesado'),
]
