from django.db import models

class User(models.Model):
    realname          = models.CharField(max_length=50)
    username          = models.CharField(max_length=50, unique=True)
    birthday          = models.DateField()
    gender            = models.CharField(max_length=20) 
    service_provider  = models.CharField(max_length=30)
    phone             = models.CharField(max_length=50, unique=True)
    password          = models.CharField(max_length=2000)
    group             = models.ForeignKey('UserGroup', on_delete=models.SET_NULL, null=True)
    points_sum        = models.PositiveIntegerField(default=0)
    privacy_3rd_party = models.BooleanField(default=False) 
    privacy_foreign   = models.BooleanField(default=False) 
    point_message     = models.BooleanField(default=False)
    web_message       = models.BooleanField(default=False) 
    created_at        = models.DateField(auto_now_add=True)
    cart_coupons      = models.ManyToManyField('CartCoupon', through='UserCartCoupon')
    mobile_coupons    = models.ManyToManyField('MobileCoupon', through='UserMobileCoupon') 

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'

class UnregisteredUser(models.Model):
    recipient_ name   = models.CharField(max_length=50)
    orderer_name      = models.CharField(max_length=50)
    phone             = models.CharField(max_length=50)
    email             = models.EmailField()
    recipient_address = models.CharField(max_length=200)
    orderer_address   = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'unregistered_users'

class UserGroup(models.Model):
    name         = models.CharField(max_length=30, unique=True)
    sum_paid     = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_groups'

class UserCartCoupon(models.Model):
    user        = models.ForeignKey('User', on_delete=models.CASCADE)
    coupon      = models.ForeignKey('CartCoupon', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_cart_coupons'

class CartCoupon(models.Model):
    name        = models.CharField(max_length=50)
    discount    = models.PositiveIntegerfield()
    start_date  = models.DateField()
    expiry_date = models.DateField()
    min_order   = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cart_coupons'

class UserMobileCoupon(models.Model):
    user        = models.ForeignKey('User', on_delete=models.CASCADE)
    coupon      = models.ForeignKey('MobileCoupon', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_mobile_coupons'

class MobileCoupon(models.Model):
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
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    item    = models.ForeignKey('Item', on_delete=models.CASCADE)
    
    def __str__(self):
        return user.name + "-" + user.item

    class Meta:
        db_table = 'wishlists'
