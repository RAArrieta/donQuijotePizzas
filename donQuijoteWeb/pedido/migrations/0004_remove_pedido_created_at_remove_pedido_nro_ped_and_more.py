# Generated by Django 5.0.6 on 2024-06-26 20:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0003_rename_pedido_id_pedidoproductos_pedido_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='nro_ped',
        ),
        migrations.AddField(
            model_name='pedido',
            name='direccion',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('Entregado', 'Entregado'), ('Pendiente', 'Pendiente'), ('Cancelado', 'Cancelado')], default='Pendiente', max_length=10),
        ),
        migrations.AddField(
            model_name='pedido',
            name='hora',
            field=models.TimeField(default=django.utils.timezone.now, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='observacion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='pago',
            field=models.CharField(choices=[('Efectivo', 'EFT'), ('Mercado', 'MP'), ('Naranja', 'NRJ'), ('Debito', 'DEBIT'), ('Cobrar', 'COBRAR')], default='Cobrar', max_length=10),
        ),
    ]