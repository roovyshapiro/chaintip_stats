from __future__ import absolute_import, unicode_literals
#from celery import Celery, shared_task
from django.utils import timezone
from django.utils.timezone import make_aware
 
from .models import RedditTip
from .chaintip_stats import Chaintip_stats
import json, os

#@shared_task
def get_tips():
    '''    Example Tip:
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
    type = models.CharField(max_length = 15)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    '''
    tips = retrieve_reddit_tips()

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
        new_tip.receiver = tip['body']['receiver']
        new_tip.sender = tip['body']['sender']

        new_tip.body_text = tip['body_text']
        new_tip.created_datetime = make_aware(tip['created_datetime'])

        new_tip.created_utc = tip['created_utc']
        new_tip.comment_id = tip['id']
        new_tip.parent_comment_permalink = tip['parent_comment_permalink']
        new_tip.parent_id = tip['parent_id']
        new_tip.permalink = tip['permalink']
        new_tip.score = tip['score']
        new_tip.subreddit = tip['subreddit']
        new_tip.type = tip['type']

        new_tip.save()

def retrieve_reddit_tips():
    '''
    '''
    credentials_file = 'credentials.json'
    credentials_path = os.path.join(os.path.abspath('.'), credentials_file)
    with open(credentials_path) as f:
        data = f.read()
    credential_dict = json.loads(data)
    chaintip_api = Chaintip_stats(credential_dict['client_id'], credential_dict['client_secret'], credential_dict['user_agent'], credential_dict['username'], credential_dict['password'])
    chaintip_comments = chaintip_api.gather_chaintip_stats()

    return chaintip_comments