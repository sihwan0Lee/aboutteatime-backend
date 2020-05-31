import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Count

from item.models import Item

class ItemListView(View):
    def get(self, request):
        sort = request.GET.get('sort', 'review')
        page = request.GET.get('p', '0')

        if sort == 'review':
            items = list(Item.objects.annotate(count=Count('itemreview_set')).order_by('count'))
        elif sort == 'popular':
            items = list(Item.objects.annotate(count=Count('order_set')).order_by('count'))
        elif sort == 'new_arrival':
            items = list(Item.objects.annotate(count=Count('-id')).order_by('count'))
        elif sort == 'price_desc':
            items = list(Item.objects.annotate(count=Count('-price')).order_by('count'))
        elif sort == 'price_asc':
            items = list(Item.objects.annotate(count=Count('price')).order_by('count'))

        item_values = []
        for i in range(24*int(page), 24+(24*int(page))):
            if i >= len(items):
                 break            
            label_dict = items[i].get_labels()
            item = {
                 'id' : items[i].id,
                 'title' : items[i].title,
                 'price' : items[i].price,
                 'discount_percent' : items[i].discount_percent,
                 'num_reviews' : items[i].itemreview_set.count(),
                 'num_wishlist' : items[i].wishlisted_users.count(),
                 'best' : label_dict['BEST'],
                 'gift' : label_dict['선물용'],
                 'sold_out' : label_dict['일시품절'],
                 'on_sale' : label_dict['SALE'],
                 'bonus' : label_dict['사은품'],
                 'new' : label_dict['NEW'],
                 'front' : items[i].images.front_url,
                 'hover' : items[i].images.hover_url,
            }
            item_values.append(item)
        return JsonResponse({'items':item_values}, status=200)

class ItemDetailView(View):
    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        label_dict = item.get_labels()
        item_dict = {
            'sub_category' : item.sub_category,
            'fourth_category' : item.fourth_category,
            'title' : item.title,
            'description' : item.description,
            'price' : item.price,
            'discount_percent' : item.discount_percent,
            'best' : label_dict['BEST'],
            'gift' : label_dict['선물용'],
            'sold_out' : label_dict['일시품절'],
            'on_sale' : label_dict['SALE'],
            'bonus' : label_dict['사은품'],
            'new' : label_dict['NEW'],
            'benefits' : item.get_benefits(),
            'rating' : item.itemreview_set.all().aggregate(Avg('overall_rating')),
            'num_reviews' : item.itemreview_set.count() ,
            'main_image' : item.images.main_url
        }
        return JsonResponse({'item':item_dict}, status=200)
