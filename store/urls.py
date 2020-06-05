from django.urls import path
from .views import StoreList,StoreDetail

urlpatterns = [
    path('/list', StoreList.as_view()),
    path('/detail', StoreDetail.as_view())
]
