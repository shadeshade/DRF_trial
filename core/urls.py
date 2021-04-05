from django.urls import path

from core import views


urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list'})),
    path('users/<int:pk>/', views.UserViewSet.as_view({'get': 'details'})),

    path('posts/like/', views.PostViewSet.as_view({'post': 'like'})),
    path('posts/create/', views.PostViewSet.as_view({'post': 'create'})),

    path('analytics/', views.LikeViewSet.as_view({'get': 'list'})),

]
