# Generated by Django 5.0.6 on 2025-02-07 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_producto_precio_rec'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoinsumos',
            name='unidad',
            field=models.CharField(choices=[('Gr', 'Gr'), ('Ltr', 'Ltr'), ('Unid', 'Unid'), ('Doc', 'Doc'), ('Caja', 'Caja'), ('Lata', 'Lata'), ('Rollo', 'Rollo')], default='Gr', max_length=50),
        ),
    ]
