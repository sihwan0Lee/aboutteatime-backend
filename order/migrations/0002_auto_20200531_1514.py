# Generated by Django 3.0.6 on 2020-05-31 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='add_packaging',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
