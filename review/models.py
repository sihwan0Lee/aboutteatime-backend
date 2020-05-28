from django.db import models
from user.models import User
from item.models import Item
from store.models import Store

class ItemReview(models.Model):
	user				= models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	item				= models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
	packaging_rating	= models.ForeignKey('Ratings', on_delete=models.SET_NULL, null=True)
	fragrance_rating	= models.ForeignKey('Ratings', on_delete=models.SET_NULL, null=True)
	taste_rating		= models.ForeignKey('Ratings', on_delete=models.Set_NULL, null=True)
	content				= models.CharField(max_length=500)
	overall_rating		= models.DecimalField(max_degits=4, decimal_places=2)
	created_at			= models.DateTimeField(auto_now_add=True)
	modified_at			= models.DateTimeField(auto_now=True)
	liked_by			= models.ManyToManyField('User', through='ItemLike', related_name='liked_item_reviews')

	def __str__(self):
		return self.user + "-" + self.item + " review"
	
	class Meta:
		db_table = 'item_reviews'

class StoreReview(models.Model):
	user				= models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	store				= models.ForeignKey('Store', on_delete=models.SET_NULL, null=True)
	content				= models.CharField(max_length=1000)
	rating				= models.DecimalField(max_digits=2, decimal_places=1)		
	created_at			= models.DateTimeField(auto_now_add=True)
	modified_at 		= models.DateTimeField(auto_now=True)
	liked_by			= models.ManyToManyField('User', through='StoreLike', related_name='liked_store_reviews')

	def __str__(self):
		return self.user + "-" + self.store + " review"

	class Meta:
		db_table = 'store_reviews'

class ItemRevImg(models.Model):
	reivew				= models.ForeignKey('ItemReview', on_delete=models.SET_NULL, null=True, related_name='images')
	image_url			= models.CharField(max_length=3000)

	def __str__(self):
		return self.review + " image"

	class Meta:
		db_table = 'item_review_images'


class StoreRevImg(models.Model):
	review				= models.ForeignKey('StoreReview', on_delete=models.SET_NULL, null=True, related_name='images')
	image_url			= models.CharField(max_length=3000)
	
	def __str__(self):
		return self.review + " image"

	class Meta:
		db_table = 'store_review_images'


class ItemLike(models.Model):
	review				= models.ForeignKey('ItemReview', on_delete=models.SET_NULL, null=True, related_name='likes')
	user				= models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	
	def __str__(self):
		return self.review + " like"

	class Meta:
		db_table = 'item_review_likes'


class StoreLike(models.Model):
	review				= models.ForeignKey('StoreReview', on_delete=models.SET_NULL, null=True, related_name='likes')
	user				= models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	
	def __str__(self):
		return self.review + " like"

	class Meta:
		db_table = 'store_review_likes'


class Ratings(models.Model):
	name				= models.CharField(max_length=45)
	rating				= models.IntegerField()

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'ratings_conversions'
