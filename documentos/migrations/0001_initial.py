# Generated by Django 5.0.1 on 2025-06-24 22:11

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('propiedad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_documento', models.CharField(max_length=255)),
                ('pdf_documento', models.FileField(blank=True, null=True, upload_to='documentos/docu_venta/')),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('id_propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='propiedad.propiedad')),
            ],
        ),
    ]
