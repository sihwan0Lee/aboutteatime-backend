from django.urls import path
 
from user import views

urlpatterns = [
    path('sign-up', views.SignUpView.as_view(), name='user-signup'),
    path('sign-in', views.SignInView.as_view(), name='user-signin'),
    path('wishlist', views.WishlistView.as_view(), name='user-wishlist')
]
