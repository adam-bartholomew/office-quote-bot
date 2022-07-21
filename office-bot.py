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

# Custom libraries.
import config
import lib.quoteDict as quoteDict

# Get config info.
CONSUMER_KEY = config.properties["consumer_key"]
CONSUMER_SECRET = config.properties["consumer_secret"]
ACCESS_TOKEN = config.properties["access_token"]
ACCESS_SECRET = config.properties["access_secret"]
SLEEP_FOR = int(config.properties["sleep_for"])
DATE_FORMAT = config.properties["logging_date_format"]
LOG_FORMAT = config.properties["log_format"]
BASE_LOG_DIR = config.properties["base_log_dir"]
BASE_LOG_EXT = config.properties["base_log_extension"]
USE_CONN = config.get_use_connection()

# Create variables.
log_filename = BASE_LOG_DIR + "twitter-bot_" + datetime.datetime.now().strftime("%Y%m%d") + BASE_LOG_EXT
logging.basicConfig(filename=log_filename, format=LOG_FORMAT, level=logging.DEBUG, datefmt=DATE_FORMAT)
log = logging.getLogger()
sleep_time = datetime.timedelta(seconds=int(SLEEP_FOR))
used_quotes = {}


# Setup connection with Twitter.
def connect():
    log.info(f"Attempting to connect to Twitter.")
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)


# Sends a tweet given the line and connection to the api.
#   quote - what the tweet will be.
#   conn  - tweepy api connection.
def send_tweet(quote, tweet, conn):
    if tweet and isinstance(tweet, str):
        try:
            if USE_CONN:
                conn.update_status(status=tweet)
                log.info(f"USE_CONN={USE_CONN} | Tweet sent: {tweet}")
                print(f"USE_CONN={USE_CONN} | Tweet sent: {tweet}")
            log.info(f"USE_CONN={USE_CONN} | Tweet not sent: {tweet}")
            print(f"USE_CONN={USE_CONN} | Tweet not sent: {tweet}")
            quoteDict.increase_used_by_one(quote)
            return True
        except tweepy.TweepyException as err:
            log.error(f"Error occurred sending tweet: {err}")
            return False


# Chooses a quote from the dictionary.
def get_quote():
    log.info(f"Choosing quote...")

    possible_options = quoteDict.get_least_used_dict()
    random.seed()
    index = random.randint(0, len(possible_options) - 1)

    quote = list(possible_options.keys())[index]
    quote_speaker = (list(possible_options.values())[index]).get('source')
    msg = "\"%s\" - %s" % (quote, quote_speaker)
    log.info(f"Quote selected \"{quote}\": {str(quoteDict.quote_dict[quote])}")

    return quote, msg


# Follows someone back if they follow this account.
#   conn  - tweepy api connection.
def check_followers(conn):
    log.info(f"Checking {conn.verify_credentials().screen_name}'s followers")

    if USE_CONN:
        for follower in conn.get_followers():
            if not follower.following:
                try:
                    conn.create_friendship(follower.screen_name, follower.id)
                except tweepy.TweepyException as err:
                    log.info(f"An unknown exception occurred while trying to follow '{follower.screen_name}': {err}")
                else:
                    log.info(f"ALERT: Now following {follower.screen_name}!")
        log.info(f"All followers are now followed.\nFOLLOWER CHECK COMPLETE.")
    else:
        log.info(f"USE_CONN is {USE_CONN}, not doing anything.")


# Manages the process of sending a tweet.
#   conn  - tweepy api connection.
def iteration(conn):
    log.info(f"Start of a new iteration.")
    quote, tweet = get_quote()
    if send_tweet(quote, tweet, conn):
        return True
    else:
        log.error(f"Caught a tweepy error, trying again...")
        print(f"Caught a tweepy error, trying again...")
        return False


# Gets the "Best Friend", the user with whom we interacted with the most
#   conn  - tweepy api connection.
def get_best_friend(conn):
    log.info(f"Getting {conn.verify_credentials().screen_name}'s best friend.")
    followers = dict()
    followers[conn.verify_credentials().id] = {}
    followers[conn.verify_credentials().id]['screen_name'] = conn.verify_credentials().screen_name
    followers[conn.verify_credentials().id]['num_dms'] = 0

    if USE_CONN:
        for follower in conn.get_followers():
            followers[follower.id] = {}
            followers[follower.id]['screen_name'] = follower.screen_name
            followers[follower.id]['num_dms'] = 0

        log.info(f"Grabbing direct messages.")
        for dm in conn.get_direct_messages():
            print(dm)
            if int(dm.message_create['sender_id']) in followers:
                followers[int(dm.message_create['sender_id'])]['num_dms'] += 1

        # If possible continue this function here - grab retweets/likes
    else:
        log.info(f"USE_CONN is {USE_CONN}, not doing anything.")

    print(followers)


# Main function.
def main():
    log.info(f"Starting up for the first time")
    log.info(f"Property use_connection: - {USE_CONN}")
    conn = None

    try:
        conn = connect()
    except tweepy.TweepyException as e:
        log.warning(f"Connection could not be made to Twitter: - {e}")
    else:
        log.info(f"Connection made successfully")

    # Sends a new tweet and checks for new followers, sleeps.
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


if __name__ == "__main__":
    log.info(f"Calling __main__")
    #main()

    # Do any testing here, but first comment out main():
    quoteDict.add_new_speaker("michael scott")
    quoteDict.import_new_sayings_dict()
    #quoteDict.export_current_dicts()
    #conn = connect()
    #get_best_friend(conn)
