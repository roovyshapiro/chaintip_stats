# CHAINTIP STATS
- [CHAINTIP STATS](#chaintip-stats)
  - [What is Chaintip and how does it work?](#what-is-chaintip-and-how-does-it-work)
  - [What's the purpose of CHAINTIP STATS?](#whats-the-purpose-of-chaintip-stats)
  - [How does CHAINTIP STATS work?](#how-does-chaintip-stats-work)
  - [Hosting with Python Anywhere](#hosting-with-python-anywhere)
  - [Credentials](#credentials)
  - [DNS / stats.chaintip.org](#dns--statschaintiporg)
  - [Why Bitcoin Cash?](#why-bitcoin-cash)
  - [What can I actually do with Bitcoin Cash?](#what-can-i-actually-do-with-bitcoin-cash)
  
*Site is currently live at [stats.chaintip.org](https://stats.chaintip.org)*

**Monthly View**
![](https://i.imgur.com/2XzyeCZ.png)

**All Time View**
![](https://i.imgur.com/Q0wMnRB.png)

## What is Chaintip and how does it work?

[Chaintip](https://www.chaintip.org/)  for Reddit was created by  [u/Tibanne](https://www.reddit.com/user/tibanne)  to allow users to easily tip Bitcoin Cash (BCH) to each other directly without knowing the recipient's wallet address.

Let's say you want to tip a user for a comment or post they made on reddit:

1.  Simply reply to their comment or post and mention "[u/chaintip](https://www.reddit.com/user/chaintip)".
2.  Chaintip then sends you a private message letting you know which Bitcoin Cash address to send the tip to.
3. When you send any amount of BCH to that address, Chaintip will act as a middle man and hold onto the funds until the recipient claims it.
4.  The recipient can then claim the funds by checking the private message they received from u/chaintip and replying with their Bitcoin Cash  [wallet](https://wallet.bitcoin.com/)  address.
5.  Chaintip sends the recipient the Bitcoin Cash and edits the original comment to let everyone know the tip was claimed.
6.  If the recipient doesn't claim the tip within a week, it gets returned to the sender.

This process is only necessary the first time a user receives funds. Once the recipient has already told u/chaintip their address, the next tip they receive will get sent directly to their wallet.

## What's the purpose of CHAINTIP STATS?

CHAINTIP STATS is live dashboard which collects and analyzes the tips that are being sent. It has been designed as a high score / leaderboard to showcase information such as 
- which users are tipping the most number of tips 
- which users are tipping the most value of tips in USD
- which tippers have been active in the most unique subreddits. 

By highlighting individual user achievements, users will be encouraged to tip more which will help spread awareness and adoption of BCH.

CHAINTIP STATS also contains other useful information such as

-   How much Bitcoin Cash was tipped in total?
-   How much was it worth in USD at the time of the tip being sent and how much is it worth now?
-   Which subreddits have the most tips?
-   How does this month's tipping activity compare to previous months 

## How does CHAINTIP STATS work?

Chaintip Stats is a web application built with Django.

Chaintip automatically posts a public comment stating the amount and status of every tip.
*Here you can see an example of every possible status:*
![enter image description here](https://i.imgur.com/oQZq2wv.png)

Every hour, all of u/chaintip's recent are collected from Reddit via API using [PRAW](https://praw.readthedocs.io/en/stable/) and then stored in the Django database.

Current BCH -> USD price data is retrieved from the CoinMarketCap API and stored as well.

On the back end, Django calculates and presents the data to the web page.

[DataTables](https://datatables.net/)  is used to give the tables some extra functionality.

[Chart.JS](https://www.chartjs.org/docs/master/)  is used to present the data in graphs and charts.

## Hosting with [Python Anywhere](https://www.pythonanywhere.com/?affiliate_id=00a5e5d4)
This site is being hosted on [Python Anywhere](https://www.pythonanywhere.com/?affiliate_id=00a5e5d4) currently. Originally, the regular API calls to reddit were designed to work with Celery/[Celery Beat](https://www.merixstudio.com/blog/django-celery-beat/). As PythonAnywhere doesn't support celery, a simple cron job with a [custom Django managament](https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/) command is used instead.


## Credentials
In order for this project to run, a file called "credentials.json" is needed within the main directory.
This is where the reddit API information, coinmarketcap API key, and django secret key will be stored.

The format of this file must look like this:
```
{"client_id":"<reddit client id>","client_secret":"<reddit client secret>","user_agent":"<reddit user agent>",
"username":"<regular reddit username>","password":"<regular reddit password>",
"django_secret_key":"<django secret key>",
"coinmarketcap_apikey":"<coinmarketcapi api key>"}
```


## DNS / [stats.chaintip.org](https://stats.chaintip.org/)
[Chaintip](https://www.chaintip.org/)  for Reddit was created and is maintained by [u/Tibanne](https://www.reddit.com/user/tibanne) and he is the owner of chaintip.org. This live dashboard is a completely separate project but for now, he has allowed the use of the stats subdomain so its easy for users to find.


## [Why Bitcoin Cash?](https://whybitcoincash.com/)

Bitcoin Cash (BCH) is the most faithful implementation of Satoshi Nakamoto's Bitcoin CryptoCurrency project. BCH is focused on low fees, adoption, scalability and usage as an actual currency for everyday transcations.

_"Bitcoin Cash is a global, peer-to-peer cryptocurrency that allows value to be sent to anyone, anywhere in the world, without intermediaries. Bitcoin Cash is not controlled by any single entity and is instead secured permissionlessly by thousands of computers around the world dedicated to maintaining the network._

_Bitcoin Cash is decentralized so that no business, institution, or government can control it and no one can censor your payments. It is an alternative to government-controlled fiat currency that has been mismanaged and debased to an unprecedented degree. Bitcoin Cash, on the other hand, maintains a diminishing minting schedule and will forever be capped at 21 million coins."_

[-https://bchfaq.com/faq/what-is-bitcoin-cash/](https://bchfaq.com/faq/what-is-bitcoin-cash/)

## What can I actually do with Bitcoin Cash?

Bitcoin Cash has a very expansive community and ecosystem of products and services.
[Here's a great place to start](https://read.cash/@tula_s/bitcoin-cash-meta-25d6f35e) to find everything BCH related.