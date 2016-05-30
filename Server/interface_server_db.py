import ServerLogic.user_data as ud
from ServerLogic.friendship_data import *
from ServerLogic.searches_logic import *
from time import gmtime, strftime
import traceback

'''
Every function in this module return a tuple of 2:
return-tuple[0] is the data requested or the traceback text in case of an error
return-tuple[1] is the error code- 0 if success, and 1 if failure.
The server checks error code in the server, for every use of this functions
'''

def create_tuples(*fields):
    '''
    extrating user data from db with selected fields, sorted by the second parameter (which should be full_name)
    :param fields:
    :return:sorted list with the chosen fields, th key is screen_name, error code
    '''
    try:
        users_data = ud.get_user_list()
        result = []

        for user in users_data.keys():
            temp = [users_data[user]["screen_name"]]

            for field in fields:
                temp.append(users_data[user][field])
            result.append(temp)

        return sorted(result, key=lambda item: item[1]), 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1


def get_friendship(screen_name_1, screen_name_2):
    '''
    this function generates an html text that gives all the shared data of the two given screen names.
    including: party, role, location, followers and followees
    :param screen_name_1:
    :param screen_name_2:
    :return:html text as described up, error code
    '''
    try:
        if screen_name_1 == screen_name_2:
            html = "<br />You chose to compare the same person! Please choose different persons"
        else:
            users_data = ud.get_user_list()
            shared_info = get_shared_info(screen_name_1, screen_name_2)
            html = ""

            html_pattern = "<br />{0} and {1} are both ".format(users_data[screen_name_1]["full_name"],
                                                                users_data[screen_name_2]["full_name"])
            html_pattern_followers = "<br />{0} and {1} ".format(users_data[screen_name_1]["full_name"],
                                                                 users_data[screen_name_2]["full_name"])
            for key in shared_info.keys():
                if key == "party_name":
                    html += (
                    html_pattern + str_replace(users_data[screen_name_1]["party_name"], "Republican", "Republicans",
                                         "Democratic", "Democrats"))
                if key == "role_name":
                    html += (html_pattern + shared_info["role_name"] + "s")

                if key == "location":
                    html += (html_pattern + "from " + shared_info["location"])

                if key == "followers":
                    followers = shared_info["followers"]
                    followers = followers[0:100]

                    count = len(followers)
                    f = ""

                    for follow in followers:
                        try:
                            f += str(follow) + ", "
                        except:
                            pass
                    f = f[:-2]
                    if f != "":
                        f += "."
                        if count > 1:
                            html += (html_pattern_followers + "have the common followers: " + f)

                        else:
                            html += (html_pattern_followers + "have one common follower: " + f)

                if key == "followees":
                    followees = shared_info["followees"]
                    followees = followees[0:100]
                    f = ""

                    for follow in followees:
                        try:
                            f += str(follow) + ", "
                        except:
                            pass
                    f = f[:-2]

                    if f != "":
                        f += "."
                        html += (html_pattern_followers + "and follow: " + f)
        return html, 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

def get_tweets_shared(screen_name_1, screen_name_2,number):
    '''
    this function generates an html text that gives the number (default=20)
    of shared tweets of the two given screen names.
    :param screen_name_1:
    :param screen_name_2:
    :param num:
    :return:html text as described up, error code
    '''
    try:
        shared = get_shared_tweets(screen_name_1, screen_name_2, number=20)
        shared_tweets = shared[0]
        shared_tweets = shared_tweets[0:num]

        tweets = ""
        count = 1

        for tweet in shared_tweets:
            tweets +="<br /> " + str(count) + ". " + str(tweet)
            count += 1

        return "<br /> The shared Tweets are: " + tweets, 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

def get_tweets_user_mentions(screen_name_1, screen_name_2, number=10):
    '''
    this function generates an html text that gives the number (default=10)
    of mentions in tweets of the two given screen names.
    :param screen_name_1:
    :param screen_name_2:
    :param num:
    :return:html text as described up, error code
    '''
    try:
        users_data = ud.get_user_list()
        shared = get_shared_tweets(screen_name_1, screen_name_2)

        user1_mentions = shared[1]
        user1_mentions = user1_mentions[0:number]
        mention1 = ""
        count = 1
        for mention in user1_mentions:
            mention1 += "<br /> " + str(count) + ". " + str(mention)
            count += 1

        user2_mentions = shared[2]
        user2_mentions = user2_mentions[0:number]

        mention2 = ""
        count = 1
        for mention in user2_mentions:
            mention2 += "<br /> " + str(count) + ". " + str(mention)
            count += 1

        return "<br /> {0} was mentioned in: {1}. {2} was mentioned in: {3}".format(
            users_data[screen_name_2]["full_name"],
            mention1, users_data[screen_name_1]["full_name"], mention2), 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

def get_user_data(screen_name):
    '''
    this function generates an html text that gives personal data of the given screen name:
    profile picture, name, role, location and latest user's tweet.
    :param screen_name:
    :return:html text as described up, error code
    '''
    try:
        user_data = ud.get_user_data(screen_name=screen_name)
        #html = "<br /> <img src={}>".format(user_data["profile_picture_url"])
        html =        "<!DOCTYPE html>\
        <html lang='en'><body><center>"

        html += "<br /> <img src='https://twitter.com/{}/profile_image?size=original' style='width:200px;height:auto'>".format(screen_name)


        html += "<br />{} ".format(user_data["full_name"])
        html += "<br />Is a {} ".format(user_data["role_name"])
        html += "<br />From {} ".format(user_data["location"])
        last_tweets = ud.get_last_tweets(count=1, screen_name=screen_name)
        #last_tweet = ud.get_last_tweets(count=1, screen_name=screen_name)[0]['tweet']['text']
        last_tweet = format_tweet(last_tweets)
        html += "<br /> <br />Last tweet: {} "\
            .format(str(last_tweet))

        return html + "</center></body></html>", 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

def add_href_to_raw_text(string, target="_blank"):
    string = string.encode('utf-8')
    string_array = string.split(" ")
    for i in range(len(string_array)):
        if string_array[i].startswith("http"):
            string_array[i] = "<a href='{0}' target='{1}'>{2}</a>".format(string_array[i], target, string_array[i])
        elif string_array[i].startswith("#"):
            string_array[i] = "<a href='https://twitter.com/hashtag/{0}' target='{1}'>{2}</a>".format(string_array[i][1:], target, string_array[i])
    return " ".join(string_array)

def format_tweet(last_tweets):
    if len(last_tweets) == 0:
        return ""

    else:
        tweet = last_tweets[0]
        return "<a href='https://twitter.com/anyuser/status/{0}' target='_blank'>".format(tweet["tweet"]["tweet_id"]) + str(tweet["tweet"]["date"]) + "</a>" + "<br /><i>" + add_href_to_raw_text(tweet["tweet"]["text"]) + "</i>"

def get_popular_searched(count = 5):
    '''
    this function generates an html text that shows the most popular searches in our application (default=5),
    and date of update.
    :param count:
    :return:html text as described up, error code
    '''
    try:
        searched_list = str(get_popular_users(count).strip('[]'))
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        return "<br /> The most popular congress members searched, till {0} are: {1}".format(get_date(), searched_list), 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

def update_search(screen_name):
    '''
    this function updates a search of a give screen_name in the db, including the date of selection.
    :param screen_name:
    :return:error message in case of error, error code
    '''
    try:
        update_user_search(screen_name, get_date())
        return "", 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

'''
helper functions
'''
def get_date():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())