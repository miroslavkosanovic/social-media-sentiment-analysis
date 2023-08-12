from django.contrib import admin
from .models import SocialMediaPost, ProcessedPost

@admin.register(SocialMediaPost)
class SocialMediaPostAdmin(admin.ModelAdmin):
    list_display = ('content', 'timestamp', 'author')
    list_filter = ('timestamp',)
    search_fields = ('content', 'author__username')

@admin.register(ProcessedPost)
class ProcessedPostAdmin(admin.ModelAdmin):
    list_display = ('social_media_post', 'sentiment_score', 'sentiment_label', 'processed_timestamp')
    list_filter = ('processed_timestamp',)
    search_fields = ('social_media_post__content', 'social_media_post__author__username')

    # Custom method for list_display
    def social_media_post(self, obj):
        return obj.social_media_post.content  # Replace 'content' with the actual field name

    social_media_post.short_description = 'Social Media Post'  # Custom column header

# Register other models here if needed
