from django.db import models
from user.models import User, UnregisteredUser
from item.models import Item

class Order(models.Model):
	user				= models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
	unregistered_user	= models.ForeignKey('user.UnregisteredUser', on_delete=models.CASCADE, null=True, default=None)
	status				= models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)
	payment_method		= models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True)
	request_message		= models.CharField(max_length=500, null=True)
	tracking_number		= models.CharField(max_length=100, null=True)
	final_price			= models.DecimalField(max_digits=12, decimal_places=2, null=True)
	shipping_fee		= models.PositiveIntegerField(default=2500)
	cash_receipt_phone	= models.CharField(max_length=45, null=True, default=None)
	escrow_policy		= models.BooleanField(default=False)
	items				= models.ManyToManyField('item.Item', through='OrderItem') 
	ordered_date 		= models.DateTimeField(null=True)
	total_price         = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	
	def __str__(self):
		return self.user

	class Meta:
		db_table = 'orders'

class OrderItem(models.Model):
    order	      = models.ForeignKey('Order', on_delete=models.CASCADE)
    item	      = models.ForeignKey('item.Item', on_delete=models.CASCADE)
    quantity      = models.PositiveIntegerField()
    add_bag       = models.PositiveIntegerField()
    add_packaging = models.PositiveIntegerField(default=0)

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

    def __str__(self):
        return self.method

    class Meta:
        db_table = 'payment_methods'
