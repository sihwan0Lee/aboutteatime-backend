# Generated by Django 3.0.5 on 2020-06-01 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='latitude',
            field=models.DecimalField(decimal_places=8, max_digits=15),
        ),
        migrations.AlterField(
            model_name='store',
            name='longitude',
            field=models.DecimalField(decimal_places=8, max_digits=15),
        ),
    ]
