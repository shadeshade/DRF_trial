from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(User, blank=False, related_name='posts', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)
    # liked_by = models.ManyToManyField(User, blank=True, related_name='liked')

    # disliked_by = models.ManyToManyField(User, blank=True, related_name="disliked")

    def __str__(self):
        if len(str(self.text)) > 10:
            return f'By (id: {self.pk}) {self.author} - {self.text[:10]}...'
        return f'By (id: {self.pk}) {self.author} - {self.text}'

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class LastRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='requested_at')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ': ' + str(self.date)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    created_at = models.DateTimeField(auto_now_add=True)