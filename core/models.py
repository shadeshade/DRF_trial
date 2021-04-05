from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(User, blank=False, related_name='posts', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        s = f'By (id: {self.pk}) {self.author} - {self.text[:10]}'
        if len(str(self.text)) > 10:
            s += '...'
        return s


class LastRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='requested_at')
    date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def save_activity(user):
        obj, created = LastRequest.objects.get_or_create(user=user)
        if not created:
            obj.date = timezone.now()
            obj.save()

    def __str__(self):
        return str(self.user) + ': ' + str(self.date)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    created_at = models.DateTimeField(auto_now_add=True)