# Generated by Django 5.0.6 on 2025-02-07 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoInsumos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField(default=1, verbose_name='Cantidad')),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.insumos', verbose_name='Insumo')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insumos', to='productos.producto', verbose_name='Producto')),
            ],
        ),
    ]
