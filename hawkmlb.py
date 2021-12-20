#!python

from __future__ import print_function
import traceback
import mlbgame
import random
import tweepy
import hk_twitter_credentials
import time
from datetime import datetime
from pytz import timezone

# puts on timer for 15 hours
start = time.time()
PERIOD_OF_TIME = 59100

auth = tweepy.OAuthHandler(
    hk_twitter_credentials.CONSUMER_KEY, hk_twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(hk_twitter_credentials.ACCESS_TOKEN,
                      hk_twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

currentDay = datetime.now(timezone('America/Los_Angeles')).day
currentMonth = datetime.now(timezone('America/Los_Angeles')).month
currentYear = datetime.now(timezone('America/Los_Angeles')).year
happened = False
atbat_string = happened
defense_string = None


def run_once(f):
    # wrapper allows function to run only once
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

# @run_once
# def relief(cubs_runs, oppo_runs):
#    pass


def harry_news(a, b, c, d):
    username = 'ChicagoSports'
    tweets = api.user_timeline(
        screen_name=username, count=9, include_rts=False)
    for tweet in tweets:
        try:
            encoded_tweet = tweet.text.encode('utf-8')
            if 'white sox' in encoded_tweet.lower():
                retweet_link = 'https://twitter.com/ChicagoSports/status/' + \
                    str(tweet.id)
                retweet_news(a, b, c, d, retweet_link)
        except tweepy.TweepError as e:
            f = open('log.txt', 'a')
            f.write('An exceptional Hawkbot thing happened - {}'.format(e))
            f.close()
            time.sleep(9)
            continue
        except StopIteration:
            break


@run_once
def retweet_news(a, b, c, d, retweet_link):
    options = ["""DJ, I read something interesting in the Tribune earlier today:
                \n#WhiteSox #ChangeTheGame\n {}""".format(retweet_link),
               """There was an article from our friends in the Trib I saw:
               \n#WhiteSox #ChangeTheGame\n{}""".format(retweet_link)]
    pick = random.choice(options)
    game_score = """The good guys are getting ready to come to the plate. Score is {} {} and the {} {}.\n""".format(
        a, b, c, d)
    my_status = game_score + pick
    api.update_status(status=my_status)


while(True):
    today_game = mlbgame.day(currentYear, currentMonth,
                             currentDay, home="White Sox", away="White Sox")
    print(today_game)
    if today_game == []:
        break
    stats = today_game[0]
    rosters = mlbgame.players(stats.game_id)

    if stats.away_team == "White Sox":
        oppo_team = stats.home_team
        oppo_roster = rosters.home_players

    else:
        oppo_team = stats.away_team
        oppo_roster = rosters.away_players

    if stats.game_status == "FINAL":

        people = ["", "", " and Tom Paciorek",
                  " and 'Wimpy'", " and DJ", " and Darrin Jackson"]
        pick = random.choice(people)
        sayings = "This is Hawk Harrelson with Steve Stone" + pick
        if stats.away_team == "White Sox":
            sox_runs = stats.away_team_runs
            sox_hits = stats.away_team_hits
            sox_errors = stats.away_team_errors
            oppo_runs = stats.home_team_runs
            oppo_hits = stats.home_team_hits
            oppo_errors = stats.home_team_errors
            oppo_team = stats.home_team

        else:
            sox_runs = stats.home_team_runs
            sox_hits = stats.home_team_hits
            sox_errors = stats.home_team_errors
            oppo_runs = stats.away_team_runs
            oppo_hits = stats.away_team_hits
            oppo_errors = stats.away_team_errors
            oppo_team = stats.away_team
        sox_h = "hits"
        sox_r = "runs"
        sox_e = "errors"
        oppo_h = "hits"
        oppo_r = "runs"
        oppo_e = "errors"
        if sox_runs == 1:
            sox_r = "run"
        if sox_hits == 1:
            sox_h = "hit"
        if sox_errors == 1:
            sox_e = "error"
        if oppo_runs == 1:
            oppo_r = "run"
        if oppo_hits == 1:
            oppo_h = "hit"
        if oppo_errors == 1:
            oppo_e = "error"
        if stats.w_team == "White Sox":
            openers = ["#WhiteSox win!", "This game is ovah!", "This game is ovah! Sox win!",
                       "#WhiteSox win! Hell yes!", "Good guys win!", "South Siders win!"]
            opener = random.choice(openers)

        else:
            openers = ["(30 seconds of silence)",
                       "Tough day for the Sox.", "White Sox lose today.", "South Siders lose."]
            opener = random.choice(openers)

        my_status = """{} The score: The #WhiteSox {} and the {} {}. Here are your totals:\nFor the Sox. {} {}, {} {} and {} {}.\nFor the {}, {} {}, {} {} and {} {}. \n{}. Goodnight. \n#ChangeTheGame""".format(opener, sox_runs, oppo_team, oppo_runs, sox_runs, sox_r, sox_hits, sox_h,
                                                                                                                                                                                                                  sox_errors, sox_e,
                                                                                                                                                                                                                  oppo_team, oppo_runs, oppo_r, oppo_hits,
                                                                                                                                                                                                                  oppo_h, oppo_errors, oppo_e,
                                                                                                                                                                                                                  sayings)
        # print(my_status)
        api.update_status(status=my_status)
        time.sleep(90)

        break

    elif stats.game_status == "IN_PROGRESS":
        try:
            events = mlbgame.game_events(stats.game_id)
            this_inning = len(events)
            for event in events:
                if(event.num == this_inning):
                    break

            if(len(event.bottom) == 0):
                this_half = "top"
                this_atbat = event.top[-1]

            else:
                this_half = "bottom"
                this_atbat = event.bottom[-1]

            atbat = this_atbat

            # if(not atbat):
            #    atbat_string = "Changing Innings"
            # when sox are at bat
            if stats.away_team == "White Sox" and this_half == "top":
                atbat_string = atbat.nice_output()

            elif stats.home_team == "White Sox" and this_half == "bottom":
                atbat_string = atbat.nice_output()

            # when sox are on field
            elif stats.home_team == "White Sox" and this_half == "top":
                defense_string = atbat.nice_output()

            elif stats.away_team == "White Sox" and this_half == "bottom":
                defense_string = atbat.nice_output()

            else:
                atbat_string = happened
                defense_string = happened
                time.sleep(6)
                # print(atbat.b,atbat.s,atbat.o,atbat.away_team_runs,atbat.home_team_runs)

            if happened != atbat_string:
                print("here")
                print(happened)
                print(atbat_string)
                if "homer" in atbat_string:
                    homer_calls = ["Hit hard! He looks up! You can put it on the boaaard! Yes! \n",
                                   "That ball hit deep! You can put in on the board! Yes!!\n", "Stretch! That ball is gone! Mercy!\n"]
                    homer_call = random.choice(homer_calls)
                    if stats.home_team == "White Sox":
                        closer = "\nThe home crowd loves it!\n\n#ChangeTheGame #WhiteSox"
                    else:
                        closer = "\n#ChangeTheGame #WhiteSox"
                    my_status = homer_call + atbat_string + closer
                    api.update_status(status=my_status)
                    happened = atbat_string
                    time.sleep(60)

                elif "grand" in atbat_string:
                    homer_calls = ["You can put it on the boooooard! Yes! Grand slam! \n",
                                   "Hit hard! Stretch! Grand slam! MERCY!!!...\n"]
                    homer_call = random.choice(homer_calls)
                    if stats.home_team == "White Sox":
                        closer = "\nComiskey is going wild!\n\n#ChangeTheGame #WhiteSox @WhiteSox"
                    else:
                        closer = "\n#ChangeTheGame #WhiteSox @WhiteSox"
                    my_status = homer_call + atbat_string + closer
                    api.update_status(status=my_status)
                    # print(my_status)
                    happened = atbat_string
                    time.sleep(60)

                elif "flies out" in atbat_string and "sharply" not in atbat_string:
                    the_calls = ["\nCan of corn.\n"]
                    my_status = atbat_string + "\nCan of corn.\n"
                    will_it_run = random.randint(0, 240)
                    if will_it_run < 6:
                        api.update_status(status=my_status)
                        # print(my_status)
                        happened = atbat_string
                        time.sleep(27)

                # elif this_inning == 3 and stats.away_team == "White Sox" and this_half == "top":
                #     flip_it(atbat.pitcher, oppo_roster, oppo_team)
                #     happened = atbat_string
                # elif this_inning == 3 and stats.home_team == "White Sox" and this_half == "bottom":
                #     flip_it(atbat.pitcher, oppo_roster, oppo_team)
                #     happened = atbat_string

                else:
                    happened = atbat_string
                    if this_inning == 4 and stats.away_team == "White Sox" and this_half == "top":
                        harry_news(stats.home_team, stats.home_team_runs,
                                   stats.away_team, stats.away_team_runs)
                    if this_inning == 4 and stats.home_team == "White Sox" and this_half == "bottom":
                        harry_news(stats.home_team, stats.home_team_runs,
                                   stats.away_team, stats.away_team_runs)

                if happened != defense_string:
                    if "strikes out" in defense_string:
                        closer = "\n#ChangeTheGame #WhiteSox #HeGone"
                        my_status = "HE GONE! \n" + defense_string + closer
                        will_it_run = random.randint(0, 100)
                        if will_it_run < 50:
                            api.update_status(status=my_status)

                        happened = defense_string
                        time.sleep(60)

                    if "walks" in defense_string:
                        closer = "\n#ChangeTheGame #WhiteSox #umpirestrikesback"
                        my_status = "Where was that? \n" + defense_string + closer
                        will_it_run = random.randint(0, 100)
                        if will_it_run < 50:
                            api.update_status(status=my_status)
                            api.update_status(status=my_status)

                        happened = defense_string
                        time.sleep(60)

        except Exception as e:
            q = (str(datetime.now()))
            f = open('hawklog.txt', 'a')
            f.write('An exceptional Hawkbot thing happened - {}'.format(e))
            f.write(q)
            f.close()
            time.sleep(3)
    else:

        time.sleep(42)

    if time.time() > start + PERIOD_OF_TIME:
        break
