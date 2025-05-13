from django.db import models
import uuid
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

# Create your models here.

class corredor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    rut = models.CharField(max_length=10, unique=True)
    correo = models.EmailField(max_length=255, unique=True)
    numero_contacto = models.CharField(max_length=255, null=True, blank=True)
    contrasenia = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateField(default=timezone.now)

    # Campos para recuperación de contraseña
    reset_token = models.UUIDField(default=None, null=True, blank=True)
    token_expira = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'corredor'

    def clean(self):
        # Validar que el RUT y correo sean únicos (evita registros duplicados)
        if corredor.objects.filter(rut=self.rut).exclude(pk=self.pk).exists():
            raise ValidationError({'rut': 'El RUT ya está registrado.'})
        if corredor.objects.filter(correo=self.correo).exclude(pk=self.pk).exists():
            raise ValidationError({'correo': 'El correo ya está registrado.'})

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.rut}"

    def save(self, *args, **kwargs):
        self.full_clean()
        self.contrasenia = make_password(self.contrasenia)
        super().save(*args, **kwargs)

    def generar_token(self):
        """Genera un token de recuperación y establece un tiempo de expiración."""
        self.reset_token = uuid.uuid4()
        self.token_expira = timezone.now() + timedelta(hours=1)  # Expira en 1 hora
        self.save()