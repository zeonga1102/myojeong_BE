from django.urls import path
from wish import views

urlpatterns = [
    path('', views.WishView.as_view(), name='wish'),
    path('/list', views.WishListView.as_view, name='wish_list'),
    path('/like', views.WishLikeView.as_view(), name='like'),
]
