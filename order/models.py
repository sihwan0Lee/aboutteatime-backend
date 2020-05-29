from django.db import models
from user.models import User
from item.models import Item

class Order(models.Model):
	user				= models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	unregistered_user	= models.OneToOneField('UnregisteredUser', on_delete=models.CASCADE, default=None)
	status				= models.OneToOneField('OrderStatus', on_delete=models.SET_NULL, null=True)
	payment_method		= models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True)
	request				= models.CharField(max_length=500)
	tracking_number		= models.CharField(max_length=100)
	final_price			= models.DecimalField(max_digits=12, decimal_places=2)
	shipping_fee		= models.PositiveIntegerField(default=2500)
	cash_receipt_phone	= models.CharField(max_length=45, null=True, default=None)
	escrow_policy		= models.BooleanField(default=False)
	items				= models.ManyToManyField('Item', through='OrderItem') 
	ordered_date 		= models.DateTimeField(null=True)
	price               = models.DecimalField(max_digits=12, decimal_places=2)
	
	def __str__(self):
		return self.user

	class Meta:
		db_table = 'orders'

class OrderItem(models.Model):
	order	 = models.ForeignKey('Order', on_delete=models.CASCADE)
	item	 = models.ForeignKey('Item', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()

	class Meta:
		db_table = 'order_items'

class OrderStatus(models.Model):
	status = models.CharField(max_length=45)

	def __str__(self):
		return self.status

	class Meta:
		db_table = 'order_status'

class PaymentMethod(models.Model):
	method = models.CharField(max_length=45)
		return self.method

	class Meta:
		db_table = 'payment_methods'
