# Generated by Django 3.0.6 on 2020-06-03 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20200603_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='final_price',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='request_message',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]