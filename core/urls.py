from django.urls import path

from core.views import UserListAPIView

urlpatterns = [
    # Users
    path('users/', UserListAPIView.as_view(), name='user-list'),

]
