import json

from django.views import View 
from django.http import JsonResponse,HttpResponse

from .models import(
        ItemReview,
        ItemReviewImage,
        Rating,
        Item
)
from order.models import Order
from aboutteatime.utils import logindecorator

class ReviewView(View):
    @logindecorator
    def post(self, request):
        data = json.loads(request.body)
        item_id_from_front = data['item_id']
        if Item.objects.filter(id=item_id_from_front).exists() and Order.objects.filter(user_id=request.user.id).exists():
            ItemReview(
                user_id        = request.user.id,
                content        = data['content'],
                item_id        = item_id_from_front,
                overall_rating = data['overall_rating'],
                ).save()
            return HttpResponse(status=200)
        return JsonResponse({'comments':list(ItemReview.objects.values())}, status=200)

    def get(self, request):
        item_id_from_front = request.GET.get('id')
        reviews = ItemReview.objects.filter(item_id=item_id_from_front)
        allreviews=[]
        for review in reviews:
            all_info={
                "username"   : review.user.username,
                "comment"    : review.content,
                "overallrate": review.overall_rating,
                "date"       : review.created_at,
                }
            allreviews.append(all_info)
        return JsonResponse({'reviews':allreviews}, status=200)

class ReviewDetailView(View):
    def get(self, request, review_id):
        review = ItemReview.objects.get(id = review_id)
        images = []
        if review.images.all():
            images = review.images.values_list('image_url', flat=True)
        desc_info={
                    "itemname"    : review.item.title,
                    "username"    : review.user.username,
                    "delivery"    : review.packaging_rating.name,
                    "fragrance"   : review.fragrance_rating.name,
                    "taste"       : review.taste_rating.name,
                    "comment"     : review.content,
                    "overallrate" : review.overall_rating,
                    "date"        : review.created_at,
                    "like"        : review.liked_by,
                    "image"       : images
        }
        return JsonResponse({'review':desc_info}, status=200) 
