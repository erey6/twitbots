#!python
from __future__ import print_function
import mlbgame
import random
import tweepy
import twitter_credentials
from datetime import datetime

auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

classics = [["Jody", "Davis", "1956-11-12"],
            ["Andre", "Dawson", "1954-07-10"],
            ["Ryne", "Sandberg", "1959-09-18"],
            ["Fergie", "Jenkins",  "1942-12-13"],
            ["Greg", "Maddux", "1966-04-14"],
            ["Billy", "Williams","1938-06-15"],
            ["Sammy", "Sosa", "1968-11-12"],
            ["Gary", "Matthews","1950-07-05"],
            ["Rick", "Sutcliffe","1956-06-21"],
            ["Rick", "Reuschel","1949-05-16"],
            ["Lee", "Smith","1957-12-04"],
            ["Kerry", "Wood","1977-06-16"]]

rip_classics = [["Ron", "Santo","1940-02-25"],
                ["Jack", "Brickhouse", "1916-01-24"],
                ["Ernie", "Banks", "1931-01-31"]]
fans = [['Michelle', 'Obama', '1964-01-11'],
        ['Bill', 'Murray', '1950-09-21'],
        ['John ', 'Cusack', '1966-06-28'],
        ['Eddie', 'Veddder', '1964-12-23'],
        ['Hillary', 'Clinton', '1947-10-26'],
        ['Billy', 'Corgan', '1967-06-17'],
        ['Vince', 'Vaughn', '1970-03-28'],
        ['Dwyane', 'Wade', '1982-01-17'],
        ['Jeff', 'Garlin', '1962-06-05'],
        ['Nick', 'Offerman', '1970-06-26'],
        ['Bonnie', 'Hunt', '1961-09-22']]

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

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
cubs_roster = mlbgame.roster(112)



for i in cubs_roster.players:
    dob = i.birth_date
    b_year = dob[0:4]
    b_month = dob[5:7]
    b_date = dob[8:10]
    age = currentYear - int(b_year)
    if int(b_date) == currentDay and int(b_month) == currentMonth:
        closing = random.choice(["I'll see you on Rush Street.", "This Bud's for you!"])
        my_status = "{} {} turns {} today. Happy birthday, {}! {}\n\n#Cubs".format(i.name_first, i.name_last, age, i.name_first, closing)
        api.update_status(status=my_status)


for item in classic_dicts:
    dob = (item['birth_date'])
    b_year = dob[0:4]
    b_month = dob[5:7]
    b_date = dob[8:10]
    age = currentYear - int(b_year)
    if int(b_date) == currentDay and int(b_month) == currentMonth:
        closing = random.choice(["I'll see you on Rush Street.", "This Bud's for you!"])
        my_status = "{} {} turns {} today. Happy birthday, {}! {}\n\n#Cubs @Cubs".format(item["name_first"], item["name_last"], age, item["name_first"], closing)
        #print(my_status)
        api.update_status(status=my_status)

for item in fans_dicts:
    dob = (item['birth_date'])
    b_year = dob[0:4]
    b_month = dob[5:7]
    b_date = dob[8:10]
    age = currentYear - int(b_year)
    if int(b_date) == currentDay and int(b_month) == currentMonth:
        closing = random.choice(["I'll see you on Rush Street.", "This Bud's for you!"])
        my_status = "Longtime Cubs fan {} {} turns {} today. Happy birthday, {}! {}\n\n#Cubs @Cubs".format(item["name_first"], item["name_last"], age, item["name_first"], closing)
        #print(my_status)
        api.update_status(status=my_status)

for item in rip_classic_dicts:
    dob = (item['birth_date'])
    b_year = dob[0:4]
    b_month = dob[5:7]
    b_date = dob[8:10]
    age = currentYear - int(b_year)
    if int(b_date) == currentDay and int(b_month) == currentMonth:
        closing = random.choice(["Everybody raise a can of ice cold Bud Light.", "This Bud's for you! "])
        my_status = "{} {} was born {} years ago today. Happy birthday, {}! Gone but not forgotten. {}\n\n#Cubs @Cubs ".format(item["name_first"], item["name_last"], age, item["name_first"], closing)
        #print(my_status)
        api.update_status(status=my_status)





      
    
