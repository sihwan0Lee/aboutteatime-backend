# Generated by Django 3.0.6 on 2020-06-02 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20200602_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemreview',
            name='overall_rating',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]
