import json

from django.views import View
from django.http import JsonResponse
from .models import Store,StoreType

from django.core.serializers.json import DjangoJSONEncoder

class StoreList(View):
    def get(self, request):     #그냥 데이터 전부 띄워주면 된다아님?
        stores = Store.objects.all()
        store_list=[]
        for store in stores:
            info={
                "category_id" : store.category.id,
                "name"     : store.name,
                "address"  : store.address,
                "contact"  : store.contact
                }
            store_list.append(info)
        return JsonResponse({'stores':store_list}, status=200)

class StoreDetail(View):
    def get(self, request):
        store_id = request.GET.get('id')
        store = Store.objects.get(id=store_id)
        info={
            "category_id"   : store.category.id,
            "name"          : store.name,
            "address"       : store.address,
            "contact"       : store.contact,
            "opening_hours" : store.opening_hours,
            "longitude"     : store.longitude,
            "latitude"      : store.latitude
        }
        return JsonResponse({'store_info':info}, status=200)    


