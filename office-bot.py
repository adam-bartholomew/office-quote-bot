#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from lib.quoteDict import quotes

# Get information from config file.
CONSUMER_KEY = config["consumer_key"]
CONSUMER_SECRET = config["consumer_secret"]
ACCESS_TOKEN = config["access_token"]
ACCESS_SECRET = config["access_secret"]
COMMENT_CHAR = config["comment_char"]
DOUBLE_LINE_CHAR = config["double_line_char"]
SLEEP_FOR = int(config["sleep_for"])

# Create logger.
log = logging.getLogger()

# Calculate sleep time
sleep_time = datetime.timedelta(seconds=int(SLEEP_FOR))


# Setup connection with Twitter.
def connect():
    log.info("Connecting to Twitter...")
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    connection = tweepy.API(auth)
    return connection


# Sends a tweet given the line and connection to the api.
#       quote - what to tweet.
#       connection - api connection
def send_tweet(quote, connection, date):
    if quote != "":
        try:
            # connection.update_status(status=quote)
            log.info("[%s]: Tweet sent with the quote %s", date, quote)
            print("[%s]: Tweet sent with the quote %s", date, quote)
            return True
        except tweepy.TweepyException as err:
            log.error("%s: Error occurred sending tweet: ", err)
            return False


# Chooses a quote from the dictionary.
def get_quote():
    log.info("Choosing quote...")

    random.seed()
    index = random.randint(0, len(quotes))
    quote = list(quotes.keys())[index]

    while is_used(quote):
        index = random.randint(0, len(quotes))
        quote = list(quotes.keys())[index]

    info = list(quotes.values())[index]
    quotes[quote]['used'] = 1

    msg = "\"%s\" - %s" % (quote, info.get('source'))
    log.info("Quote selected: [" + msg + "]\n" + str(quotes[quote]))
    print(msg)

    return msg


def is_used(quote):
    list_of_values = list(quotes.get(quote).values())
    return bool(list_of_values[1])


# Follows someone back if they follow this account.
def check_followers():
    log.info("Checking followers...")
    connection = connect()
    bot = connection.me()
    log.info(connection.followers())
    for follower in connection.followers():
        if not follower.following:
            log.info("ALERT: Now following %s!", follower.screen_name)
            connection.create_friendship(follower.id, follower.screen_name)
        else:
            log.info("All followers are followed.")
    log.info("Follower check COMPLETE.")


# Manages the process of sending a tweet.
def iteration(date):
    log.info("[%s] Start of a new iteration.", date)
    try:
        connection = connect()
    except tweepy.TweepyException as err:
        log.warning("Connection could not be made to Twitter:\n - %s", err)
    else:
        log.info("Connected...")

    quote = get_quote()

    log.info("Sending tweet...")
    if send_tweet(quote, connection, date) is True:
        # date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # log.info("Tweet sent with the quote: %s at time %s", quote, date)
        # print("Tweet sent with the quote: [%s] at time %s", quote, date)
        return True
    else:
        log.error("[%s]: Caught a tweepy error, trying again...", date)
        print("[%s]: Caught a tweepy error, trying again...", date)
        return False


# Main function
def main():
    base_dir = "./logs/"
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logfile = base_dir + "twitter-bot_" + datetime.datetime.now().strftime("%Y%m%d") + ".log"
    logging.basicConfig(filename=logfile, level=logging.INFO)
    log.info("Starting up for the first time...")

    # Sends a new tweet and checks for new followers, sleeps.
    while True:
        # check_followers()
        did_tweet = iteration(date)
        if did_tweet is False:
            did_tweet = iteration(date)
        else:
            log.info("Going to sleep for %s ", sleep_time)
            print("Sleeping...")
            time.sleep(SLEEP_FOR)


if __name__ == "__main__":
    main()
