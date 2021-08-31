from django.http.response import HttpResponse
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.shortcuts import render
from .models import RedditTip, BCHPrice
import datetime, csv, calendar
from collections import OrderedDict
from operator import getitem

def main(request):

    all_stats = {}
    month_stats = {}

    date_request = request.GET.get('date_start')
    today, end_of_day, first_of_week, end_of_week, first_of_month, end_of_month = retrieve_dates(date_request)
    all_stats['today'] = today.strftime('%A, %B %d %Y')
    all_tips = RedditTip.objects.all()
    bch_prices = BCHPrice.objects.all().order_by('-time_dt')

    all_stats['bch_price'] = bch_prices.first().price_format
    all_stats['total_tips'] = len(all_tips)
    all_stats['sent_tips'] = len(all_tips.filter(status='sent'))
    all_stats['sent_percentage'] = str(round(float(format(all_stats['sent_tips'] / all_stats['total_tips'], '.2%').replace('%','')))) + '%'
    all_stats['claimed_tips'] = len(all_tips.filter(status='claimed'))
    all_stats['claimed_percentage'] = str(round(float(format(all_stats['claimed_tips'] / all_stats['total_tips'], '.2%').replace('%','')))) + '%'
    all_stats['returned_tips'] = len(all_tips.filter(status='returned'))
    all_stats['returned_percentage'] = str(round(float(format(all_stats['returned_tips'] / all_stats['total_tips'], '.2%').replace('%','')))) + '%'
    all_stats['claim_waiting'] = len(all_tips.filter(status='unclaimed'))
    all_stats['claim_waiting_percent'] = str(round(float(format(all_stats['claim_waiting'] / all_stats['total_tips'], '.2%').replace('%','')))) + '%'
    all_stats['total_claimed_returned'] = {'Sent': all_stats['sent_tips'], 'Claimed':all_stats['claimed_tips'], 'Unclaimed': all_stats['claim_waiting'], 'Returned': all_stats['returned_tips'],}

    total_BCH = all_tips.aggregate(Sum('coin_amount'))
    all_stats['total_BCH'] = total_BCH['coin_amount__sum']
    total_USD = all_tips.aggregate(Sum('fiat_value'))
    all_stats['total_USD'] = total_USD['fiat_value__sum']

    all_tips_ordered = all_tips.order_by('-created_datetime')
    all_stats['start_date'] = all_tips_ordered.last().created_datetime
    all_stats['end_date'] = all_tips_ordered.first().created_datetime
    #Min Max Values for Date Picker 
    first_tip = all_tips_ordered.last().created_datetime
    all_stats['first_tip_date'] = first_tip.strftime('%Y-%m')
    all_stats['last_tip_date'] = timezone.now().strftime('%Y-%m')

    all_stats['all_senders'] = all_tips.filter(~Q(sender = " ")).values_list('sender').annotate(sender_count=Count('sender')).order_by('-sender_count')
    #Organize senders by total value tipped
    sender_amount = {}
    for sender, count in all_stats['all_senders']:
        sender_amount[sender] = {'bch':0,'usd':0,'usd_current':0}
        for tip in all_tips:
            if tip.sender == sender:
                sender_amount[sender]['bch'] += float(tip.coin_amount)
                sender_amount[sender]['usd'] += float(tip.fiat_value)
        sender_amount[sender]['usd_current'] = float(sender_amount[sender]['bch']) * all_stats['bch_price']
    #https://www.geeksforgeeks.org/python-sort-nested-dictionary-by-key/
    #Sorting nested dictionary by key so that the user with the highest 'bch' value ends up first
    sorted_sender_amount = OrderedDict(sorted(sender_amount.items(), key = lambda x: getitem(x[1], 'bch'), reverse=True))
    all_stats['sender_amount'] = sorted_sender_amount

    all_stats['senders_by_subs'] = sender_subreddits(all_stats['all_senders'], all_tips)

    all_tips_receivers = all_tips.filter(~Q(status = 'returned'))
    all_stats['all_receivers'] = all_tips_receivers.values_list('receiver').annotate(receiver_count=Count('receiver')).order_by('-receiver_count')
    all_stats['all_subs'] = all_tips.values_list('subreddit').annotate(subreddit_count=Count('subreddit')).order_by('-subreddit_count')

    all_stats['total_USD_current'] = "{:.2f}".format(float(all_stats['total_BCH']) * all_stats['bch_price'])

    all_stats['tip_per_day_result'] = tip_per_day(all_tips.order_by('created_datetime'))
    all_stats['value_per_day_result'] = tip_per_day(all_tips.order_by('created_datetime'), tip_value=True)
    all_stats['tip_value_per_month_result'] = tip_per_month(all_tips)

    #MONTH SPECIFIC DATA
    month_stats['today'] = today.strftime('%A, %B %d %Y')
    month_stats['month'] = today.strftime('%B %Y')
    all_month_tips = all_tips.filter(created_datetime__gte=first_of_month, created_datetime__lte=end_of_month).order_by('-created_datetime')
    
    month_stats['bch_price'] = bch_prices.first().price_format
    month_stats['total_tips'] = len(all_month_tips)
    month_stats['sent_tips'] = len(all_month_tips.filter(status='sent'))
    month_stats['claimed_tips'] = len(all_month_tips.filter(status='claimed'))
    try:
        month_stats['sent_percentage'] = str(round(float(format(month_stats['sent_tips'] / month_stats['total_tips'], '.2%').replace('%','')))) + '%'
    except ZeroDivisionError:
        #first of the month with no tips yet
        month_stats['sent_percentage'] = '0%'
    try:
        month_stats['claimed_percentage'] = str(round(float(format(month_stats['claimed_tips'] / month_stats['total_tips'], '.2%').replace('%','')))) + '%'
    except ZeroDivisionError:
        #first of the month with no tips yet
        month_stats['claimed_percentage'] = '0%'
    month_stats['returned_tips'] = len(all_month_tips.filter(status='returned'))
    try:
        month_stats['returned_percentage'] = str(round(float(format(month_stats['returned_tips'] / month_stats['total_tips'], '.2%').replace('%','')))) + '%'
    except ZeroDivisionError:
        #first of the month with no tips yet
        month_stats['claimed_percentage'] = '0%'
    month_stats['claim_waiting'] = len(all_month_tips.filter(status='unclaimed'))
    try:
        month_stats['claim_waiting_percent'] = str(round(float(format(month_stats['claim_waiting'] / month_stats['total_tips'], '.2%').replace('%','')))) + '%'
    except ZeroDivisionError:
        #first of the month with no tips yet
        month_stats['claim_waiting_percent'] = '0%'
    month_stats['total_claimed_returned'] = {'Sent': month_stats['sent_tips'], 'Claimed':month_stats['claimed_tips'], 'Unclaimed': month_stats['claim_waiting'], 'Returned': month_stats['returned_tips'],}

    total_BCH = all_month_tips.aggregate(Sum('coin_amount'))
    month_stats['total_BCH'] = total_BCH['coin_amount__sum']
    total_USD = all_month_tips.aggregate(Sum('fiat_value'))
    month_stats['total_USD'] = total_USD['fiat_value__sum']

    #month_tips_ordered = all_tips.order_by('-created_datetime')
    #month_stats['start_date'] = month_tips_ordered.last().created_datetime
    #month_stats['end_date'] = all_tips_ordered.first().created_datetime

    month_stats['all_senders'] = all_month_tips.filter(~Q(sender = " ")).values_list('sender').annotate(sender_count=Count('sender')).order_by('-sender_count')
    #Organize senders by total value tipped
    sender_amount = {}
    for sender, count in month_stats['all_senders']:
        sender_amount[sender] = {'bch':0,'usd':0,'usd_current':0}
        for tip in all_month_tips:
            if tip.sender == sender:
                sender_amount[sender]['bch'] += float(tip.coin_amount)
                sender_amount[sender]['usd'] += float(tip.fiat_value)
        sender_amount[sender]['usd_current'] = float(sender_amount[sender]['bch']) * month_stats['bch_price']
    #https://www.geeksforgeeks.org/python-sort-nested-dictionary-by-key/
    #Sorting nested dictionary by key so that the user with the highest 'bch' value ends up first
    sorted_sender_amount = OrderedDict(sorted(sender_amount.items(), key = lambda x: getitem(x[1], 'bch'), reverse=True))
    month_stats['sender_amount'] = sorted_sender_amount

    month_stats['senders_by_subs'] = sender_subreddits(month_stats['all_senders'], all_month_tips)

    all_tips_receivers = all_month_tips.filter(~Q(status = 'returned'))
    month_stats['all_receivers'] = all_tips_receivers.values_list('receiver').annotate(receiver_count=Count('receiver')).order_by('-receiver_count')
    month_stats['all_subs'] = all_month_tips.values_list('subreddit').annotate(subreddit_count=Count('subreddit')).order_by('-subreddit_count')

    try:
        month_stats['total_USD_current'] = "{:.2f}".format(float(month_stats['total_BCH']) * month_stats['bch_price'])
    except TypeError:
        #first of the month with no tips yet
        month_stats['total_USD_current'] = '0'

    month_stats['tip_per_day_result'] = tip_per_day(all_month_tips.order_by('created_datetime'))
    month_stats['value_per_day_result'] = tip_per_day(all_month_tips.order_by('created_datetime'), tip_value=True)
    context = {
        'all_tips':all_tips_ordered,
        'all_month_tips':all_month_tips,
        'all_stats':all_stats,
        'month_stats':month_stats,

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

def tip_per_month(all_tips):
    '''
    Prepares a dict of # of tips and value of tips per month
    '''
    case_years = {}
    for tip in all_tips:
        year = tip.created_datetime.year
        month = tip.created_datetime.strftime("%B")
        if year not in case_years:
            case_years[year] = {}
        if month not in case_years[year]:
            case_years[year][month] = {}
        try:
            case_years[year][month]['tip_amount'] += 1
        except KeyError:
            case_years[year][month]['tip_amount'] = 0
            case_years[year][month]['tip_amount'] += 1
        try:
            case_years[year][month]['tip_value'] += round(tip.fiat_value, 2)
        except KeyError:
            case_years[year][month]['tip_value'] = 0
            case_years[year][month]['tip_value'] += round(tip.fiat_value, 2)
    return case_years

def sender_subreddits(all_senders, all_tips):
    '''
    Orders Tippers by the amount of unique subreddits they tipped in.
    A user who tipped 100 tips in only one subreddit will get a count of 1.
    '''
    #all_senders = all_tips.filter(~Q(sender = " ")).values_list('sender').annotate(sender_count=Count('subreddit')).order_by('-sender_count')
    sender_amount = {}
    for sender, count in all_senders:
        sender_amount[sender] = {}
        sender_subs = []
        for tip in all_tips:
            if tip.sender == sender:
                sender_subs.append(tip.subreddit)
        sender_amount[sender]['subs'] = [i for i in set(sender_subs)]
        sender_amount[sender]['subs_len'] = len(sender_amount[sender]['subs'])
        #sender_amount[sender]['count'] = count
    #https://www.geeksforgeeks.org/python-sort-nested-dictionary-by-key/
    #Sorting nested dictionary by key so that the user with the highest 'bch' value ends up first
    sorted_sender_subs = OrderedDict(sorted(sender_amount.items(), key = lambda x: getitem(x[1], 'subs_len'), reverse=True))
    return sorted_sender_subs

def retrieve_dates(date_request):
    '''
    today = (datetime.datetime(2020, 12, 4, 0, 0) 
    end_of_day = (datetime.datetime(2020, 12, 4, 23, 59) 
    first_of_week = (datetime.datetime(2020, 11, 30, 0, 0) 
    end_of_week = (datetime.datetime(2020, 12, 6, 23, 59) 
    first_of_month = (datetime.datetime(2020, 12, 1, 0, 0)
    end_of_month = (datetime.datetime(2020, 12, 31, 23, 59)
    '''
    if date_request == '' or date_request == None:
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        today = datetime.datetime.strptime(date_request, '%Y-%m')

    end_of_day = today.replace(hour=23, minute = 59, second = 59, microsecond = 0)

    #0 = monday, 5 = Saturday, 6 = Sunday 
    day = today.weekday()
    first_of_week = today + timezone.timedelta(days = -day)
    end_of_week = first_of_week + timezone.timedelta(days = 6)
    end_of_week = end_of_week.replace(hour = 23, minute = 59, second = 59)

    first_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    year = first_of_month.year
    month = first_of_month.month
    last_day = calendar.monthrange(year,month)[1]
    end_of_month = first_of_month.replace(day=last_day, hour=23, minute=59, second=59)

    return today, end_of_day, first_of_week, end_of_week, first_of_month, end_of_month

def export_csv_all_tips(request):
    all_tips = RedditTip.objects.all().values_list('blockchain_tx', 'coin_amount', 'coin_type','fiat_type','fiat_value','receiver','sender','body_text','created_datetime','created_utc','comment_id','permalink','parent_id','parent_comment_permalink','score','subreddit','status',)

    response = HttpResponse(content_type='test/csv')

    csv_writer = csv.writer(response)
    csv_writer.writerow(['blockchain_tx', 'coin_amount', 'coin_type','fiat_type','fiat_value','receiver','sender','body_text','created_datetime','created_utc','comment_id','permalink','parent_id','parent_comment_permalink','score','subreddit','status',])

    for tip in all_tips:
        csv_writer.writerow(tip)
    response['Content-Disposition'] = 'attachment; filename="tips.csv"'

    return response

def test_post(request):
    from .tasks import make_post
    make_post()
    return HttpResponse('Completed!!')

def populate_db(request):
    from .tasks import get_tips
    get_tips()
    #from .tasks import get_price
    #get_price()
    return HttpResponse('Testing!')