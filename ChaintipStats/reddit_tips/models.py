from os import set_inheritable
from django.db import models
from django.utils import timezone

class RedditTip(models.Model):
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
    '''
    blockchain_tx = models.CharField(max_length=150)
    coin_amount = models.CharField(max_length=30)
    coin_type = models.CharField(max_length=10)
    fiat_type = models.CharField(max_length=10)
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
    status = models.CharField(max_length=30, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender} -> {self.receiver} - r/{self.subreddit} - {self.created_datetime.strftime("%Y-%m-%d %H:%M:%S")}'

class BCHPrice(models.Model):
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
    '''
    price = models.CharField(max_length=30) 
    price_format = models.FloatField()
    time = models.CharField(max_length=30)
    time_dt = models.DateTimeField(null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.price_format} - {self.time_dt.strftime("%Y-%m-%d %H:%M:%S")}'