from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import OpcionOtros  # Importa el modelo donde se almacenarán las opciones

# Lista de opciones predefinidas
OPCIONES_PREDEFINIDAS = [
    "Internet", "Luz", "Agua Potable", "Alcantarillado", "Alarma",
    "Teléfono", "Riego Automático", "Portón Automático", "TV Cable",
    "Chimenea", "Calefacción", "Aire Acondicionado", "Baño Visita",
    "Hall", "Antejardín", "Patio de Servicio", "Estar de Servicio",
    "Jardín", "Despensa", "Sala Estar", "Quincho", "Lavadero Interior",
    "Lavadero Exterior", "Escritorio", "Mansarda", "Terraza",
    "Comedor Diario", "Cocina Equipada", "Cocina Amoblada",
    "Persianas", "Protecciones Ventana", "Termopaneles", "Jacuzzi",
    "Piscina"
]

# Señal que inserta las opciones automáticamente después de `migrate`
@receiver(post_migrate)
def insertar_opciones(sender, **kwargs):
    if sender.name == "propiedad":  # Asegura que solo se ejecute en la app `propiedad`
        for opcion in OPCIONES_PREDEFINIDAS:
            OpcionOtros.objects.get_or_create(nombre=opcion)
