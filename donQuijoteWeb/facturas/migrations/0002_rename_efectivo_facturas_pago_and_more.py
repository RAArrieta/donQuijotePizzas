# Generated by Django 5.0.6 on 2024-08-16 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facturas',
            old_name='efectivo',
            new_name='pago',
        ),
        migrations.RemoveField(
            model_name='facturas',
            name='mercado',
        ),
        migrations.RemoveField(
            model_name='facturas',
            name='naranja',
        ),
    ]
