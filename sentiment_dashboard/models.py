from django.db import models

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
    processed_timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.original_post} - {self.sentiment_label}"

class CacheEntry(models.Model):
    key = models.CharField(max_length=100)
    data = models.TextField()

class DashboardConfiguration(models.Model):
    keywords = models.TextField()
    refresh_interval = models.PositiveIntegerField()
