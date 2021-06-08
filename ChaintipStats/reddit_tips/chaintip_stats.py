#https://praw.readthedocs.io/en/latest/index.html
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
        #print("u/chaintip's comment karma: ", redditor_chaintip.comment_karma)

        for comment in self.reddit.redditor("chaintip").comments.new(limit=None):
            comment_dict ={}
            if "[been sent]" in comment.body:
                comment_dict['type'] = 'sent'
                body_list = comment.body.replace("you've [been sent]","").replace("by","").replace("via [chaintip](http://www.chaintip.org).","").replace("(","").replace(")","").replace('|',"").replace("***","").replace("`","").replace("~","").split()
                comment_dict['body'] = {}
                comment_dict['body']['receiver'] = body_list[0].replace(",","")
                comment_dict['body']['blockchain_tx'] = body_list[1]
                comment_dict['body']['coin_amount'] = body_list[2]
                comment_dict['body']['coin_type'] = body_list[3]
                comment_dict['body']['fiat_value'] = body_list[4]
                comment_dict['body']['fiat_type'] = body_list[5]
                comment_dict['body']['sender'] = body_list[6]
            elif "[claimed]" in comment.body:
                comment_dict['type'] = 'claimed'
                body_list = comment.body.replace("has [claimed]","").replace("the","").replace("sent by","").replace("via [chaintip](http://www.chaintip.org).","").replace("(","").replace(")","").replace("`","").replace("~","").replace("|","").replace("***","").split()
                comment_dict['body'] = {}
                comment_dict['body']['receiver'] = body_list[0]
                comment_dict['body']['blockchain_tx'] = body_list[1]
                comment_dict['body']['coin_amount'] = body_list[2]
                comment_dict['body']['coin_type'] = body_list[3]
                comment_dict['body']['fiat_value'] = body_list[4]
                comment_dict['body']['fiat_type'] = body_list[5]
                comment_dict['body']['sender'] = body_list[6]
            else:
                comment_dict['type'] = 'returned'
                body_list = comment.body.replace("[chaintip](http://www.chaintip.org) has [returned]("," ").replace(") the unclaimed tip of `"," ").replace("` | `~"," ").replace("` to "," ").replace("***","").split()
                comment_dict['body'] = {}
                comment_dict['body']['receiver'] = body_list[5]
                comment_dict['body']['blockchain_tx'] = body_list[0]
                comment_dict['body']['coin_amount'] = body_list[1]
                comment_dict['body']['coin_type'] = body_list[2]
                comment_dict['body']['fiat_value'] = body_list[3]
                comment_dict['body']['fiat_type'] = body_list[4]
                comment_dict['body']['sender'] = ' '
            comment_dict["subreddit"] = comment.subreddit.display_name
            comment_dict["body_text"] = comment.body.replace("***","").replace("\n"," ")
            comment_dict["id"] = comment.id
            comment_dict["parent_id"] = comment.parent_id
            parent_comment_id = comment.parent_id.replace('t1_','').replace('t3_','')
            comment_dict['parent_comment_permalink'] = "https://reddit.com" + comment.permalink.replace(comment.id,parent_comment_id)
            comment_dict["created_utc"] = comment.created_utc
            comment_dict["created_datetime"] = datetime.datetime.utcfromtimestamp(int(comment.created_utc))
            comment_dict["score"] = comment.score
            comment_dict["permalink"] = "https://reddit.com" + comment.permalink
            self.chaintip_comments.append(comment_dict)

        print('total comments: ', len(self.chaintip_comments))
        return(self.chaintip_comments)

if __name__ == '__main__':
    with open('credentials.json') as f:
        data = f.read()
    credential_dict = json.loads(data)
    chaintip_api = Chaintip_stats(credential_dict['client_id'], credential_dict['client_secret'], credential_dict['user_agent'], credential_dict['username'], credential_dict['password'])
    chaintip_comments = chaintip_api.gather_chaintip_stats()
    data = json.dumps(chaintip_comments,  indent=4, sort_keys=True)
    with open('chaintip_comments.json', 'w') as f:
        f.write(data)