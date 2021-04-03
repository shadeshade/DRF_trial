from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.serializers import PostLikeSerializer, PostSerializer, UserActivitySerializer
from .models import User, Post, LastRequest


def save_activity(user):
    # try:
    #     obj = LastRequest.objects.get(user=user)
    # except LastRequest.DoesNotExist:
    #     obj = LastRequest.objects.create(user=user)
    # obj.__dict__.update(date=datetime.now())
    # obj.save()

    obj, created = LastRequest.objects.update_or_create(user=user)
    if not created:
        obj.__dict__.update(date=datetime.now())
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

    def list(self, request, *args, **kwargs):
        save_activity(request.user)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def dis_like(self, request, *args, **kwargs):
        save_activity(request.user)

        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response(serializer.data)
        return Response(data=serializer.errors)

# class CustomRegistrationView(views.RegistrationView):
#
#     def send_activation_email(self, *args, **kwargs):
#         your_custom_email_sender(*args, **kwargs)
