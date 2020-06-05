import json

from django.views import View
from django.http import JsonResponse
from .models import Store,StoreType

class StoreList(View):
    def get(self, request):     #그냥 데이터 전부 띄워주면 된다아님?
        stores = Store.objects.all()
        store_list=[]
        for store in stores:
            info={
                "category_id" : store.category,
                "name"     : store.name,
                "address"  : store.address,
                "contact"  : store.contact
                }
            store_list.append(info)
        return JsonResponse({'stores':store_list}, status=200)

class StoreDetail(View):
    def get(self, request):
        stores = Store.objects.all()
        store_list=[]
        for store in stores:
            info={
                "category_id"      : store.category,
                "name"          : store.name,
                "address"       : store.address,
                "contact"       : store.contact,
                "opening_hours" : store.opening_hours,
                "longitude"     : store.longitude,
                "latitude"      : store.latitude
                }
            store_list.append(info)
        return JsonResponse({'store':store_list}, status=200)    


