from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.Corredor_logear, name='login'),
    path('registrar/', views.Corredor_registrar, name='registrar'),
    path("solicitar_recuperacion/", views.solicitar_recuperacion, name="solicitar_recuperacion"),
    path("cambiar_contrasenia/<uuid:token>/", views.cambiar_contrasenia, name="cambia_contrasenia"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.cerrar_sesion, name='logout'),
]
