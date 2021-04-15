from django.urls import path

from core import views


urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list'})),
    path('users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve'})),

    path('posts/', views.PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('posts/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve'})),

    path('posts/<int:pk>/like/', views.PostLikeViewSet.as_view()),
    path('posts/<int:pk>/unlike/', views.PostLikeViewSet.as_view()),

    path('analytics/', views.AnalyticsViewSet.as_view()),
]
