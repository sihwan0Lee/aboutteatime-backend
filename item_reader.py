import os
import django
import csv
import sys
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aboutteatime.settings')
django.setup()

from item.models import Item, MainCategory, SubCategory, ThirdCategory, FourthCategory, Label, ItemLabel, ItemImage

CSV_PATH_PRODUCTS = '../tea_items_info3.csv'

def insert_products():
    with open(CSV_PATH_PRODUCTS) as in_file:
        
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        
        for row in data_reader:
            fourth_category = row[2]
            title = row[3]
            description = row[4]
            price = int(row[5].replace(",", ""))
            labels = row[6].replace("[", "").replace("]", "").replace("'", "").split(", ")
            benefits = row[7].replace("[", "").replace("]", "").replace("'", "").split(", ")
            main_image = row[8]
            default_image = row[9]
            hover_image = row[10]

            if fourth_category not in FourthCategory.objects.values_list('name', flat=True):
                FourthCategory.objects.create(name=fourth_category)
            
            images = ItemImage.objects.create(
                main_url = main_image,
                front_url = default_image,
                hover_url = hover_image
            )

            cur_item = Item(
                main_category = MainCategory.objects.get(name="Shop"),
                sub_category = SubCategory.objects.get(name="Tea Shop"),
                third_category = ThirdCategory.objects.get(name=row[1]),
                fourth_category = FourthCategory.objects.get(name=fourth_category),
                title = title,
                description = description,
                price = price,
                images = images
            )
            cur_item.save()
            cur_item.set_benefits(benefits)
            cur_item.save()

            if labels[0] != "":
                for each_label in labels:
                    print(each_label)
                    ItemLabel.objects.create(
                        label = Label.objects.get(name=each_label),
                        item  = cur_item
                     )

insert_products()

