import json
from django.db import models

class Item(models.Model):
    also_viewed        = models.ManyToManyField('self', through='AlsoViewed', symmetrical=False, related_name='+')
    also_bought        = models.ManyToManyField('self', through='AlsoBought', symmetrical=False, related_name='+')
    options            = models.ManyToManyField('self', through='OptionItem', symmetrical=False, related_name='+')
    main_category      = models.ForeignKey('MainCategory', on_delete=models.SET_NULL, null=True)
    sub_category       = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)
    third_category     = models.ForeignKey('ThirdCategory', on_delete=models.SET_NULL, null=True)
    fourth_category    = models.ForeignKey('FourthCategory', on_delete=models.SET_NULL, null=True)
    content            = models.TextField(null=True) 
    detail             = models.TextField(null=True) 
    title              = models.CharField(max_length=100)
    description        = models.CharField(max_length=300)
    price              = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percent   = models.DecimalField(max_digits=4, decimal_places=3, default=1)
    labels             = models.ManyToManyField('Label', through='ItemLabel')
    benefits           = models.CharField(max_length=300, null=True)
    images             = models.OneToOneField('ItemImage', on_delete=models.SET_NULL, null=True)
    
    @property
    def points(self):
        return float(self.price) * 0.01

    def set_benefits(self, benefit_list):
        self.benefits = json.dumps(benefit_list, ensure_ascii=False)

    def get_benefits(self):
        return json.loads(self.benefits)
    
    def get_labels(self):
        labels = self.labels.values_list('name', flat=True)
        label_dict = {
            'BEST' : False,
            '선물용' : False,
            '일시품절' : False,
            'SALE' : False,
            '사은품' : False,
            'NEW' : False
        }
        if labels is None:
            return label_dict
        for label in labels:
            if label in label_dict:
                label_dict[label] = True
        return label_dict

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'items'

class ItemImage(models.Model):
    main_url    = models.URLField(max_length=3000)
    front_url   = models.URLField(max_length=3000)
    hover_url   = models.URLField(max_length=3000) 

    def __str__(self):
        return 'images for ' + self.item 

    class Meta:
        db_table = 'item_images' 
    
class ItemLabel(models.Model):
    item    = models.ForeignKey('Item', on_delete=models.CASCADE)
    label   = models.ForeignKey('Label', on_delete=models.CASCADE)

    class Meta:
        db_table = 'item_labels'

class Label(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'labels'

class AlsoViewed(models.Model):
    current     = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='+')
    viewed      = models.ForeignKey('Item', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.current + ":" + self.viewed

    class Meta:
        db_table = 'also_viewed_items'

class AlsoBought(models.Model):
    current     = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='+')
    bought      = models.ForeignKey('Item', on_delete=models.CASCADE)

    def __str__(self):
        return self.current + ":" + self.bought

    class Meta:
        db_table = 'also_bought_items'

class OptionItem(models.Model):
    current     = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='+')
    option      = models.ForeignKey('Item', on_delete=models.CASCADE)

    def __str__(self):
        return self.current + ":" + self.option

    class Meta:
        db_table = 'optional_items'

class Category(models.Model):
    name        = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class MainCategory(Category):
    class Meta:
        db_table = 'main_categories'

class SubCategory(Category):
    class Meta:
        db_table = 'sub_categories'

class ThirdCategory(Category):
    class Meta:
        db_table = 'third_categories'

class FourthCategory(Category):
    class Meta:
        db_table = 'fourth_categories'



