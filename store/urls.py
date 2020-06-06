from django.urls import path
from .views import StoreListView,StoreDetailView

urlpatterns = [
    path('list', StoreListView.as_view()),
    path('detail', StoreDetailView.as_view())
]
