from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    post_title = models.CharField(max_length= 200, blank = False, null = False)
    post_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post_body = models.TextField()
    post_thumbnail = models.FileField(upload_to='images/thumbnails')
    Date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post_title
        