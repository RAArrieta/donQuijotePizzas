# Generated by Django 5.0.6 on 2024-06-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_remove_productocategoria_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Nombre'),
        ),
    ]
