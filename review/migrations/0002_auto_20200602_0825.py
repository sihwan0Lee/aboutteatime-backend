# Generated by Django 3.0.6 on 2020-06-02 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemreview',
            name='fragrance_rating',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fragrance', to='review.Rating'),
        ),
        migrations.AlterField(
            model_name='itemreview',
            name='packaging_rating',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packaging', to='review.Rating'),
        ),
        migrations.AlterField(
            model_name='itemreview',
            name='taste_rating',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taste', to='review.Rating'),
        ),
    ]