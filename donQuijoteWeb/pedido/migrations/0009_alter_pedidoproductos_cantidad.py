# Generated by Django 5.0.6 on 2024-07-08 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0008_alter_pedido_direccion_alter_pedido_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoproductos',
            name='cantidad',
            field=models.FloatField(default=1),
        ),
    ]
