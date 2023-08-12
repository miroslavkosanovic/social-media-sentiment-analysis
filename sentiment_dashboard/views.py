from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import SocialMediaPost, ProcessedPost
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
    # Retrieve data and statistics
    recent_posts = SocialMediaPost.objects.order_by('-timestamp')[:10]
    positive_posts = ProcessedPost.objects.filter(sentiment_label='Positive').count()
    negative_posts = ProcessedPost.objects.filter(sentiment_label='Negative').count()
    neutral_posts = ProcessedPost.objects.filter(sentiment_label='Neutral').count()

    context = {
        'recent_posts': recent_posts,
        'positive_posts': positive_posts,
        'negative_posts': negative_posts,
        'neutral_posts': neutral_posts,
    }
    
    return render(request, 'home.html', context)


def real_time_dashboard(request):
    return render(request, 'real_time_dashboard.html')

def data_analysis(request):
    # Retrieve and process sentiment data for analysis
    positive_posts = ProcessedPost.objects.filter(sentiment_label='Positive')
    negative_posts = ProcessedPost.objects.filter(sentiment_label='Negative')
    neutral_posts = ProcessedPost.objects.filter(sentiment_label='Neutral')

    context = {
        'positive_posts': positive_posts,
        'negative_posts': negative_posts,
        'neutral_posts': neutral_posts,
    }
    
    return render(request, 'data_analysis.html', context)

# Custom decorator to restrict access to admin users
def admin_check(user):
    return user.is_superuser

@user_passes_test(admin_check)
def admin_dashboard(request):
    # Retrieve admin-specific data
    total_users = User.objects.count()
    total_positive_posts = ProcessedPost.objects.filter(sentiment_label='Positive').count()
    total_negative_posts = ProcessedPost.objects.filter(sentiment_label='Negative').count()

    context = {
        'total_users': total_users,
        'total_positive_posts': total_positive_posts,
        'total_negative_posts': total_negative_posts,
    }

    return render(request, 'admin_dashboard.html', context)

def sentiment_data_api(request):
    # Retrieve sentiment data
    positive_posts_count = ProcessedPost.objects.filter(sentiment_label='Positive').count()
    negative_posts_count = ProcessedPost.objects.filter(sentiment_label='Negative').count()
    neutral_posts_count = ProcessedPost.objects.filter(sentiment_label='Neutral').count()

    # Serialize sentiment data as JSON
    data = {
        'positive_posts': positive_posts_count,
        'negative_posts': negative_posts_count,
        'neutral_posts': neutral_posts_count,
    }

    return JsonResponse(data)

    # Custom decorator to restrict access to admin users

@login_required
def protected_view(request):
    user = request.user  # Access the currently logged-in user

    context = {
        'user': user,
    }
    return render(request, 'protected_view.html', context)

def websocket_interaction_view(request):
    return render(request, 'websocket_interaction.html')