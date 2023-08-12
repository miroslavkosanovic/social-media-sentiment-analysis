from django.db import models
from django.contrib.auth.models import AbstractUser

class SocialMediaPost(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField()
    author = models.CharField(max_length=100)
    platform = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.author} - {self.timestamp}"


class ProcessedPost(models.Model):
    original_post = models.ForeignKey(SocialMediaPost, on_delete=models.CASCADE)
    sentiment_score = models.FloatField()
    sentiment_label = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.original_post} - {self.sentiment_label}"

class User(models.Model):
    username = models.CharField(max_length=50)
    followers_count = models.IntegerField()
    profile_info = models.TextField()

class CacheEntry(models.Model):
    key = models.CharField(max_length=100)
    data = models.TextField()

class DashboardConfiguration(models.Model):
    keywords = models.TextField()
    refresh_interval = models.PositiveIntegerField()

class CustomUser(AbstractUser):
    # Add additional fields for user profile
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

# Replace the default User model with CustomUser
AUTH_USER_MODEL = 'sentiment_dashboard.CustomUser'
