# Generated by Django 3.0.6 on 2020-06-01 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_auto_20200531_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='benefits',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
