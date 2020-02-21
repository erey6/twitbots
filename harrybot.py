import tweepy
import json
import random
import twitter_credentials
import time
from time import sleep
y = 1
#8/23, 11am

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

def video_test(tweet):
    #gets json info from tweet, looks for video file link
    json_str = json.dumps(tweet._json)
    json_dict = json.loads(json_str)
    entities = json_dict[u'entities']
    try:
        media = entities[u'media']
        video_url = (media[0])[u'expanded_url']
        if 'video' in video_url:
            return True
        else:
            return False
    except:
        return False

def baez_brain(r):
    #returns string about Javy
    superlatives = ["incredible!", "something else!",
                    "amazing!", "an astonishing player!",
                    "like the great Dave Henning: an amazing magician."]
    pick = random.choice(superlatives)
    closers = ["Holy cow!", "Listen to the crowd!",
               "Holy cow! \n#EverybodyIn ", "Holy cow! ","", "#EverybodyIn " , " "]
    closing = random.choice(closers)
    harry_says = "This guy is {} {} {}".format(pick, closing, r)
    return harry_says

def harry_brain(status, encoded_tweet, tweet_id):
    #searches tweets for keywords
    #print("working")
    retweet_link = 'https://twitter.com/Cubs/status/' + str(tweet_id)
    keywords = [ "Javy", "Baez"]
    if any(c in encoded_tweet.lower() for c in keywords):
        testing = video_test(status)
        if testing is True:
            my_status = baez_brain(retweet_link)
            return my_status
            #print("tweeted")
        else:
            x = random.randint(0,99)
            if x > 90:
                my_status = "Steve, Baez spelled backwards is Zeab. \n#EverybodyIn " + retweet_link
                return my_status
                #print("retweeted backwards")
    elif "#cubs" in encoded_tweet.lower() and  "lineup" in encoded_tweet.lower():
        sponsor = ["Pepsi", "Gatorade", "Mountain Dew", "American Airlines"]
        pick = random.choice(sponsor)
        my_status = "Hello again, everybody. Here's today's " + pick + " starting lineup: " + retweet_link
        my_status = "Hello again, everybody. Here's today's {} starting lineup: \n#Cubs #EverybodyIn {}".format(pick, retweet_link)
        time.sleep(7620)
        return my_status

    elif "#kboom" in encoded_tweet.lower():
        hr_call = ["There it goes! Way back...", "There it goes!\nIt might be!\nIt could be...",
                   "There it goes! Back to the wall!\nIt might be!\nIt could be...", "Swung on. Way back!", ""]
        pick = random.choice(hr_call)
        closers = ["Holy cow!", "Listen to the crowd!", "They're dancing in the streets of Las Vegas, Nevada!",
                   "He's a good lookin' fella. Even better looking rounding the bases!", "", ""]
        closing = random.choice(closers)
        testing = video_test(status)
        if testing is True:
            video_calls = ["Arnie, roll the tape again.", "Let's take a look at the Budweiser replay.",
                           "Let's see the replay.", "Arnie, play that again!"]
            video_call = random.choice(video_calls)
        else:
            video_call = ""
        my_status = "{} \n {} {} \n#kboom #EverybodyIn #Cubs \n{}".format(pick, closing, video_call, retweet_link)
        return my_status
    else:
        return None
        #print (tweet.text.encode('utf-8'))



class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if from_creator(status):

            try:
                encoded_tweet = status.text.encode('utf-8')
                tweet_id = status.id
                my_status = harry_brain(status, encoded_tweet, tweet_id)
                if my_status is None:
                    pass

                else:
                    api.update_status(status=my_status)
                    #print(my_status)
                    #print(encoded_tweet)
                    #print(status.user.screen_name)
            except Exception as e:
                print(traceback.format_exc())
                print (e)
                f = open('log.txt', 'w')
                f.write('An exceptional thing happened in harrbot - %s' % e)
                f.close()
            return True
        return True


    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
            # returning non-False reconnects the stream, with backoff.



if __name__ == "__main__":



    myStreamListener = MyStreamListener()

    auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    while True:
        try:
            myStream.filter(follow=['41144996'], stall_warnings=True)
        except Exception as e:
            f = open('log.txt', 'a')
            f.write('An exceptional thing happened in harrbot - %s' % e)
            f.close()
            time.sleep(30)
            continue

#41144996



