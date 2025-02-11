# Generated by Django 5.0.6 on 2025-02-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_alter_insumos_unidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumos',
            name='unidad',
            field=models.CharField(choices=[('Kg', 'Kg'), ('Ltr', 'Ltr'), ('Unid', 'Unid'), ('Doc', 'Doc'), ('Caja', 'Caja'), ('Pack', 'Pack'), ('Lata', 'Lata'), ('Rollo', 'Rollo')], max_length=50),
        ),
    ]
