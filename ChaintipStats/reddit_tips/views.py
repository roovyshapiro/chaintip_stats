from django.http.response import HttpResponse
from django.db.models import Q, Sum, Count
from django.shortcuts import render
from .models import RedditTip, BCHPrice
import datetime, csv
from collections import OrderedDict
from operator import getitem

def main(request):
    all_tips = RedditTip.objects.all()
    bch_prices = BCHPrice.objects.all().order_by('-time_dt')

    all_stats = {}
    all_stats['bch_price'] = bch_prices.first().price_format

    all_stats['total_tips'] = len(all_tips)
    all_stats['claimed_tips'] = len(all_tips.filter(claimed=True))
    all_stats['claimed_percentage'] = format(all_stats['claimed_tips'] / all_stats['total_tips'], '.2%')
    all_stats['returned_tips'] = len(all_tips.filter(returned=True))
    all_stats['returned_percentage'] = format(all_stats['returned_tips'] / all_stats['total_tips'], '.2%')
    all_stats['claim_waiting'] = all_stats['total_tips'] - (all_stats['claimed_tips'] + all_stats['returned_tips'])
    all_stats['claim_waiting_percent'] = format(all_stats['claim_waiting'] / all_stats['total_tips'], '.2%')
    all_stats['total_claimed_returned'] = {'Claimed':all_stats['claimed_tips'], 'Unclaimed': all_stats['claim_waiting'], 'Returned': all_stats['returned_tips'],}


    total_BCH = all_tips.aggregate(Sum('coin_amount'))
    all_stats['total_BCH'] = format(total_BCH['coin_amount__sum'], '.9')
    total_USD = all_tips.aggregate(Sum('fiat_value'))
    all_stats['total_USD'] = "{:.2f}".format(total_USD['fiat_value__sum'])

    all_tips_ordered = all_tips.order_by('-created_datetime')
    all_stats['start_date'] = all_tips_ordered.last().created_datetime
    all_stats['end_date'] = all_tips_ordered.first().created_datetime

    all_stats['all_senders'] = all_tips.filter(~Q(sender = " ")).values_list('sender').annotate(sender_count=Count('sender')).order_by('-sender_count')
    #Organize senders by total value tipped
    sender_amount = {}
    for sender, count in all_stats['all_senders']:
        sender_amount[sender] = {'bch':0,'usd':0,'usd_current':0}
        for tip in all_tips:
            if tip.sender == sender:
                sender_amount[sender]['bch'] += float(tip.coin_amount)
                sender_amount[sender]['usd'] += float(tip.fiat_value)
        sender_amount[sender]['bch'] = "{0:.8f}".format(sender_amount[sender]['bch'])
        sender_amount[sender]['usd'] = "{0:.2f}".format(sender_amount[sender]['usd'])
        sender_amount[sender]['usd_current'] = "{0:.2f}".format(float(sender_amount[sender]['bch']) * all_stats['bch_price'])
    #https://www.geeksforgeeks.org/python-sort-nested-dictionary-by-key/
    #Sorting nested dictionary by key so that the user with the highest 'bch' value ends up first
    sorted_sender_amount = OrderedDict(sorted(sender_amount.items(), key = lambda x: getitem(x[1], 'bch'), reverse=True))

    all_stats['sender_amount'] = sorted_sender_amount

    all_tips_receivers = all_tips.filter(~Q(returned = True))
    all_stats['all_receivers'] = all_tips_receivers.values_list('receiver').annotate(receiver_count=Count('receiver')).order_by('-receiver_count')
    all_stats['all_subs'] = all_tips.values_list('subreddit').annotate(subreddit_count=Count('subreddit')).order_by('-subreddit_count')

    all_stats['total_USD_current'] = "{:.2f}".format(float(all_stats['total_BCH']) * all_stats['bch_price'])

    all_stats['tip_per_day_result'] = tip_per_day(all_tips.order_by('created_datetime'))
    all_stats['value_per_day_result'] = tip_per_day(all_tips.order_by('created_datetime'), tip_value=True)

    context = {
        'all_tips':all_tips,
        'all_stats':all_stats,
    }
    return render(request, "reddit_tips/reddit_tips.html", context) 



def tip_per_day(all_tips, tip_value=False):
    '''
    Prepares a dict of # of tips per day
    '''
    start = all_tips.first().created_datetime
    end =  all_tips.last().created_datetime

    #Makes a list of all days in the range of the beginning and end of the available days in db
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days + 1)]
    #Convert the list into a dict where each key is the date without hour, minute, second and
    #each value is 0
    date_generated_dict = {i.replace(hour=0, minute =0, second = 0).strftime('%Y-%m-%d'):0 for i in date_generated}

    for tip in all_tips:
        tip_date = tip.created_datetime.replace(hour=0, minute=0, second=0).strftime('%Y-%m-%d')
        if tip_date in date_generated_dict:
            if tip_value:
                date_generated_dict[tip_date] += round(tip.fiat_value, 2)
            else:
                date_generated_dict[tip_date] += 1

    return date_generated_dict


def export_csv_all_tips(request):
    all_tips = RedditTip.objects.all().values_list('blockchain_tx', 'coin_amount', 'coin_type','fiat_type','fiat_value','receiver','sender','body_text','created_datetime','created_utc','comment_id','permalink','parent_id','parent_comment_permalink','score','subreddit','claimed','returned',)

    response = HttpResponse(content_type='test/csv')

    csv_writer = csv.writer(response)
    csv_writer.writerow(['blockchain_tx', 'coin_amount', 'coin_type','fiat_type','fiat_value','receiver','sender','body_text','created_datetime','created_utc','comment_id','permalink','parent_id','parent_comment_permalink','score','subreddit','claimed','returned',])

    for tip in all_tips:
        csv_writer.writerow(tip)
    response['Content-Disposition'] = 'attachment; filename="tips.csv"'

    return response


def populate_db(request):
    from .tasks import get_tips
    get_tips()
    #from .tasks import get_price
    #get_price()
    return HttpResponse('Testing!')