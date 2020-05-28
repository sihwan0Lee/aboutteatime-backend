from django.db import models
from review.models import StoreReview

class Store(models.Model):
    type            = models.ForeignKey('StoreType', on_delete=models.SET_NULL, null=True)
    name            = models.CharField(max_length=45)
    address         = models.CharField(max_length=300)
    contact         = models.CharField(max_length=45)
    opening_hours   = models.CharField(max_length=100)
    longitude       = models.DecimalField(max_degits=10, decimal_places=8)
    latitude        = models.DecimalField(max_degits=10, decimal_places=8)


	def __str__(self):
		return self.name


    class Meta:
        db_table = 'stores'


class StoreType(models.Model):
    name            = models.CharField(max_length=45)

    class Meta:
        db_table = 'storetypes'
