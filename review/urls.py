from django.urls import path
from .views import  ReviewView, ReviewDetailView

urlpatterns = [
    path('' , ReviewView.as_view()),
    path('/detail/<int:review_id>', ReviewDetailView.as_view()),

]
