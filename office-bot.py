#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# A Twitter bot that tweets random quotes from "The Office".
# Created by Adam Bartholomew.

# Standard libraries.
import tweepy
import datetime
import time
import logging
import random
from playsound import playsound
import os

# Custom imports.
import config
import lib.quoteDict as quoteDict

# Get config info.
CONSUMER_KEY = config.get_property("consumer_key")
CONSUMER_SECRET = config.get_property("consumer_secret")
ACCESS_TOKEN = config.get_property("access_token")
ACCESS_SECRET = config.get_property("access_secret")
SLEEP_FOR = int(config.get_property("sleep_for"))
DATE_FORMAT = config.get_property("logging_date_format")
LOG_FORMAT = config.get_property("log_format")
BASE_LOG_DIR = config.get_property("base_log_dir")
BASE_LOG_EXT = config.get_property("base_log_extension")
USE_CONN = config.get_use_connection()
SOUND_DIR = config.get_property("sound_dir")

# Create variables.
log_filename = BASE_LOG_DIR + "twitter-bot_" + datetime.datetime.now().strftime("%Y%m%d") + BASE_LOG_EXT
logging.basicConfig(filename=log_filename, format=LOG_FORMAT, level=logging.INFO, datefmt=DATE_FORMAT)
log = logging.getLogger()
sleep_time = datetime.timedelta(seconds=int(SLEEP_FOR))
used_quotes = {}


# Setup connection with Twitter.
def connect() -> tweepy.API:
    log.info(f"Attempting to connect to Twitter")
    try:
        auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    except tweepy.TweepyException as err:
        log.error(f"Exception in connect(). Connection could not be made. {err}")
    else:
        return tweepy.API(auth, wait_on_rate_limit=True)


# Sends a tweet given the line and connection to the api.
# @param: quote - The quote being used.
# @param: tweet - The actual tweet being delivered.
# @param: conn - The tweepy api connection.
# Returns: Boolean
def send_tweet(quote: str, tweet: str, conn: tweepy.API) -> bool:
    if tweet and isinstance(tweet, str) and len(tweet) <= 280:
        if USE_CONN:
            try:
                conn.update_status(status=tweet)
            except tweepy.TweepyException as err:
                log.error(f"Encountered an error while sending a tweet: {err}")
            else:
                log.info(f"USE_CONN={USE_CONN} | Tweet sent: {tweet}")
                print(f"USE_CONN={USE_CONN} | Tweet sent: {tweet}")
        else:
            log.info(f"USE_CONN={USE_CONN} | Tweet not sent: {tweet}")
            print(f"USE_CONN={USE_CONN} | Tweet not sent: {tweet}")
        quoteDict.increase_used_by_one(quote)
        return True
    log.warning(f"office-bot.send_tweet(): Reached the end of the function without returning anything, the tweet may be too long for twitter.")


# Get the last tweet sent.
# @param: conn - The tweepy api connection.
def get_last_tweet(conn: tweepy.API) -> str | None:
    log.info(f"Getting the last tweet sent by this user.")
    try:
        name = conn.verify_credentials().screen_name
        last_tweet = conn.user_timeline(screen_name=name, count=1)[0].text
        log.info(f"Got the last tweet sent for {name}: \"{last_tweet}\"")
        return last_tweet
    except tweepy.TweepyException as err:
        log.error(f"Encountered an error when retrieving last tweet: {err}")
        return None


# Chooses a quote from the dictionary.
# Returns: String, String
def get_quote() -> (str, str):
    log.info(f"Choosing quote...")

    possible_options = quoteDict.get_least_used_dict()
    random.seed()
    msg = ""

    while msg == "":
        index = random.randint(0, len(possible_options) - 1)
        quote = list(possible_options.keys())[index]
        quote_speaker = (list(possible_options.values())[index]).get('source')
        msg = "\"%s\" - %s" % (quote, quote_speaker)

        # Check to make sure the tweet is not too long.
        if len(msg) > 280:
            log.debug(f"Built a tweet but it is too long, starting over.")
            msg = ""
        else:
            log.info(f"Quote selected \"{quote}\": {str(quoteDict.quote_dict[quote])}")
            return quote, msg


