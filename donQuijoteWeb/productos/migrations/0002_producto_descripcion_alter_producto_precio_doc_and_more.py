# Generated by Django 5.0.6 on 2024-06-14 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_doc',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_media',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
