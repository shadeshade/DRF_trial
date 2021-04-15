from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from core.models import User, Post, LastRequest, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text',)

    def to_representation(self, instance):
        return {'id': instance.id}

    def create(self, validated_data):
        user = self.context['request'].user
        LastRequest.save_activity(user)
        validated_data = {**validated_data, 'author': user}
        return super(CreatePostSerializer, self).create(validated_data)


class ViewPostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author_id', 'text', 'likes_count', 'date_posted')

    def get_likes_count(self, instance):
        return instance.likes.count()


class LikePostSerializer(serializers.ModelSerializer):
    UNLIKE_PATH_STR = 'unlike'

    id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id',)

    def to_representation(self, instance):
        return {}

    def save(self, **kwargs):
        request = self.context['request']
        is_unlike_request = self.UNLIKE_PATH_STR in request.path

        user = request.user
        LastRequest.save_activity(user)
        post_id = self.validated_data['id']
        post = Post.objects.get(id=post_id)

        try:
            like = Like.objects.get(post=post, liked_by=user)
        except Like.DoesNotExist:
            like = None

        if is_unlike_request and like:
            like.delete()
        elif not is_unlike_request and not like:
            Like.objects.create(post=post, liked_by=user)

    def validate_id(self, value):
        try:
            Post.objects.get(id=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Post with such id doesn\'t exist')
        return value


class UserActivitySerializer(serializers.ModelSerializer):
    last_request = serializers.DateTimeField(source='requested_at.date')

    class Meta:
        model = User
        fields = ('id', 'last_login', 'last_request')


class LikeAnalyticsArgsSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=True)
    date_to = serializers.DateField(required=True)
