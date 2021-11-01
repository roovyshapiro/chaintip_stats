from django.db.models.expressions import Value
from django.http.response import HttpResponse
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.utils.timezone import make_aware
from django.shortcuts import render
from .models import RedditTip, BCHPrice
import datetime, csv, calendar
from collections import OrderedDict
from operator import getitem

def main_month(request):

    month_stats = {}

    date_request = request.GET.get('date_start')
    today, end_of_day, first_of_week, end_of_week, first_of_month, end_of_month = retrieve_dates(date_request)
    all_tips = RedditTip.objects.all()
    bch_prices = BCHPrice.objects.all().order_by('-time_dt')

    all_tips_ordered = all_tips.order_by('-created_datetime')
    #Min Max Values for Date Picker 
    first_tip = all_tips_ordered.last().created_datetime
    month_stats['first_tip_date'] = first_tip.strftime('%Y-%m')
    month_stats['last_tip_date'] = timezone.now().strftime('%Y-%m')


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

    try:
        month_stats['tip_per_day_result'] = tip_per_day(all_month_tips.order_by('created_datetime'))
    except AttributeError:
        month_stats['tip_per_day_result'] = ''
    try:
        month_stats['value_per_day_result'] = tip_per_day(all_month_tips.order_by('created_datetime'), tip_value=True)
    except AttributeError:
        month_stats['value_per_day_result'] = ''


    #Generate the data needed for the line graph which compares each day to the previous month's day
    month_stats['month_comparison_data'] = month_comparison_data(all_tips, today)

    context = {
        'all_month_tips':all_month_tips,
        'month_stats':month_stats,
    }
    return render(request, "reddit_tips/reddit_tips_month.html", context) 


def main_all(request):

    all_stats = {}

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
    all_stats['tip_value_per_month_result'] = tip_per_month(all_tips.order_by('created_datetime'))

    context = {
        'all_tips':all_tips_ordered,
        'all_stats':all_stats,

    }
    return render(request, "reddit_tips/reddit_tips_all.html", context) 

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
            case_years[year][month]['tip_value'] += int(tip.fiat_value)
        except KeyError:
            case_years[year][month]['tip_value'] = 0
            case_years[year][month]['tip_value'] += int(tip.fiat_value)

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


