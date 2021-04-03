from django.urls import path

from core import views


urlpatterns = [
    path('users/<int:pk>/', views.UserViewSet.as_view({'get': 'details'})),
    path('users/', views.UserViewSet.as_view({'get': 'list',})),
    path('posts/', views.PostViewSet.as_view({'get': 'list', 'post': 'dis_like'})),
    path('posts/create/', views.PostViewSet.as_view({'post': 'create'})),
]

