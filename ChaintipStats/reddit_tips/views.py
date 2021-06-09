from django.http.response import HttpResponse
from django.db.models import Q, Sum, Count
from django.shortcuts import render
from .models import RedditTip

def main(request):
    all_tips = RedditTip.objects.all()

    all_stats = {}

    all_stats['total_tips'] = len(all_tips)
    all_stats['claimed_tips'] = len(all_tips.filter(claimed=True))
    all_stats['claimed_percentage'] = format(all_stats['claimed_tips'] / all_stats['total_tips'], '.2%')
    all_stats['returned_tips'] = len(all_tips.filter(returned=True))
    all_stats['returned_percentage'] = format(all_stats['returned_tips'] / all_stats['total_tips'], '.2%')
    all_stats['claim_waiting'] = all_stats['total_tips'] - (all_stats['claimed_tips'] + all_stats['returned_tips'])
    all_stats['claim_waiting_percent'] = format(all_stats['claim_waiting'] / all_stats['total_tips'], '.2%')

    all_stats['total_BCH'] = all_tips.aggregate(Sum('coin_amount'))
    all_tips_ordered = all_tips.order_by('-created_datetime')
    all_stats['start_date'] = all_tips_ordered.last().created_datetime
    top_senders = all_tips.values_list('sender').annotate(sender_count=Count('sender')).order_by('-sender_count')
    all_stats['top_senders'] = top_senders[0:16]
    all_tips_receivers = all_tips.filter(~Q(returned = True))
    top_receivers = all_tips_receivers.values_list('receiver').annotate(receiver_count=Count('receiver')).order_by('-receiver_count')
    all_stats['top_receivers'] = top_receivers[0:16]
    top_subs = all_tips.values_list('subreddit').annotate(subreddit_count=Count('subreddit')).order_by('-subreddit_count')
    all_stats['top_subs'] = top_subs[0:21]

    distinct_subs = all_tips.values_list('subreddit').distinct()
    distinct_subs = [''.join(i) for i in distinct_subs]
    all_stats['distinct_subs'] = distinct_subs
    all_stats['distinct_subs_amount'] = len(distinct_subs)

    context = {
        'all_tips':all_tips,
        'all_stats':all_stats,
    }
    return render(request, "reddit_tips/reddit_tips.html", context) 

def populate_db(request):
    from .tasks import get_tips
    get_tips()
    return HttpResponse('Testing!')
