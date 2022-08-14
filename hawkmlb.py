#!python

from __future__ import print_function
import traceback
from xml.dom.expatbuilder import FragmentBuilderNS
import mlbapi
import random
import tweepy
import hk_twitter_credentials
import time
import requests
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

def get_play_description(most_recent_play, atbat_string):
    try:
        if most_recent_play["result"]["description"] == atbat_string:
                time.sleep(21)
        else:
            play = most_recent_play["result"]["description"]
            return play
    
    except:
        time.sleep(15)


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
    today_date = f"{currentMonth}/{currentDay}/{currentYear}"
    team_schedule = mlbapi.schedule(date = today_date, team_id = 145)
    if team_schedule.total_games == 0:
        break
    game_status = team_schedule.dates[0].games[0].status.detailed_state
    game_pk = team_schedule.dates[0].games[0].game_pk
    home_team = team_schedule.dates[0].games[0].teams.home.team.name 
    away_team = team_schedule.dates[0].games[0].teams.away.team.name 

    if home_team == "Chicago White Sox":
        home_game = True
    else:
        home_game = False

    if game_status == "Game Over" or game_status == "Final":
        try:
            get_play_by_play= mlbapi.get_play_by_play(game_pk)
            most_recent_play = get_play_by_play["allPlays"][-1]
            result = most_recent_play["result"]
            boxscore = mlbapi.boxscore(game_pk)
            people = ["", "", " and Tom Paciorek",
                    " and 'Wimpy'", " and DJ"]
            pick = random.choice(people)
            sayings = "This is Hawk Harrelson with Stoney" + pick
            if home_game == False:
                sox_runs = result["awayScore"]
                sox_hits = boxscore.teams.away.team_stats.batting.hits
                sox_errors = boxscore.teams.away.team_stats.fielding.errors
                oppo_runs = result["homeScore"]
                oppo_hits = boxscore.teams.home.team_stats.batting.hits
                oppo_errors = boxscore.teams.home.team_stats.fielding.errors
                oppo_team = home_team

            else:
                sox_runs = result["homeScore"]
                sox_hits = boxscore.teams.home.team_stats.batting.hits
                sox_errors = boxscore.teams.home.team_stats.fielding.errors
                oppo_runs = result["awayScore"]
                oppo_hits = boxscore.teams.away.team_stats.batting.hits
                oppo_errors = boxscore.teams.away.team_stats.fielding.errors
                oppo_team = away_team
            if sox_runs > oppo_runs:
                sox_win = True
            else: sox_win = False 
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
            if sox_win:
                openers = ["#WhiteSox win!", "This game is ovah!", "Sox win!",
                        "Sox win! Hell yes!"]
                opener = random.choice(openers)

            else:
                openers = ["(30 seconds of silence)",
                        "Sox lose today."]
                opener = random.choice(openers)

            my_status = """{opner} The score: The #WhiteSox {sox_runs} and the {oppo_team} {oppo_runs}. Your totals:\nFor the Sox. {sox_runs} {sox_r}, {sox_hits} {sox_h} and {sox_errors} {sox_e}.\nFor the {oppo_team}, {oppo_runs} {oppo_r}, {oppo_hits} {oppo_h} and {oppo_errors} {oppo_e}. \n{sayings}. Goodnight."""
            # print(my_status)
            api.update_status(status=my_status)
            time.sleep(30)
            
        except Exception as e:
            q = (str(datetime.now()))
            f = open('hawklog.txt', 'a')
            f.write('An exceptional Hawkbot thing happened - {}'.format(e))
            f.write(q)
            f.close()
            time.sleep(30)
    break

    elif game_status == "In Progress":
        try:
            get_play_by_play= mlbapi.get_play_by_play(game_pk)
            most_recent_play = get_play_by_play["allPlays"][-1]
            this_half = most_recent_play["about"]["halfInning"]
            this_inning = most_recent_play["about"]["inning"]
            if home_game == False and this_half == "top":
                atbat_string = get_play_description(most_recent_play, atbat_string)
                # atbat_string = most_recent_play["result"]["description"] 
                # print(atbat_string)

            elif home_game == True and this_half == "bottom":
                atbat_string = get_play_description(most_recent_play, atbat_string)
                # print(atbat_string)

                # atbat_string = most_recent_play["result"]["description"] 
            elif home_game == True and this_half == "top":
                defense_string = get_play_description(most_recent_play, atbat_string)

            elif home_game == False and this_half == "bottom":
                defense_string =get_play_description(most_recent_play, atbat_string)

            else:
                atbat_string = happened
                print(atbat_string)

                time.sleep(9)

            if atbat_string and happened != atbat_string:
                if "homer" in atbat_string:
                    homer_calls = ["Hit hard! He looks up! You can put it on the boaaard! Yes! \n",
                                   "That ball hit deep! You can put in on the board! Yes!!\n", "Stretch! That ball is gone! Mercy!\n"]
                    homer_call = random.choice(homer_calls)
                    if home_game == True:
                        closer = "\nThe home crowd loves it!\n#WhiteSox"
                    else:
                        closer = "\n#WhiteSox"
                    my_status = homer_call + atbat_string + closer
                    api.update_status(status=my_status)
                    happened = atbat_string
                    time.sleep(51)

                elif "grand" in atbat_string:
                    homer_calls = ["You can put it on the boooooard! Yes! Grand slam! \n",
                                   "Hit hard! Stretch! Grand slam! MERCY!!!...\n"]
                    homer_call = random.choice(homer_calls)
                    if home_game == True:
                        closer = "\nComiskey is going wild!\n#WhiteSox @WhiteSox"
                    else:
                        closer = "\n#WhiteSox @WhiteSox"
                    my_status = homer_call + atbat_string + closer
                    api.update_status(status=my_status)
                    # print(my_status)
                    happened = atbat_string
                    time.sleep(51)

                elif "flies out" in atbat_string and "sharply" not in atbat_string:
                    the_calls = ["\nCan of corn.\n"]
                    my_status = atbat_string + "\nCan of corn.\n"
                    will_it_run = random.randint(0, 246)
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
                    # if this_inning == 4 and stats.away_team == "White Sox" and this_half == "top":
                    #     harry_news(stats.home_team, stats.home_team_runs,
                    #                stats.away_team, stats.away_team_runs)
                    # if this_inning == 4 and stats.home_team == "White Sox" and this_half == "bottom":
                    #     harry_news(stats.home_team, stats.home_team_runs,
                    #                stats.away_team, stats.away_team_runs)

                if happened != defense_string:
                    if "strikes out" in defense_string:
                        closer = "\n#WhiteSox"
                        my_status = "HE GONE! \n" + defense_string + closer
                        will_it_run = random.randint(0, 100)
                        if will_it_run < 50:
                            api.update_status(status=my_status)

                        happened = defense_string
                        time.sleep(51)

                    if "walks" in defense_string:
                        closer = "\n#WhiteSox #umpirestrikesback"
                        my_status = "Where was that? \n" + defense_string + closer
                        will_it_run = random.randint(0, 100)
                        if will_it_run < 36:
                            api.update_status(status=my_status)
                            api.update_status(status=my_status)

                        happened = defense_string
                        time.sleep(51)

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
