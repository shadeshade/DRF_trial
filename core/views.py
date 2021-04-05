from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from djoser.conf import settings
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.serializers import PostLikeSerializer, PostSerializer, UserActivitySerializer, LikeAnalyticsSerializer
from .models import User, Post, Like


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def details(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = settings.PERMISSIONS.user

    def like(self, request, *args, **kwargs):
        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeAnalyticsSerializer
    permission_classes = [IsAdminUser]
    paginator = PageNumberPagination()
    paginator.page_size = 10

    def list(self, request, *args, **kwargs):
        try:
            date_from = request.query_params['date_from']
            date_to = request.query_params['date_to']
            self.queryset = Like.objects.filter(created_at__range=[date_from, date_to])
        except MultiValueDictKeyError:
            return Response({'error': 'Expected "date_from" and "date_to" get parameters'},
                            status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as err:
            return Response({'error': err.args}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        currentUserModel = get_user_model()
        user = currentUserModel.objects.get(username=request.data['username'])
        update_last_login(None, user)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
