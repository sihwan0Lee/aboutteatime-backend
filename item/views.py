import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.db.models import Q
from django.db.models import Avg

from item.models import Item

class ItemListView(View):
    def select_sort(self, sort, qs):
        if sort == 'review':
            items = list(qs.annotate(count=Count('itemreview')).order_by('-count'))
        elif sort == 'popular':
            items = list(qs.annotate(count=Count('order')).order_by('-count'))
        elif sort == 'new_arrival':
            items = list(qs.order_by('-id'))
        elif sort == 'price_desc':
            items = list(qs.order_by('-price'))
        elif sort == 'price_asc':
            items = list(qs.order_by('price'))
        return items
    
    def get_selected_items(self, sort, category, packs):
        category_q = None
        pack_q = None
        if category:
            category_q = Q(third_category__name=category) 
        else:
            category_q = Q(sub_category__name='Tea Shop')
        if packs:
            queries = [Q(title__icontains=pack) if pack != '파우더' else Q(fourth_category__name = pack) for pack in packs]
            pack_q = queries.pop()
            for each_q in queries:
                pack_q |= each_q
        else:
            pack_q = Q(sub_category__name='Tea Shop')
        return self.select_sort(sort, Item.objects.filter(category_q & pack_q))

    def get(self, request):
        ITEMS_IN_PAGE = 24
        sort = request.GET.get('sort', 'review')
        category = request.GET.get('category', None)
        packs = request.GET.getlist('pack', None)
        page = int(request.GET.get('p', '0'))
        
        items = self.get_selected_items(sort, category, packs)
        num_pages = len(items)//ITEMS_IN_PAGE + 1 if len(items)%ITEMS_IN_PAGE != 0 else len(items)//ITEMS_IN_PAGE
        item_values = []
        for i in range(ITEMS_IN_PAGE * page, ITEMS_IN_PAGE + (ITEMS_IN_PAGE * page)):
            if i > len(items) - 1:
                return JsonResponse({'items':item_values, 'num_pages':num_pages}, status=200)            
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
        return JsonResponse({'items':item_values, 'num_pages':num_pages}, status=200)

class ItemDetailView(View):
    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        label_dict = item.get_labels()
        rating = 0

        if item.itemreview_set.all():
            rating_dict = item.itemreview_set.all().aggregate(Avg('overall_rating'))
            rating = rating_dict["overall_rating__avg"]
        f_rating = f'{rating:.1f}'

        item_dict = {
            'sub_category' : item.sub_category.name,
            'fourth_category' : item.fourth_category.name,
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
            'rating' : f_rating,
            'num_reviews' : item.itemreview_set.count(),
            'main_image' : item.images.main_url
        }
        return JsonResponse({'item':item_dict}, status=200)
