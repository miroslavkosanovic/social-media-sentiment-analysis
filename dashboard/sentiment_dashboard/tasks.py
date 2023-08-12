# sentiment_dashboard/tasks.py
import tweepy
from celery import shared_task
from .models import SocialMediaPost, ProcessedPost
from textblob import TextBlob
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from elasticsearch import Elasticsearch
from django.core.cache import cache
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

@shared_task
def collect_data_task(api_key, api_secret_key, access_token, access_token_secret, keyword):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    social_media_posts = []
    for tweet in tweepy.Cursor(api.search, q=keyword, lang='en', tweet_mode='extended').items(10):
        social_media_posts.append({
            'content': tweet.full_text,
            'timestamp': tweet.created_at,
            'author': tweet.user.screen_name,
            'platform': 'Twitter',
        })

    SocialMediaPost.objects.bulk_create([
        SocialMediaPost(**post_data) for post_data in social_media_posts
    ])

    return len(social_media_posts)

@shared_task
def sentiment_analysis(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
       
    sentiment_score = sentiment_scores['compound']
    if sentiment_score >= 0.05:
        sentiment_label = 'Positive'
    elif sentiment_score <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'
       
    return sentiment_score, sentiment_label
    ProcessedPost.objects.bulk_create(processed_posts)
    return len(processed_posts)

@shared_task
def update_dashboard_task(sentiment_label, count):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'dashboard_group',
        {
            'type': 'update.dashboard',
            'sentiment_label': sentiment_label,
            'count': count,
        }
    )
    return "Update sent"

def send_websocket_message(message_type, content):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'dashboard_group',  # Group name
        {
            'type': 'update.dashboard',
            'content': content,
        }
    )
@shared_task
def save_to_elasticsearch(post_id, sentiment_score, sentiment_label):
    es = Elasticsearch()
    doc = {
        'post_id': post_id,
        'sentiment_score': sentiment_score,
        'sentiment_label': sentiment_label,
    }
    es.index(index='sentiment_data', body=doc)

@shared_task
def cache_dashboard_data(data):
    cache.set('dashboard_data', data, timeout=3600)  # Cache for an hour
