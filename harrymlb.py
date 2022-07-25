#!python
# 8/30 3pm
from __future__ import print_function
import traceback
from xml.dom.expatbuilder import FragmentBuilderNS
import mlbgame
import mlbapi
import random
import tweepy
import twitter_credentials
import time
from datetime import datetime
from pytz import timezone

# puts on timer for 15 hours
start = time.time()
PERIOD_OF_TIME = 59100

auth = tweepy.OAuthHandler(
    twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                      twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

currentDay = datetime.now(timezone('America/Los_Angeles')).day
currentMonth = datetime.now(timezone('America/Los_Angeles')).month
currentYear = datetime.now(timezone('America/Los_Angeles')).year
happened = False
atbat_string = happened


def run_once(f):
    # wrapper allows function to run only once
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper



def harry_news(a, b, c, d):
    username = 'ChicagoSports'
    tweets = api.user_timeline(
        screen_name=username, count=9, include_rts=False)
    for tweet in tweets:
        try:
            encoded_tweet = tweet.text.encode('utf-8')
            if 'cubs' in encoded_tweet.lower():
                retweet_link = 'https://twitter.com/ChicagoSports/status/' + \
                    str(tweet.id)
                retweet_news(a, b, c, d, retweet_link)
        except tweepy.TweepError as e:
            print(e.reason)
            f = open('log.txt', 'a')
            f.write('An exceptional thing happened - {}'.format(e))
            f.close()
            sleep(9)
            continue
        except StopIteration:
            break


@run_once
def retweet_news(a, b, c, d, retweet_link):
    options = ["""Steve, I read something interesting in the Chicago Tribune earlier today:
                \n#Cubs #CubTogether\n {}""".format(retweet_link),
               """There was an excellent article in the Tribune I saw:
               \n#Cubs #CubTogether\n{}""".format(retweet_link)]
    pick = random.choice(options)
    game_score = """The Cubs are getting ready to bat here in the fourth. The score is the {} {} and the {} {}.\n""".format(
        a, b, c, d)
    my_status = game_score + pick
    api.update_status(status=my_status)


@run_once
def flip_it(oppo_pitcher, oppo_roster, oppo_team):
    will_it_run = random.randint(0, 27)
    if will_it_run > 2:
        roster_dict = {}
        for i in oppo_roster:
            roster_dict[i.id] = i.last
        l_name = roster_dict[oppo_pitcher]
        backname = l_name[::-1].capitalize()
        options = ["Here's a pitcher on the mound for the {} with the last name {}. Steve, let me try this...\n{} spelled backwards is {}. ".format(oppo_team, l_name, l_name, backname),
                   "{} is pitching for the {}. Let's see....{} spelled backwards is {}.... \nWhat's that Arnie?...That's what I said, {}. ".format(l_name, oppo_team, l_name, backname, backname)]
        pick = random.choice(options)
        closers = ["I think I'm saying that right. \n\n#Cubs",
                   "\n\n#Cubs",
                   "\n\n#Cubs"]
        closer = random.choice(closers)
        pick = pick + closer
        my_status = pick
        api.update_status(status=my_status)
        # print(my_status)
        #print("flipit works")


while(True):
    today_date = f"{currentMonth}/{currentDay}/{currentYear}"
    today_game = mlbgame.day(currentYear, currentMonth,
                             currentDay, home="Cubs", away="Cubs")
    team_schedule = mlbapi.schedule(date = today_date, team_id = 112)
    if team_schedule.total_games == 0:
        break
    # stats = today_game[0]
    # rosters = mlbgame.players(stats.game_id)

    game_status = team_schedule.dates[0].games[0].status.detailed_state
    game_pk = team_schedule.dates[0].games[0].game_pk
    home_team = team_schedule.dates[0].games[0].teams.home.team.name 
    away_team = team_schedule.dates[0].games[0].teams.away.team.name 
    if home_team == "Chicago Cubs":
        home_game = True
    else:
        home_game = False

    if game_status == "Final":
        get_play_by_play= mlbapi.get_play_by_play(game_pk)
        most_recent_play = get_play_by_play["allPlays"][-1]
        result = most_recent_play["result"]
        boxscore = mlbapi.boxscore(game_pk)
        people = ["", "", " and Wayne Larrivee", " and Arnie Harris", " and Thom Brennaman", " and Lou Boudreau",
                  " and Milo Hamilton"]
        pick = random.choice(people)
        sayings = "This is Harry Caray with Steve Stone" + pick
        if home_game == False:
            cubs_runs = result["awayScore"]
            cubs_hits = boxscore.teams.away.team_stats.batting.hits
            cubs_errors = boxscore.teams.away.team_stats.fielding.errors
            oppo_runs = result["homeScore"]
            oppo_hits = boxscore.teams.home.team_stats.batting.hits
            oppo_errors = boxscore.teams.home.team_stats.fielding.errors
            oppo_team = home_team

        else:
            cubs_runs = result["homeScore"]
            cubs_hits = boxscore.teams.home.team_stats.batting.hits
            cubs_errors = boxscore.teams.home.team_stats.fielding.errors
            oppo_runs = result["awayScore"]
            oppo_hits = boxscore.teams.away.team_stats.batting.hits
            oppo_errors = boxscore.teams.away.team_stats.fielding.errors
            oppo_team = away_team
        if cubs_runs > oppo_runs:
            cubs_win = True
        else: cubs_win = False 
            
        cub_h = "hits"
        cub_r = "runs"
        cub_e = "errors"
        oppo_h = "hits"
        oppo_r = "runs"
        oppo_e = "errors"
        if cubs_runs == 1:
            cub_r = "run"
        if cubs_hits == 1:
            cub_h = "hit"
        if cubs_errors == 1:
            cub_e = "error"
        if oppo_runs == 1:
            oppo_r = "run"
        if oppo_hits == 1:
            oppo_h = "hit"
        if oppo_errors == 1:
            oppo_e = "error"
        if cubs_win:
            openers = ["#Cubs win! Cubs win!",
                       "#Cubs win! The good Lord loves the Cubs!", "Holy cow!"]
            opener = random.choice(openers)

        else:
            openers = ["That's it for today.",
                       "A tough loss today." "It's a tough loss."]
            opener = random.choice(openers)

        my_status = f"{opener} The final: The Cubs {cubs_runs} and the {oppo_team} {oppo_runs}. Your totals:\nFor the Cubs. {cubs_runs} {cub_r}, {cubs_hits} {cub_h} and {cubs_errors} {cub_e}.\nFor the {oppo_team}, {oppo_runs} {oppo_r}, {oppo_hits} {oppo_h} and {oppo_errors} {oppo_e}. \n{sayings}. Goodnight, everybody. \n#Cubs #CubTogether"
        print(my_status)
        # api.update_status(status=my_status)
        time.sleep(90)
        # print(my_status)

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

            if stats.away_team == "Cubs" and this_half == "top":
                atbat_string = atbat.nice_output()

            elif stats.home_team == "Cubs" and this_half == "bottom":
                atbat_string = atbat.nice_output()

            else:
                atbat_string = happened
                time.sleep(12)
                # print(atbat.b,atbat.s,atbat.o,atbat.away_team_runs,atbat.home_team_runs)

            if happened != atbat_string:
                if "homer" in atbat_string:
                    homer_calls = ["There it goes! Way back! It might be! It could be! It is! \n",
                                   "There it goes! Way back...\n", "Swung on. Way back! It might be...\n"]
                    homer_call = random.choice(homer_calls)
                    if stats.home_team == "Cubs":
                        closer = "\nListen to the crowd!\n\n#CubTogether #Cubs"
                    else:
                        closer = "\n#CubTogether #Cubs"
                    my_status = homer_call + atbat_string + closer
                    api.update_status(status=my_status)
                    # print(my_status)
                    happened = atbat_string
                    time.sleep(51)

                elif "grand" in atbat_string:
                    homer_calls = ["There it goes! Way back! Grand slam! Grand slam! \n",
                                   "There it goes! A grand slam! Holy cow!...\n"]
                    homer_call = random.choice(homer_calls)
                    if stats.home_team == "Cubs":
                        closer = "\nListen to the crowd!\n\n#CubTogether #Cubs @Cubs"
                    else:
                        closer = "\n#CubTogether #Cubs @Cubs"
                    my_status = homer_call + atbat_string + closer
                    api.update_status(status=my_status)
                    # print(my_status)
                    happened = atbat_string
                    time.sleep(51)

                elif this_inning == 3 and stats.away_team == "Cubs" and this_half == "top":
                    flip_it(atbat.pitcher, oppo_roster, oppo_team)
                    happened = atbat_string
                elif this_inning == 3 and stats.home_team == "Cubs" and this_half == "bottom":
                    flip_it(atbat.pitcher, oppo_roster, oppo_team)
                    happened = atbat_string

                else:
                    happened = atbat_string
                    if this_inning == 4 and stats.away_team == "Cubs" and this_half == "top":
                        harry_news(stats.home_team, stats.home_team_runs,
                                   stats.away_team, stats.away_team_runs)
                    if this_inning == 4 and stats.home_team == "Cubs" and this_half == "bottom":
                        harry_news(stats.home_team, stats.home_team_runs,
                                   stats.away_team, stats.away_team_runs)
                    # if this_inning == 9:
                    #    if stats.home_team == "Cubs" and this_half == "top":
                    #        relief(stats.home_team_runs, stats.away_team_runs)
                    #    else:
                     #       relief(stats.away_team_runs, stats.home_team_runs)

                    # time.sleep(6)

        except Exception as e:
            print(traceback.format_exc())
            print(e)
            f = open('log.txt', 'a')
            f.write('An exceptional thing happened - {}'.format(e))
            f.close()
            time.sleep(3)
    else:

        time.sleep(45)

    if time.time() > start + PERIOD_OF_TIME:
        break
