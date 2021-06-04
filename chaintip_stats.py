#TODO: take into account when chaintip edits a comment
#"body_text": "[chaintip](http://www.chaintip.org) has [returned](https://explorer.bitcoin.com/bch/address/bitcoincash:qrelay2vhc3tzgmssztkelucgd0z3tj8kyyuph8uaf) the unclaimed tip of `0.00133864 BCH` | `~0.93 USD` to u/hero462.",
#"body_text": "u/NoodleyP has [claimed](https://explorer.bitcoin.com/bch/tx/7c7ceb1854d4f48914df2068c9f0e459a884478ecd094c91a4ba2b9b0f1717cd) the `0.005 BCH` | `~3.42 USD` sent by u/Tibannevia [chaintip](http://www.chaintip.org).",
#"body_text": "u/walerikus, you've [been sent](https://explorer.bitcoin.com/bch/address/bitcoincash:qrelay2cx05ju5l4v0vv0eh3vpd8f5u2xyjg2lytv6) `0.001337 BCH` | `~0.91 USD` by u/Remora_101via [chaintip](http://www.chaintip.org).",



import praw, datetime, json

class Chaintip_stats:
    def __init__(self, client_id, client_secret, user_agent, username, password):

        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.username = username
        self.password = password
        
        self.chaintip_comments = []

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            username=self.username,
            password=self.password,
        )

    def gather_chaintip_stats(self):
        redditor_chaintip = self.reddit.redditor("chaintip")
        print(redditor_chaintip.comment_karma)


        for comment in self.reddit.redditor("chaintip").comments.new(limit=None):
            comment_dict ={}
            comment_dict["subreddit"] = comment.subreddit.display_name
            body_list = comment.body.replace("you've [been sent]","").replace("by","").replace("via [chaintip](http://www.chaintip.org).","").replace("(","").replace(")","").replace('|',"").replace("***","").replace("`","").replace("~","").split()
            comment_dict['body'] = {}
            comment_dict['body']['receiver'] = body_list[0].replace(",","")
            comment_dict['body']['blockchain_tx'] = body_list[1]
            comment_dict['body']['coin_amount'] = body_list[2]
            comment_dict['body']['coin_type'] = body_list[3]
            comment_dict['body']['fiat_value'] = body_list[4]
            comment_dict['body']['fiat_type'] = body_list[5]
            comment_dict['body']['sender'] = body_list[6]
            comment_dict["body_text"] = comment.body.replace("***","").replace("\n","")
            comment_dict["created_utc"] = comment.created_utc
            comment_dict["created_datetime"] = datetime.datetime.utcfromtimestamp(int(comment.created_utc)).strftime("%m/%d/%Y, %H:%M:%S")
            comment_dict["score"] = comment.score
            comment_dict["permalink"] = "https://reddit.com" + comment.permalink
            print(comment_dict["permalink"])
            self.chaintip_comments.append(comment_dict)

        print(len(self.chaintip_comments))
        return(self.chaintip_comments)

if __name__ == '__main__':
    with open('credentials.json') as f:
        data = f.read()
        print(type(data))
    credential_dict = json.loads(data)
    chaintip_api = Chaintip_stats(credential_dict['client_id'], credential_dict['client_secret'], credential_dict['user_agent'], credential_dict['username'], credential_dict['password'])
    chaintip_comments = chaintip_api.gather_chaintip_stats()
    data = json.dumps(chaintip_comments,  indent=4, sort_keys=True)
    with open('chaintip_comments.json', 'a') as f:
        f.write(data)