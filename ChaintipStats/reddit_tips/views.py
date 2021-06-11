from django.http.response import HttpResponse
from django.db.models import Q, Sum, Count
from django.shortcuts import render
from .models import RedditTip, BCHPrice

def main(request):
    all_tips = RedditTip.objects.all()
    bch_prices = BCHPrice.objects.all().order_by('-time_dt')

    all_stats = {}

    all_stats['total_tips'] = len(all_tips)
    all_stats['claimed_tips'] = len(all_tips.filter(claimed=True))
    all_stats['claimed_percentage'] = format(all_stats['claimed_tips'] / all_stats['total_tips'], '.2%')
    all_stats['returned_tips'] = len(all_tips.filter(returned=True))
    all_stats['returned_percentage'] = format(all_stats['returned_tips'] / all_stats['total_tips'], '.2%')
    all_stats['claim_waiting'] = all_stats['total_tips'] - (all_stats['claimed_tips'] + all_stats['returned_tips'])
    all_stats['claim_waiting_percent'] = format(all_stats['claim_waiting'] / all_stats['total_tips'], '.2%')

    total_BCH = all_tips.aggregate(Sum('coin_amount'))
    all_stats['total_BCH'] = format(total_BCH['coin_amount__sum'], '.9')
    total_USD = all_tips.aggregate(Sum('fiat_value'))
    all_stats['total_USD'] = "{:.2f}".format(total_USD['fiat_value__sum'])

    all_tips_ordered = all_tips.order_by('-created_datetime')
    all_stats['start_date'] = all_tips_ordered.last().created_datetime
    all_stats['end_date'] = all_tips_ordered.first().created_datetime

    all_stats['all_senders'] = all_tips.filter(~Q(sender = " ")).values_list('sender').annotate(sender_count=Count('sender')).order_by('-sender_count')
    all_tips_receivers = all_tips.filter(~Q(returned = True))
    all_stats['all_receivers'] = all_tips_receivers.values_list('receiver').annotate(receiver_count=Count('receiver')).order_by('-receiver_count')
    all_stats['all_subs'] = all_tips.values_list('subreddit').annotate(subreddit_count=Count('subreddit')).order_by('-subreddit_count')

    all_stats['bch_price'] = bch_prices.first().price_format
    all_stats['total_USD_current'] = "{:.2f}".format(float(all_stats['total_BCH']) * all_stats['bch_price'])

    context = {
        'all_tips':all_tips,
        'all_stats':all_stats,
    }
    return render(request, "reddit_tips/reddit_tips.html", context) 

def populate_db(request):
    from .tasks import get_tips
    get_tips()
    #from .tasks import get_price
    #get_price()
    return HttpResponse('Testing!')
