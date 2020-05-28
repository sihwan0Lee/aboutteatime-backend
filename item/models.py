import json
from django.db import models

class Item(models.Model):
    also_viewed = models.ManyToManyField('self', through='AlsoViewed', symmetrical=False)
    also_bought = models.ManyToManyField('self', through='AlsoBought', symmetrical=False)
    options     = models.ManyToManyField('self', through='OptionItem', symmetrical=False)
    main_c      = models.ForeignKey('MainCategory', on_delete=models.SET_NULL, null=True)
    sub_c       = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)
    third_c     = models.ForeignKey('ThirdCategory', on_delete=models.SET_NULL, null=True)
    fourth_c    = models.ForeignKey('FourthCategory', on_delete=models.SET_NULL, null=True)
    content     = models.TextField(null=True) # item introduction view in html
    detail      = models.Textfield(null=True) # item detailed information view in html
    title       = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price       = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    labels      = models.ManyToManyField('Label', through='Item_Label')
    benefits    = models.CharField(max_length=300)

    def set_benefits(self, benefit_list):
        self.benefits = json.dumps(benefit_list)

    def get_benefits(self):
        return json.loads(self.benefits)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'items'

class Item_Label(models.Model):
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    label = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'item_label'

class Label(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'labels'

class AlsoViewed(models.Model):
    current     = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    viewed      = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.current + ":" + self.viewed

    class Meta:
        db_table = 'also_viewed_items'

class AlsoBought(models.Model):
    current     = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    bought      = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.current + ":" + self.bought

    class Meta:
        db_table = 'also_bought_items'

class OptionItem(models.Model):
    current     = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    option      = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.current + ":" + self.option

    class Meta:
        db_table = 'optional_items'

class MainCategory(models.Model):
    name        = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'main_categories'

class SubCategory(models.Model):
    name        = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sub_categories'

class ThirdCategory(models.Model):
    name        = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'third_categories'

class FourthCategory(models.Model):
    name        = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'fourth_categories'



