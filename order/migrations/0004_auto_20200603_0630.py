# Generated by Django 3.0.6 on 2020-06-03 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200602_0413'),
        ('order', '0003_auto_20200603_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='unregistered_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.UnregisteredUser'),
        ),
    ]
