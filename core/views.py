from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.serializers import LikePostSerializer, CreatePostSerializer, UserActivitySerializer, \
    ViewPostSerializer, LikeAnalyticsArgsSerializer
from .models import User, Post, Like


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {**serializer.data}
        result.pop('id')  # id is redundant when returning one object
        return Response(result)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePostSerializer
        else:
            return ViewPostSerializer


class PostLikeViewSet(CreateAPIView):
    serializer_class = LikePostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['id'] = kwargs['pk']
        return super().create(request, *args, **kwargs)


class AnalyticsViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    paginator = PageNumberPagination()
    paginator.page_size = 10

    def list(self, request, *args, **kwargs):
        serializer = LikeAnalyticsArgsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        date_from = serializer.validated_data['date_from']
        date_to = serializer.validated_data['date_to']

        base_query_set = Like.objects.filter(created_at__range=[date_from, date_to])
        total_likes = base_query_set.count()

        queryset = base_query_set\
            .annotate(day=TruncDay('created_at'))\
            .values('day')\
            .annotate(likes_count=Count('id'))\
            .order_by('day')

        page = self.paginate_queryset(queryset)
        response = self.get_paginated_response(page)
        response.data['total_likes'] = total_likes
        return response


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
