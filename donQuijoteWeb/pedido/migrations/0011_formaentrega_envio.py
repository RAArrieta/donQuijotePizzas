# Generated by Django 5.0.6 on 2024-07-24 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0010_formaentrega_alter_pedido_forma_entrega'),
    ]

    operations = [
        migrations.AddField(
            model_name='formaentrega',
            name='envio',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
