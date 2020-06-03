import json

from django.views import View             
from django.http import JsonResponse

from .models import *
from aboutteatime.utils import logindecorator

class ReviewWriteView(View):
    @logindecorator
    def post(self, request, item_id_from_front, user_id_from_front):
        if Item.objects.filter(item_id=item_id_from_front).exist() and Order.objects.filter(user_id=user_id_from_front).exist():
            data = json.loads(request.body)
            Review(
                comment   = data['content'],
                image     = data['image_url'],
                fragrance = data['fragrance_rating'],
                delivery  = data['packaging_rating'],
                flavor    = data['taste_rating'],
                rating    = data['overall_rating'],
                like      = data['liked_by']
                ).save()
     
            return HttpResponse(status=200)
    return JsonResponse({'comments':list(Review.objects.values()}, status=200)


class ReviewView(View):
    def get(self, request, item_id_from_front):
        reviews = ItemReview.objects.filter(item_id=item_id_from_front)
        allreviews=[]
        for review in reviews:
            all_info={
                "username"   : review.user.username,
                "comment"    : review.content,
                "overallrate": review.overall_rating,
                "date"       : review.created_at,
                "image"      : review.image_url
                }
            allreviews.append(all_info)
    return JsonResponse({'reviews':allreviews}, status=200)

class RiviewDetailView(View):
    def get(self, request,id_from_front):
        detailreviews = ItemReview.objects.filter(id = id_from_front)
        detail_reviews=[]
        for detailreview in detailreviews:
            desc_info={
                    "itemname"    : detailreview.item.item,
                    "username"    : detailreview.user.user,
                    "delivery"    : detailreview.packaging_rating,
                    "fragrance"   : detailreview.fragrance_rating,
                    "taste"       : detailreview.taste_rating,
                    "comment"     : detailreview.content,
                    "overallrate" : detailreview.overall_rating,
                    "date"        : detailreview.created_at,
                    "like"        : detailreview.liked_by,
                    "image"       : detailreview.image_url
                }
            detail_reviews.append(desc_info)
    return JsonResponse({'reviews':detailreviews}, status=200) 
