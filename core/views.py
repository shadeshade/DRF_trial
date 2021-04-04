from time import strptime

from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from djoser.conf import settings

from core.serializers import PostLikeSerializer, PostSerializer, UserActivitySerializer, LikeAnalyticsSerializer
from .models import User, Post, LastRequest, Like


def save_activity(user):
    obj, created = LastRequest.objects.get_or_create(user=user)
    if not created:
        obj.date = timezone.now()
        # obj.__dict__.update(date=datetime.now())
        obj.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [AllowAny]

    # filter_backends = [SearchFilter]
    # search_fields = ['']
    def list(self, request, *args, **kwargs):
        save_activity(request.user)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def details(self, request, *args, **kwargs):
        save_activity(request.user)

        queryset = self.get_queryset().filter(id=kwargs['pk'])
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # login(request, user)
    #
    # AllLogin.objects.create(user=request.user)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = settings.PERMISSIONS.user

    def like(self, request, *args, **kwargs):
        save_activity(request.user)

        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeAnalyticsSerializer

    def list(self, request, *args, **kwargs):
        try:
            date_from = request.query_params['date_from']
            date_to = request.query_params['date_to']
            strptime(date_from, '%Y-%m-%d')
            strptime(date_to, '%Y-%m-%d')
            self.queryset = Like.objects.filter(created_at__range=[date_from, date_to])
        except MultiValueDictKeyError:
            return Response({'error': 'Expected "date_from" and "date_to" get parameters'},
                            status=status.HTTP_400_BAD_REQUEST)
        except ValueError as err:
            return Response({'error': err.args}, status=status.HTTP_400_BAD_REQUEST)
        result = super(LikeViewSet, self).list(request, *args, **kwargs)
        result.data.append({'total': len(result.data)})
        return result