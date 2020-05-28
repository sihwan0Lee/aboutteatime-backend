from django.db import models
from user.models import User
from item.models import Item

class Order(models.Model):
	user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	status = models.OneToOneField('OrderStatus', on_delete=models.SET_NULL, null=True)
	payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True)
	request	= models.CharField(max_length=500)
	tracking_number	= models.CharField(max_length=200)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	cash_receipt_phone = models.CharField(max_length=45, null=True, default=None)
	escrow_policy = models.BooleanField(default=False)
	items = models.ManyToManyField('Item', through='OrderItem') 

	def __str__(self):
		return self.user

	class Meta:
		db_table = 'orders'

class OrderItem(models.Model):
	order					= models.ForeignKey('Order', on_delete=models.CASCADE)
	item					= models.ForeignKey('Item', on_delete=models.CASCADE)
	quantity				= models.IntegerField()

	class Meta:
		db_table = 'order_items'

class OrderStatus(models.Model):
	status					= models.CharField(max_length=45)

	def __str__(self):
		return self.status

	class Meta:
		db_table = 'order_status'

class PaymentMethod(models.Model):
	method					= models.CharField(max_length=45)
	
	def __str__(self):
		return self.method

	class Meta:
		db_table = 'payment_methods'
