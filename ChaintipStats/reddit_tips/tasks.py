from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task
from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Q

 
from .models import RedditTip, BCHPrice
from .chaintip_stats import Chaintip_stats
from .coinmarketcap import CoinMarketCapAPI
import json, os

@shared_task
def get_tips():
    '''    
    Example Tip:
    {
        "body": {
            "blockchain_tx": "https://explorer.bitcoin.com/bch/address/bitcoincash:qrelay2vk63vgym22t2azxjjechraf74dcks4ef00x",
            "coin_amount": "0.0395507",
            "coin_type": "BCH",
            "fiat_type": "USD",
            "fiat_value": "25.04",
            "receiver": "u/Howyoudouken",
            "sender": "u/moleccc"
        },
        "body_text": " u/Howyoudouken, you've [been sent](https://explorer.bitcoin.com/bch/address/bitcoincash:qrelay2vk63vgym22t2azxjjechraf74dcks4ef00x) `0.0395507 BCH` | `~25.04 USD` by u/moleccc via [chaintip](http://www.chaintip.org). Please [claim it!](https://www.chaintip.org/reddit#claim) ",
        "created_datetime": "06/07/2021, 20:53:56",
        "created_utc": 1623099236.0,
        "id": "h0yd6d5",
        "parent_comment_permalink": "https://reddit.com/r/funny/comments/nu81dc/the_big_breakfast_a_tale_of_regret/h0yd46m/",
        "parent_id": "t1_h0yd46m",
        "permalink": "https://reddit.com/r/funny/comments/nu81dc/the_big_breakfast_a_tale_of_regret/h0yd6d5/",
        "score": 1,
        "subreddit": "funny",
        "type": "sent"
    },
    blockchain_tx = models.CharField(max_length=150)
    coin_amount = models.FloatField()
    coin_type = models.CharField(max_length=10)
    fiat_type = models.Charfield(max_length=10)
    fiat_value = models.FloatField()
    receiver = models.CharField(max_length=30) 
    sender = models.CharField(max_length=30)

    body_text = models.TextField()
    created_datetime = models.DateTimeField(null=True)
    created_utc = models.FloatField()
    comment_id = models.CharField(max_length=15)
    parent_comment_permalink = models.CharField(max_length=150)
    parent_id = models.CharField(max_length=15)
    permalink = models.CharField(max_length=150)
    score = models.IntegerField()
    subreddit = models.CharField(max_length=30)
    sent = models.BooleanField(Blank=True)
    claimed = models.BooleanField(Blank=True)
    returned = models.BooleanField(Blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    '''
    tips = retrieve_reddit_tips()

    print(len(tips))
    db_tips = RedditTip.objects.all()

    for tip in tips:
        #If the tip_comment_id exists in the database, then the tip will be updated
        #If the tip_comment_id doesn't exist, then the tip will be added to the db
        try:
            new_tip = db_tips.get(comment_id = tip['id'])
        except:
            new_tip = RedditTip()

        new_tip.blockchain_tx = tip['body']['blockchain_tx']
        new_tip.coin_amount = tip['body']['coin_amount']
        new_tip.coin_type = tip['body']['coin_type']
        new_tip.fiat_type = tip['body']['fiat_type']
        new_tip.fiat_value = tip['body']['fiat_value']
        try:
            new_tip.receiver = tip['body']['receiver']
        except:
            pass
        try:
            new_tip.sender = tip['body']['sender']
        except:
            pass

        new_tip.body_text = tip['body_text']
        new_tip.created_datetime = make_aware(tip['created_datetime'])

        new_tip.created_utc = tip['created_utc']
        new_tip.comment_id = tip['id']
        new_tip.parent_comment_permalink = tip['parent_comment_permalink']
        new_tip.parent_id = tip['parent_id']
        new_tip.permalink = tip['permalink']
        new_tip.score = tip['score']
        new_tip.subreddit = tip['subreddit']
        if tip['type'] == '' or tip['type'] == None:
            tip['type'] = ' '
        new_tip.status = tip['type']
        try:
            new_tip.save()
        except ValueError:
            print(f"TIP NOT SAVED! {tip}")
            continue


@shared_task
def get_price():
    '''
    Uses CoinMarketCap's API returns the following response in coinmarketcap.py:
    {
        "full_response": {
            "data": {
                "amount": 1,
                "id": 1831,
                "last_updated": "2021-06-09T03:09:07.000Z",
                "name": "Bitcoin Cash",
                "quote": {
                    "USD": {
                        "last_updated": "2021-06-09T03:09:07.000Z",
                        "price": 570.8301798074937
                    }
                },
                "symbol": "BCH"
            },
            "status": {
                "credit_count": 1,
                "elapsed": 19,
                "error_code": 0,
                "error_message": null,
                "notice": null,
                "timestamp": "2021-06-09T03:09:34.028Z"
            }
        },
        "price": 570.8301798074937,
        "price_format": "570.83",
        "time": "2021-06-09T03:09:07.000Z"
        'time_dt': datetime.datetime(2021, 6, 9, 3, 9, 7),
    }
    price = models.CharField(max_length=30) 
    price_format = models.FloatField()
    time = models.CharField(max_length=30)
    time_dt = models.DateTimeField(null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.price_format} - {self.time_dt.strftime("%Y-%m-%d %H:%M:%S")}'   
    '''

    credentials_file = 'credentials.json'
    credentials_path = os.path.join(os.path.abspath('.'), credentials_file)
    with open(credentials_path) as f:
        data = f.read()
    credential_dict = json.loads(data)
    cmcapi = CoinMarketCapAPI(credential_dict['coinmarketcap_apikey'])
    api_response = cmcapi.get_bch_price()

    new_price = BCHPrice()
    new_price.price = api_response['price']
    new_price.price_format = api_response['price_format']
    new_price.time = api_response['time']
    new_price.time_dt = make_aware(api_response['time_dt'])

    new_price.save()


def fix_tips_returned():
    '''
    A one time task to fix the senders & receivers in returned tips
    '''
    list_of_tips = retrieve_reddit_tips(fix_returned=True)
    db_tips = RedditTip.objects.all()

    for tip_dict in list_of_tips:
        tip = db_tips.get(comment_id = tip_dict['id'])

        tip.sender = tip_dict['sender']
        tip.receiver = tip_dict['receiver']
        tip.save()

def retrieve_reddit_tips(fix_returned = False):
    '''
    '''
    credentials_file = 'credentials.json'
    credentials_path = os.path.join(os.path.abspath('.'), credentials_file)
    with open(credentials_path) as f:
        data = f.read()
    credential_dict = json.loads(data)
    chaintip_api = Chaintip_stats(credential_dict['client_id'], credential_dict['client_secret'], credential_dict['user_agent'], credential_dict['username'], credential_dict['password'])
    if fix_returned == False:
        chaintip_comments = chaintip_api.gather_chaintip_stats()
    else:
        db_tips = RedditTip.objects.all().filter(status='returned')
        db_tips = db_tips.filter(Q(sender = None) | Q(receiver = None) | Q(sender = ' ') | Q(receiver = ' '))
        print(len(db_tips))
        chaintip_comments = chaintip_api.fix_returned_users(db_tips)
    return chaintip_comments


