from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Blog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    snippet = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blogs = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]