def month_comparison_data(all_tips, today):
    '''
    {
    'October':{
        'first_day': datetime.datetime(2021, 10, 1, 0, 0, tzinfo=<UTC>),
        'last_day': datetime.datetime(2021, 10, 31, 23, 59, 59, tzinfo=<UTC>), 
        'tip_amount': [49, 65, 95, 162, 208, 248, 288, 314, 320, 351, 384, 410, 443, 477, 507, 518, 538, 577, 635, 716, 780, 828, 836, 888, 941, 999, 1035, 1095, 1098],
        'tip_value': [272.86, 280.87, 287.62, 330.28, 404.69, 484.26, 642.98, 664.16, 715.56, 830.83, 854.51, 905.14, 919.22, 933.4, 1112.3, 1203.89, 1246.1, 1265.06, 1393.54, 1433.83, 1690.12, 1750.72, 1754.71, 1791.89, 1832.97, 1883.55, 1921.04, 2014.58, 2015.03, 2015.03, 2015.03],
        'claimed_tips': [7, 8, 20, 34, 44, 54, 65, 73, 73, 80, 88, 95, 104, 113, 119, 122, 123, 138, 150, 167, 180, 197, 200, 207, 216, 226, 236, 251, 252, 252, 252]},
        }, 
    'September':{
        'first_day': datetime.datetime(2021, 9, 1, 0, 0, tzinfo=<UTC>), 
        'last_day': datetime.datetime(2021, 9, 30, 0, 0, tzinfo=<UTC>), 
        'tip_amount': [28, 66, 66, 66, 86, 154, 169, 203, 254, 305, 322, 393, 434, 439, 456, 481, 519, 549, 575, 610, 632, 645, 669, 697, 717, 746, 776, 792, 798, 816]
        'tip_value': 'tip_value': [9.9, 22.91, 22.91, 22.91, 25.98, 159.79, 216.64, 519.89, 559.92, 571.68, 784.98, 1014.75, 1068.94, 1070.77, 1086.67, 1155.1, 1218.52, 1428.84, 1449.97, 1509.94, 1643.31, 1671.06, 1891.15, 2062.76, 2144.31, 2171.7, 2321.49, 2341.64, 2361.6, 2425.22], 
        'claimed_tips': [4, 9, 9, 9, 17, 37, 40, 44, 58, 70, 72, 93, 101, 103, 107, 114, 120, 128, 137, 147, 152, 153, 157, 161, 163, 173, 178, 179, 182, 188]
    }, 
    'August': {
        'first_day': datetime.datetime(2021, 8, 1, 0, 0, tzinfo=<UTC>), 
        'last_day': datetime.datetime(2021, 8, 31, 0, 0, tzinfo=<UTC>), 
        'tip_amount': [15, 34, 43, 61, 99, 114, 122, 169, 213, 240, 279, 315, 369, 384, 408, 448, 485, 519, 548, 560, 570, 586, 640, 664, 717, 731, 754, 768, 782, 803, 832],
        'tip_value': [25.73, 80.77, 102.3, 131.33, 348.31, 359.87, 375.55, 414.53, 474.86, 496.82, 524.16, 531.24, 550.37, 572.01, 585.32, 619.13, 625.07, 633.47, 656.65, 672.09, 675.92, 732.65, 779.43, 802.73, 824.79, 826.72, 834.19, 847.13, 855.76, 969.42, 993.8], 
        'claimed_tips': [4, 10, 11, 18, 24, 29, 31, 41, 50, 53, 59, 66, 73, 73, 76, 85, 96, 105, 112, 115, 116, 119, 130, 138, 147, 151, 159, 161, 163, 167, 171]
        }, 
    'July': {
        ...
    }
    }
    '''
    try:
        today_date = make_aware(today.replace(hour=0, minute=0, second=0, microsecond=0))
    except ValueError:
        today_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    first_of_month = today_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    year = first_of_month.year
    month = first_of_month.month
    last_day = calendar.monthrange(year,month)[1]
    end_of_month = first_of_month.replace(day=last_day, hour=23, minute=59, second=59)
  
    comparison_data = {}

    last_day_of_previous_month1 = first_of_month - datetime.timedelta(days=1)
    last_day_of_previous_month1 = last_day_of_previous_month1.replace(hour=23, minute=59, second=59)
    first_day_of_previous_month1 = last_day_of_previous_month1.replace(day=1, hour=0,minute=0,second=0)
    
    last_day_of_previous_month2 = first_day_of_previous_month1 - datetime.timedelta(days=1)
    last_day_of_previous_month2 = last_day_of_previous_month2.replace(hour=23, minute=59, second=59)
    first_day_of_previous_month2 = last_day_of_previous_month2.replace(day=1, hour=0,minute=0,second=0)

    last_day_of_previous_month3 = first_day_of_previous_month2 - datetime.timedelta(days=1)
    last_day_of_previous_month3 = last_day_of_previous_month3.replace(hour=23, minute=59, second=59)
    first_day_of_previous_month3 = last_day_of_previous_month3.replace(day=1, hour=0,minute=0,second=0)

    comparison_data[first_of_month.strftime('%B')] = {}
    comparison_data[first_of_month.strftime('%B')]['first_day'] = first_of_month
    comparison_data[first_of_month.strftime('%B')]['last_day'] = end_of_month
    comparison_data[first_of_month.strftime('%B')]['tip_amount'] = []
    comparison_data[first_of_month.strftime('%B')]['tip_value'] = []
    comparison_data[first_of_month.strftime('%B')]['claimed_tips'] = []

    comparison_data[first_day_of_previous_month1.strftime('%B')] = {}
    comparison_data[first_day_of_previous_month1.strftime('%B')]['first_day'] = first_day_of_previous_month1
    comparison_data[first_day_of_previous_month1.strftime('%B')]['last_day'] = last_day_of_previous_month1
    comparison_data[first_day_of_previous_month1.strftime('%B')]['tip_amount'] = []
    comparison_data[first_day_of_previous_month1.strftime('%B')]['tip_value'] = []
    comparison_data[first_day_of_previous_month1.strftime('%B')]['claimed_tips'] = []

    comparison_data[first_day_of_previous_month2.strftime('%B')] = {}
    comparison_data[first_day_of_previous_month2.strftime('%B')]['first_day'] = first_day_of_previous_month2
    comparison_data[first_day_of_previous_month2.strftime('%B')]['last_day'] = last_day_of_previous_month2
    comparison_data[first_day_of_previous_month2.strftime('%B')]['tip_amount'] = []
    comparison_data[first_day_of_previous_month2.strftime('%B')]['tip_value'] = []
    comparison_data[first_day_of_previous_month2.strftime('%B')]['claimed_tips'] = []

    comparison_data[first_day_of_previous_month3.strftime('%B')] = {}
    comparison_data[first_day_of_previous_month3.strftime('%B')]['first_day'] = first_day_of_previous_month3
    comparison_data[first_day_of_previous_month3.strftime('%B')]['last_day'] = last_day_of_previous_month3
    comparison_data[first_day_of_previous_month3.strftime('%B')]['tip_amount'] = []
    comparison_data[first_day_of_previous_month3.strftime('%B')]['tip_value'] = []
    comparison_data[first_day_of_previous_month3.strftime('%B')]['claimed_tips'] = []


    #Makes a list of all days in the range of the beginning and end of the available days in db
    for month in comparison_data:
        if timezone.now().strftime('%B') == month:
            date_range = [comparison_data[month]['first_day'] + datetime.timedelta(days=x) for x in range(0, (timezone.now() - comparison_data[month]['first_day']).days + 1)]
        else:
            date_range = [comparison_data[month]['first_day'] + datetime.timedelta(days=x) for x in range(0, (comparison_data[month]['last_day'] - comparison_data[month]['first_day']).days + 1)]        
        for date in date_range:
            date_count = 0
            value_count = 0
            claim_count = 0
            for tip in all_tips.filter(created_datetime__gte=comparison_data[month]['first_day'], created_datetime__lte=comparison_data[month]['last_day']):
                if tip.created_datetime.replace(hour=0, minute = 0, second=0,microsecond=0) == date:
                    #This captures the amount of tips in a specific day
                    date_count += 1
                    #This captures the total value of tips in a specific day
                    value_count += tip.fiat_value
                    #This captures the total amount of claims (first time users) per day
                    if tip.status == "claimed":
                        claim_count += 1
            if len(comparison_data[month]['tip_amount']) >= 1:
                date_count = date_count + comparison_data[month]['tip_amount'][-1]
            
            if len(comparison_data[month]['tip_value']) >= 1:
                value_count = round(value_count + comparison_data[month]['tip_value'][-1], 2)
            else:
                value_count = round(value_count, 2)
            if len(comparison_data[month]['claimed_tips']) >= 1:
                claim_count = claim_count + comparison_data[month]['claimed_tips'][-1]

            comparison_data[month]['tip_amount'].append(date_count)
            comparison_data[month]['tip_value'].append(value_count)
            comparison_data[month]['claimed_tips'].append(claim_count)

    return comparison_data


def test_post(request):
    from .tasks import make_post
    make_post()
    return HttpResponse('Completed!!')

def populate_db(request):
    '''
    Runs the custom "tasks" management command which updates the price and tips via API
    '''
    from django.core.management import call_command
    call_command('tasks')
    return HttpResponse('Testing!')