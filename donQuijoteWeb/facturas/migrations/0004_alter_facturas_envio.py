# Generated by Django 5.0.6 on 2025-03-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0003_alter_facturas_envio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturas',
            name='envio',
            field=models.BooleanField(default=False),
        ),
    ]