# Follows someone back if they follow this account.
# @param: conn - The tweepy api connection.
def check_followers(conn: tweepy.API):
    log.info(f"Checking {conn.verify_credentials().screen_name}'s followers")

    if USE_CONN:
        try:
            for follower in conn.get_followers():
                if not follower.following:
                    try:
                        conn.create_friendship(screen_name=follower.screen_name, user_id=follower.id)
                    except tweepy.TweepyException as err:
                        log.debug(f"An unknown exception occurred while trying to follow '{follower.screen_name}': {err}")
                    else:
                        log.info(f"ALERT - Now following: {follower.screen_name}")
                    finally:
                        log.info(f"All followers are now followed. FOLLOWER CHECK COMPLETE.")
        except tweepy.TweepyException as err:
            log.error(f"An exception occurred in check_followers: {err}")
    else:
        log.info(f"USE_CONN is {USE_CONN}, not doing anything.")


# Manages the process of sending a tweet.
# @param: conn - The tweepy api connection.
def iteration(conn: tweepy.API) -> bool:
    log.info(f"Start of a new iteration")
    quote, tweet = get_quote()
    while tweet == get_last_tweet(conn):
        quote, tweet = get_quote()
    if send_tweet(quote, tweet, conn):
        sound_file = SOUND_DIR + random.choice(os.listdir(SOUND_DIR))
        playsound(sound_file)
        log.info(f"Played the sound: {sound_file}")
        return True
    else:
        log.error(f"Caught a tweepy error, trying again...")
        print(f"Caught a tweepy error, trying again...")
        return False


# Gets the "Best Friend", the user with whom we interacted with the most
# @param: conn - The tweepy api connection.
def get_best_friend(conn: tweepy.API):
    log.info(f"Getting {conn.verify_credentials().screen_name}'s best friend")
    followers = dict()
    followers[conn.verify_credentials().id] = {}
    followers[conn.verify_credentials().id]['screen_name'] = conn.verify_credentials().screen_name
    followers[conn.verify_credentials().id]['num_dms'] = 0

    if USE_CONN:
        for follower in conn.get_followers():
            followers[follower.id] = {}
            followers[follower.id]['screen_name'] = follower.screen_name
            followers[follower.id]['num_dms'] = 0

        log.info(f"Grabbing direct messages")
        for dm in conn.get_direct_messages():
            print(dm)
            if int(dm.message_create['sender_id']) in followers:
                followers[int(dm.message_create['sender_id'])]['num_dms'] += 1

        # If possible continue this function here - grab retweets/likes
    else:
        log.debug(f"USE_CONN is {USE_CONN}, not doing anything")

    print(followers)


# Main function.
def main():
    log.info(f"Starting up for the first time")
    log.info(f"Property use_connection: - {USE_CONN}")

    try:
        conn = connect()
    except tweepy.TweepyException as err:
        log.warning(f"Connection could not be made to Twitter: - {err}")
    else:
        log.info(f"Connection made successfully")
        while conn:
            log.info(f"Start of connection loop.")
            check_followers(conn)
            did_tweet = iteration(conn)
            while did_tweet is False:
                did_tweet = iteration(conn)
            # else:
            log.info(f"Going to sleep for {sleep_time}")
            print(f"Sleeping...")
            time.sleep(SLEEP_FOR)
        log.debug(f"The tweepy connection was lost.")
        print(f"Tweepy connection lost...exiting.")


if __name__ == "__main__":
    log.info(f"Calling __main__")
    main()

    # Do any testing here, but first comment out main():
    #conn = connect()
    #get_last_tweet(conn)
    #get_best_friend(conn)
    #quoteDict.export_current_dicts_csv("C:\\Users\\adamb\\OneDrive\\Desktop\\Quotes\\exports\\test_export.csv", "C:\\Users\\adamb\\OneDrive\\Desktop\\Quotes\\exports\\test_export_2.csv")
    #quoteDict.export_current_dicts_json("C:\\Users\\adamb\\OneDrive\\Desktop\\Quotes\\exports\\test_export.json", "C:\\Users\\adamb\\OneDrive\\Desktop\\Quotes\\exports\\test_export_2.json")
    #quote, tweet = "1234567890"*28+"A", "1234567890"*28+"A"
    #send_tweet(quote, tweet, connect())
