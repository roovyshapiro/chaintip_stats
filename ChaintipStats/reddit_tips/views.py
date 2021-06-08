from django.http.response import HttpResponse
from django.shortcuts import render
from .models import RedditTip

def main(request):
    all_tips = RedditTip.objects.all().order_by('-created_datetime')

    all_stats = {}

    all_stats['total_tips'] = len(all_tips)
    all_stats['claimed_tips'] = len(all_tips.filter(claimed=True))
    all_stats['returned_tips'] = len(all_tips.filter(returned=True))


    context = {
        'all_tips':all_tips,
        'all_stats':all_stats,
    }
    return render(request, "reddit_tips/reddit_tips.html", context) 

def populate_db(request):
    from .tasks import get_tips
    get_tips()
    return HttpResponse('Testing!')
