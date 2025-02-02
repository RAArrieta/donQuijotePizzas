# Generated by Django 5.0.6 on 2025-02-02 08:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gastos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.FloatField(verbose_name='Monto')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('forma_pago', models.CharField(choices=[('efectivo', 'Efectivo'), ('mercado', 'Mercado'), ('naranja', 'Naranja')], max_length=50)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.proveedores', verbose_name='Proveedor')),
            ],
        ),
    ]
