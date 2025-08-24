from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=100)   # short text
    content = models.TextField()               # long text
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)  # auto timestamp

    def __str__(self):
        return self.title   # what shows up in admin/console