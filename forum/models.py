from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    """A model class that is used for a single post"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    text = models.TextField(max_length=500)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    likes_total = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
        
    def comments_excluding_replies(self):
        return self.comments.filter(reply=None)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
        
    """A model class used for a single comment"""
    post = models.ForeignKey('forum.Post', related_name='comments', on_delete=models.CASCADE)
    reply = models.ForeignKey("Comment", null=True, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    
    """Order comments by created_date"""
    class Meta:
        ordering = ['-created_date']

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
