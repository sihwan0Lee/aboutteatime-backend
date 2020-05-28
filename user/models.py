from django.db import models

class User(models.Model):
    realname          = models.CharField(max_length=50)
    username          = models.CharField(max_length=50, unique=True)
    birthday          = models.DateField()
    gender            = models.CharField(max_length=20) # male / female
    service_provider  = models.CharField(max_length=30)
    phone             = models.CharField(max_length=50, unique=True)
    password          = models.CharField(max_length=2000)
    group             = models.ForeignKey('UserGroup', on_delete=models.SET_NULL, null=True)
    tea_points        = models.IntegerField(default=0)
    privacy_3rd_party = models.BooleanField() # privacy policy
    privacy_foreign   = models.BooleanField() # privacy policy
    point_message     = models.BooleanField() # advertisement policy
    web_message       = models.BooleanField() # advertisement policy
    created_at        = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'

class UserGroup(models.Model):
    name         = models.CharField(max_length=30, unique=True)
    sum_paid     = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_groups'

class CartCoupon(models.Model):
    user        = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    name        = models.CharField(max_length=50)
    discount    = models.Integerfield()
    start_date  = models.DateField()
    expiry_date = models.DateField()
    min_order   = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cart_coupons'

class MobileCoupon(models.Model):
    user            = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    name            = models.CharField(max_length=50)
    serial_number   = models.CharField(max_length=200, unique=True)
    expiry_date     = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mobile_coupons'

class Address(models.Model):
    user            = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    address_name    = models.CharField(max_length=50)
    recipient_name  = models.CharField(max_length=20)
    address         = models.CharField(max_length=200)
    phone           = models.CharField(max_length=50)
    landline        = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.address_name

    class Meta:
        db_table = 'my_addresses'

class Wishlist(models.Model):
    user    = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    item    = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return user.name + "-" + user.item

    class Meta:
        db_table = 'wishlists'



