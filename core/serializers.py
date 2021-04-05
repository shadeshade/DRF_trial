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


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text',)

    def create(self, validated_data):
        user = self.context['request'].user
        LastRequest.save_activity(user)
        validated_data = {**validated_data, 'author': user}
        return super(PostSerializer, self).create(validated_data)


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id',)

    def save(self, request, **kwargs):
        user = request.user
        LastRequest.save_activity(user)
        post_id = self.validated_data['id']
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(post=post, liked_by=user)
        if not created:
            like.delete()

    def validate_id(self, value):
        try:
            Post.objects.get(id=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Post with such id doesn\'t exist')
        return value


class LastRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastRequest
        fields = ('date',)


class UserActivitySerializer(serializers.ModelSerializer):
    last_request = LastRequestSerializer(source='requested_at')

    class Meta:
        model = User
        fields = ('id', 'last_login', 'last_request')


class LikeAnalyticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'created_at', 'post', 'liked_by')
