# Generated by Django 5.0.6 on 2025-02-12 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_alter_insumos_unidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumos',
            name='unidad',
            field=models.CharField(choices=[('Kg', 'Kg'), ('Ltr', 'Ltr'), ('Unid', 'Unid'), ('Doc', 'Doc'), ('Mtr', 'Mtr')], max_length=50),
        ),
        migrations.AlterField(
            model_name='productoinsumos',
            name='unidad',
            field=models.CharField(choices=[('Gr', 'Gr'), ('Ltr', 'Ltr'), ('Unid', 'Unid'), ('Doc', 'Doc'), ('Mtr', 'Mtr')], default='Gr', max_length=50),
        ),
    ]
