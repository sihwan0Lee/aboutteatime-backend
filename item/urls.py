from django.urls import path

from item import views

urlpatterns = [
    path('teashop/list', views.ItemListView.as_view(), name='item-list'),
    path('teashop/detail/<int:item_id>', views.ItemDetailView.as_view(), name='item-detail')
]