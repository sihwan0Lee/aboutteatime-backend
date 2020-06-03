from django.urls import path
from .views import ReviewWriteView, ReviewView, ReviewDetailView

urlpatterns = [
    path('/write', ReviewWriteView.as_view()),
    path('/view' , ReviewView.as_view()),
    path('/detail', ReviewDetailView.as_view()),

]
