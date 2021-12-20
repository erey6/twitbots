#!python
from __future__ import print_function
import mlbgame
import random
import tweepy
import hk_twitter_credentials
from datetime import datetime

auth = tweepy.OAuthHandler(hk_twitter_credentials.CONSUMER_KEY, hk_twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(hk_twitter_credentials.ACCESS_TOKEN, hk_twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year

classics = [["Carlton", "Fisk", "1947-12-26"],
            ["Harold", "Baines", "1959-03-15"],
            ["Frank", "Thomas", "1968-05-27"],
            ["Mark", "Buehrle",  "1979-03-23"],
            ["Robin", "Ventura","1967-07-14"],
            ["Luis", "Aparicio", "1934-04-29"],
            ["Magglio", "Ordonez","1974-01-28"],
            ["Chet", "Lemon","1955-02-12"],
            ["Paul", "Konerko","1976-03-05"],
            ["Ozzie", "Guillen", "1964-01-20"]]

rip_classics = [["Nellie", "Fox","1927-12-25"],
                ["Minnie", "Minoso", "1925-11-29"],
                ["Luke", "Appling", "1907-04-02"]]

fans = [['Barack', 'Obama', '1961-08-04'],
        ['Dennis', 'DeYoung', '1947-02-18'],
        ['Steve ', 'Dahl', '1954-11-20'],
        ['Michael', 'Jordan', '1963-02-17'],
        ['Richard', 'Daley', '1942-04-24'],
        ['Jenny', 'McCarthy', '1972-11-01'],
        ['George', 'Wendt', '1948-11-17'],
        ['Craig', 'Robinson', '1971-10-25']]

classic_dicts = list()
for person in classics:
    z = dict(zip(["name_first", "name_last", "birth_date"], person))
    classic_dicts.append(z)

rip_classic_dicts = list()
for person in rip_classics:
    z = dict(zip(["name_first", "name_last", "birth_date"], person))
    rip_classic_dicts.append(z)

fans_dicts = list()
for person in fans:
    z = dict(zip(["name_first", "name_last", "birth_date"], person))
    fans_dicts.append(z)


sox_roster = mlbgame.roster(145)



for i in sox_roster.players:
    dob = i.birth_date
    b_year = dob[0:4]
    b_month = dob[5:7]
    b_date = dob[8:10]
    age = currentYear - int(b_year)
    if int(b_date) == currentDay and int(b_month) == currentMonth:
        closing = random.choice(["D.J. and I wish you the best.", "Yesssssss!"])
        my_status = "{} {} turns {} today. Happy birthday, {}! {}\n\n#WhiteSox".format(i.name_use, i.name_last, age, i.name_use, closing)
        api.update_status(status=my_status)


for item in classic_dicts:
    dob = (item['birth_date'])
    b_year = dob[0:4]
    b_month = dob[5:7]
    b_date = dob[8:10]
    age = currentYear - int(b_year)
    if int(b_date) == currentDay and int(b_month) == currentMonth:
        closing = random.choice(["D.J. and I wish you the best.", "Yesssssss!"])
        my_status = "{} {} turns {} today. Happy birthday, {}! {}\n\n#WhiteSox".format(item["name_first"], item["name_last"], age, item["name_first"], closing)
        #print(my_status)
        api.update_status(status=my_status)

for item in fans_dicts:
    dob = (item['birth_date'])
    b_year = dob[0:4]
    b_month = dob[5:7]
    b_date = dob[8:10]
    age = currentYear - int(b_year)
    if int(b_date) == currentDay and int(b_month) == currentMonth:
        closing = random.choice(["D.J. and I wish you the best.", "Yesssssss!"])
        my_status = "Longtime Sox fan {} {} turns {} today. Happy birthday, {}! {}\n\n#WhiteSox".format(item["name_first"], item["name_last"], age, item["name_first"], closing)
        #print(my_status)
        api.update_status(status=my_status)

for item in rip_classic_dicts:
    dob = (item['birth_date'])
    b_year = dob[0:4]
    b_month = dob[5:7]
    b_date = dob[8:10]
    age = currentYear - int(b_year)
    if int(b_date) == currentDay and int(b_month) == currentMonth:
        closing = random.choice(["One of the greats!", "Real White Sox fans remember the great ones! "])
        my_status = "{} {} was born {} years ago on this date. Let's remember, {}! Gone but not forgotten. {}\n\n#WhiteSox".format(item["name_first"], item["name_last"], age, item["name_first"], closing)
        #print(my_status)
        api.update_status(status=my_status)





      
    
