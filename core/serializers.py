from rest_framework import serializers

from core.models import User, Post, LastRequest


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
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        like_status = serializers.CharField(max_length=8)
        fields = ('id',)

    def save(self, request, **kwargs):
        post_id = self.initial_data['id']
        like_status = self.initial_data['like_status']
        post = Post.objects.get(id=post_id)
        user = request.user
        liked_by_user = user.liked.all()
        disliked_by_user = user.disliked.all()
        if like_status == 'liked':
            if post in liked_by_user:
                post.liked_by.remove(user)
            elif post in disliked_by_user:
                post.disliked_by.remove(user)
                post.liked_by.add(user)
            else:
                post.liked_by.add(user)
        elif like_status == 'disliked':
            if post in liked_by_user:
                post.liked_by.remove(user)
                post.disliked_by.add(user)
            elif post in disliked_by_user:
                post.disliked_by.remove(user)
            else:
                post.disliked_by.add(user)

    def validate(self, *args, **kwargs):
        like_status = self.initial_data['like_status']
        if like_status not in ['liked', 'disliked']:
            raise serializers.ValidationError("Value must be equal 'liked' or 'disliked'")
        return like_status


class LastRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastRequest
        fields = '__all__'


class UserActivitySerializer(serializers.ModelSerializer):
    last_request = LastRequestSerializer(source='requested_at', many=True)

    class Meta:
        model = User
        # last_request = ''
        fields = '__all__'
        # fields = ('id', 'last_login', )
