from django.db import models
from user.models import User
from item.models import Item
from store.models import Store

class ItemReview(models.Model):
	user             = models.ForeignKey('user.User', on_delete=models.CASCADE)
	item             = models.ForeignKey('item.Item', on_delete=models.CASCADE)
	packaging_rating = models.ForeignKey('Rating', on_delete=models.SET_NULL, null=True, related_name='packaging')
	fragrance_rating = models.ForeignKey('Rating', on_delete=models.SET_NULL, null=True, related_name='fragrance')
	taste_rating     = models.ForeignKey('Rating', on_delete=models.SET_NULL, null=True, related_name='taste')
	content          = models.CharField(max_length=500)
	overall_rating   = models.DecimalField(max_digits=3, decimal_places=1)
	created_at       = models.DateTimeField(auto_now_add=True)
	modified_at      = models.DateTimeField(auto_now=True)
	liked_by         = models.ManyToManyField('user.User', through='ItemReviewLike', related_name='liked_item_reviews')

	def __str__(self):
		return self.user.username + "-" + self.item.title + " review"
	
	class Meta:
		db_table = 'item_reviews'

class StoreReview(models.Model):
	user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
	store		= models.ForeignKey('store.Store', on_delete=models.CASCADE)
	content	    = models.CharField(max_length=1000)
	rating		= models.DecimalField(max_digits=2, decimal_places=1)		
	created_at	= models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
	liked_by	= models.ManyToManyField('user.User', through='StoreReviewLike', related_name='liked_store_reviews')

	def __str__(self):
		return self.user + "-" + self.store + " review"

	class Meta:
		db_table = 'store_reviews'

class ItemReviewImage(models.Model):
	reivew = models.ForeignKey('ItemReview', on_delete=models.SET_NULL, null=True, related_name='images')
	image_url = models.URLField(max_length=3000)

	def __str__(self):
		return self.review.item.title + " image"

	class Meta:
		db_table = 'item_review_images'

class StoreReviewImage(models.Model):
	review = models.ForeignKey('StoreReview', on_delete=models.SET_NULL, null=True, related_name='images')
	image_url = models.URLField(max_length=3000)
	
	def __str__(self):
		return self.review + " image"

	class Meta:
		db_table = 'store_review_images'


class ItemReviewLike(models.Model):
	review	= models.ForeignKey('ItemReview', on_delete=models.SET_NULL, null=True, related_name='likes')
	user	= models.ForeignKey('user.User', on_delete=models.CASCADE)
	
	def __str__(self):
		return self.review + " like"

	class Meta:
		db_table = 'item_review_likes'


class StoreReviewLike(models.Model):
	review	= models.ForeignKey('StoreReview', on_delete=models.CASCADE, related_name='likes')
	user	= models.ForeignKey('user.User', on_delete=models.CASCADE)
	
	def __str__(self):
		return self.review + " like"

	class Meta:
		db_table = 'store_review_likes'


class Rating(models.Model):
	name	= models.CharField(max_length=45)
	rating	= models.IntegerField()

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'rating_conversions'
