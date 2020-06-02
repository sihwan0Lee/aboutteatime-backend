import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.db.models import Q

from item.models import Item

class ItemListView(View):
    OFFSET_PAGE = 24

    def select_sort(self, sort, qs):
        if sort == 'review':
            items = list(qs.annotate(count=Count('itemreview_set')).order_by('count'))
        elif sort == 'popular':
            items = list(qs.annotate(count=Count('order_set')).order_by('count'))
        elif sort == 'new_arrival':
            items = list(qs.annotate(count=Count('id')).order_by('-count'))
        elif sort == 'price_desc':
            items = list(qs.annotate(count=Count('price')).order_by('count'))
        elif sort == 'price_asc':
            items = list(qs.annotate(count=Count('price')).order_by('-count'))
        return items

    def evaluate_items(self, sort, category, packs):
        items = []
        if pack[0] == 'all' and category == 'all':
            items = select_sort(sort, Item.objects.all())
            return items
        if pack[0] == 'all' and category != 'all':
            qs = Item.objects.filter(third_category__name = category)
            items = select_sort(sort, qs)
            return items
        if pack[0] != 'all' and category == 'all':
            qs = Item.objects.filter(select_pack(packs))
            items = select_sort(sort, qs)
            return items
        qs = Item.objects.filter(select_pack(packs) & Q(third_category__name = category))
        items = select_sort(sort, qs)
        return items
    
    def select_pack(self, packs):
        queries = [Q(title__icontains=pack) if pack != '파우더' else Q(fourth_category__name = pack) for pack in packs]
        query = queries.pop()
        for each_q in queries:
            query |= each_q
        return query

    def get(self, request):
        sort = request.GET.get('sort', 'review')
        category = request.GET.get('category', 'all')
        packs = request.GET.getlist('pack', ['all'])
        page = int(request.GET.get('p', '0'))

        items = self.evaluate_items(sort, category, packs)

        num_pages = len(items)/OFFSET_PAGE + 1
        item_values = []
        for i in range(OFFSET_PAGE * page, OFFSET_PAGE + (OFFSET_PAGE * page)):
            if i >= len(items):
                 return JsonResponse({'items':item_values}, status=200)            
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
