# Generated by Django 5.0.6 on 2024-07-02 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0007_pedido_forma_entrega_alter_pedido_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='direccion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('entregado', 'Entregado'), ('pendiente', 'Pendiente'), ('cancelado', 'Cancelado')], max_length=10),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='forma_entrega',
            field=models.CharField(choices=[('retira', 'Retira'), ('envio', 'Envio')], max_length=10),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='pago',
            field=models.CharField(choices=[('efectivo', 'EFT'), ('mercado', 'MP'), ('naranja', 'NRJ'), ('debito', 'DEBIT'), ('cobrar', 'COBRAR')], max_length=10),
        ),
    ]