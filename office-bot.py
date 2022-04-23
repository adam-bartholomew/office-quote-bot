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

# Custom imports
from config import config
import lib.quoteDict as quoteDict

# Get config info.
CONSUMER_KEY = config["consumer_key"]
CONSUMER_SECRET = config["consumer_secret"]
ACCESS_TOKEN = config["access_token"]
ACCESS_SECRET = config["access_secret"]
COMMENT_CHAR = config["comment_char"]
DOUBLE_LINE_CHAR = config["double_line_char"]
SLEEP_FOR = int(config["sleep_for"])
DATE_FORMAT = config["logging_date_format"]
LOG_FORMAT = config["log_format"]
BASE_LOG_DIR = config["base_log_dir"]
BASE_LOG_EXT = config["base_log_extension"]

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
#       quote - what to tweet.
#       conn - api connection
def send_tweet(quote, conn):
    if quote != "":
        try:
            # conn.update_status(status=quote)
            log.info("Tweet sent: %s", quote)
            print("Tweet sent: %s" % quote)
            return True
        except tweepy.TweepyException as err:
            log.error("Error occurred sending tweet: %s", err)
            return False


# Chooses a quote from the dictionary.
def get_quote():
    log.info("Choosing quote...")

    random.seed()
    index = random.randint(0, len(quoteDict.quotes))
    quote = list(quoteDict.quotes.keys())[index]
    get_least_used_quotes()
    # quote = random.choice(get_least_used_quotes())
    print("Quote Selected: %s" % quote)

    while is_used(quote):
        index = random.randint(0, len(quoteDict.quotes))
        quote = list(quoteDict.quotes.keys())[index]

    info = list(quoteDict.quotes.values())[index]
    quoteDict.quotes[quote]['used'] = 1

    msg = "\"%s\" - %s" % (quote, info.get('source'))
    log.info("Quote selected: %s\n  %s", quote,  str(quoteDict.quotes[quote]))

    return msg


def is_used(quote):
    list_of_values = list(quoteDict.quotes.get(quote).values())
    return bool(list_of_values[1])


def get_most_used():
    # todo: set all of the quotes to be unused once they all have been used th same # of times. No 1 quote can be used a 2nd time before they all have been used once.
    print('get most used quote')


def get_least_used_quotes():
    times_used = 0
    least_used = list()

    least_used_dict = quoteDict.quotes
    # print(least_used_dict)

    for quote in quoteDict.quotes:
        # print(quote['used'])
        if quoteDict.quotes[quote]['used'] == times_used:
            least_used.append(quote)
        elif quote['used'] < times_used:
            least_used.clear()
            least_used.append(quote)

    return least_used


# Follows someone back if they follow this account.
def check_followers(conn):
    log.info("Checking %s's followers", conn.verify_credentials().screen_name)
    for follower in conn.get_followers():
        if not follower.following:
            try:
                # conn.create_friendship(follower.screen_name, follower.id)
                log.info("ALERT: Now following %s!", follower.screen_name)
            except tweepy.TweepyException as err:
                log.info("An unknown exception occurred while following: %s", err)

    log.info("All followers are now followed.")
    log.info("Follower check COMPLETE.")


# Manages the process of sending a tweet.
def iteration(conn):
    log.info("Start of a new iteration.")
    if send_tweet(get_quote(), conn) is True:
        return True
    else:
        log.error("Caught a tweepy error, trying again...")
        print("Caught a tweepy error, trying again...")
        return False


# Main function
def main():
    quoteDict.get_least_used()
    log.info("Starting up for the first time")

    try:
        conn = connect()
    except tweepy.TweepyException as err:
        log.warning("Connection could not be made to Twitter: - %s", err)
    else:
        log.info("Connection made successfully")

    # Sends a new tweet and checks for new followers, sleeps.
    while conn:
        check_followers(conn)
        did_tweet = iteration(conn)
        while did_tweet is False:
            did_tweet = iteration(conn)
        else:
            log.info("Going to sleep for %s ", sleep_time)
            print("Sleeping...")
            time.sleep(SLEEP_FOR)


if __name__ == "__main__":
    main()
