import os
import sys
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aboutteatime.settings")
django.setup()

from store.models import Store, StoreType

CSV_PATH_STORES = './output.csv'

def insert_store_type():
    with open(CSV_PATH_STORES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            store_type = row[1]

            if StoreType.objects.filter(name=store_type).exists():
                pass
            else:
                StoreType.objects.create(name=store_type)

def insert_store():
    with open(CSV_PATH_STORES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            store_type = row[1]
            print('store_type: ',store_type)
            type_id=StoreType.objects.get(name=store_type).id
            print('type_id: ',type_id)
            store_name = row[0]
            store_address = row[2]
            store_contact = row[3]
            store_open = row[4]
            store_lng = row[5]
            store_lat = row[6]
            Store.objects.create(name=store_name, address=store_address, contact=store_contact, opening_hours=store_open, longitude=store_lng, latitude=store_lat,category_id=type_id)

insert_store()                               #이거없으면 함수가 안돌아감





















# for row in data_reader:
       # print(row[0])
       # store_category = row[1]
       # Store.objects.create(name=store_category)

#        store_name = row[0]
#       # store_category = row[1]
#        store_address = row[2]
#        store_contact = row[3]
#        store_open = row[4]
#        store_lng = row[5]
#        store_lat = row[6]
#        Store.objects.create(name=store_name, address=store_address, contact=store_contact, opening_hours=store_open, longitude=store_lng,latitude=store_lat)

