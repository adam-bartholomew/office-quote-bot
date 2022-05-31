#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# A Twitter bot that tweets random quotes from "The Office".
# Created by Adam Bartholomew.

# Import needed python modules.
import tweepy
import datetime
import time
import logging
import random

# Custom imports.
import config
import lib.quoteDict as quoteDict

# Get config info.
CONSUMER_KEY = config.properties["consumer_key"]
CONSUMER_SECRET = config.properties["consumer_secret"]
ACCESS_TOKEN = config.properties["access_token"]
ACCESS_SECRET = config.properties["access_secret"]
COMMENT_CHAR = config.properties["comment_char"]
DOUBLE_LINE_CHAR = config.properties["double_line_char"]
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
    log.info("Attempting to connect to Twitter.")
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
                log.info("USE_CONN=%s | Tweet sent: %s", USE_CONN, tweet)
                print("USE_CONN=%s | Tweet sent: %s" % (USE_CONN, tweet))
            log.info("USE_CONN=%s | Tweet not sent: %s", USE_CONN, tweet)
            print("USE_CONN=%s | Tweet not sent: %s" % (USE_CONN, tweet))
            quoteDict.increase_used_by_one(quote)
            return True
        except tweepy.TweepyException as err:
            log.error("Error occurred sending tweet: %s", err)
            return False


# Chooses a quote from the dictionary.
def get_quote():
    log.info("Choosing quote...")

    possible_options = quoteDict.get_least_used_dict()
    random.seed()
    index = random.randint(0, len(possible_options) - 1)

    quote = list(possible_options.keys())[index]
    quote_speaker = (list(possible_options.values())[index]).get('source')
    msg = "\"%s\" - %s" % (quote, quote_speaker)
    log.info("Quote selected \"%s\": %s", quote, str(quoteDict.quotes[quote]))

    return quote, msg


# Follows someone back if they follow this account.
#   conn  - tweepy api connection.
def check_followers(conn):
    log.info("Checking %s's followers", conn.verify_credentials().screen_name)

    if USE_CONN:
        for follower in conn.get_followers():
            if not follower.following:
                try:
                    conn.create_friendship(follower.screen_name, follower.id)
                except tweepy.TweepyException as err:
                    log.info("An unknown exception occurred while trying to follow '%s': %s", follower.screen_name, err)
                else:
                    log.info("ALERT: Now following %s!", follower.screen_name)
        log.info("All followers are now followed.\nFOLLOWER CHECK COMPLETE.")
    else:
        log.info("USE_CONN is %s, not doing anything.", USE_CONN)


# Manages the process of sending a tweet.
#   conn  - tweepy api connection.
def iteration(conn):
    log.info("Start of a new iteration.")
    quote, tweet = get_quote()
    if send_tweet(quote, tweet, conn):
        return True
    else:
        log.error("Caught a tweepy error, trying again...")
        print("Caught a tweepy error, trying again...")
        return False


# Gets the "Best Friend", the user with whom we interacted with the most
#   conn  - tweepy api connection.
def get_best_friend(conn):
    log.info("Getting %s's best friend.", conn.verify_credentials().screen_name)
    followers = dict()
    followers[conn.verify_credentials().id] = {}
    followers[conn.verify_credentials().id]['screen_name'] = conn.verify_credentials().screen_name
    followers[conn.verify_credentials().id]['num_dms'] = 0

    if USE_CONN:
        for follower in conn.get_followers():
            followers[follower.id] = {}
            followers[follower.id]['screen_name'] = follower.screen_name
            followers[follower.id]['num_dms'] = 0

        log.info("Grabbing direct messages.")
        for dm in conn.get_direct_messages():
            print(dm)
            if int(dm.message_create['sender_id']) in followers:
                followers[int(dm.message_create['sender_id'])]['num_dms'] += 1

        # Continue this function here - grab retweets/likes
    else:
        log.info("USE_CONN is %s, not doing anything.", USE_CONN)

    print(followers)


# Main function.
def main():
    log.info("Starting up for the first time")
    log.info("Property use_connection: - %s", USE_CONN)
    conn = None

    try:
        conn = connect()
    except tweepy.TweepyException as e:
        log.warning("Connection could not be made to Twitter: - %s", e)
    else:
        log.info("Connection made successfully")

    # Sends a new tweet and checks for new followers, sleeps.
    while conn:
        log.info("Start of connection loop.")
        check_followers(conn)
        did_tweet = iteration(conn)
        while did_tweet is False:
            did_tweet = iteration(conn)
        # else:
        log.info("Going to sleep for %s ", sleep_time)
        print("Sleeping...")
        time.sleep(SLEEP_FOR)


if __name__ == "__main__":
    #main()

    # Do any testing here, but first comment out main():
    conn = connect()
    get_best_friend(conn)
