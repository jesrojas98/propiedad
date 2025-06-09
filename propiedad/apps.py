from django.apps import AppConfig

class PropiedadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'propiedad'  # Nombre de la app

    def ready(self):
        import propiedad.signals  # Importa las señales para que se activen
