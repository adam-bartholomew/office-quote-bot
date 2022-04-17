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
import lib.quoteDict as quoteDict

# Get information from config file.
CONSUMER_KEY = config["consumer_key"]
CONSUMER_SECRET = config["consumer_secret"]
ACCESS_TOKEN = config["access_token"]
ACCESS_SECRET = config["access_secret"]
COMMENT_CHAR = config["comment_char"]
DOUBLE_LINE_CHAR = config["double_line_char"]
SLEEP_FOR = int(config["sleep_for"])

# Create global variables.
log = logging.getLogger()
sleep_time = datetime.timedelta(seconds=int(SLEEP_FOR))
used_quotes = {}


# Setup connection with Twitter.
def connect():
    log.info("Connecting to Twitter...")
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)


# Sends a tweet given the line and connection to the api.
#       quote - what to tweet.
#       conn - api connection
def send_tweet(quote, conn, date):
    if quote != "":
        try:
            # conn.update_status(status=quote)
            log.info("[%s]: Tweet sent with the quote %s", date, quote)
            print("Tweet sent at %s. [%s]" % (date, quote))
            return True
        except tweepy.TweepyException as err:
            log.error("[%s]: Error occurred sending tweet: %s", date, err)
            return False


# Chooses a quote from the dictionary.
def get_quote():
    log.info("Choosing quote...")

    random.seed()
    index = random.randint(0, len(quoteDict.quotes))
    quote = list(quoteDict.quotes.keys())[index]
    get_least_used_quotes()
    #quote = random.choice(get_least_used_quotes())
    print("Selected: " + quote)

    while is_used(quote):
        index = random.randint(0, len(quoteDict.quotes))
        quote = list(quoteDict.quotes.keys())[index]

    info = list(quoteDict.quotes.values())[index]
    quoteDict.quotes[quote]['used'] = 1

    msg = "\"%s\" - %s" % (quote, info.get('source'))
    log.info("Quote selected: [" + quote + "]\n" + str(quoteDict.quotes[quote]))

    return msg


def is_used(quote):
    list_of_values = list(quoteDict.quotes.get(quote).values())
    return bool(list_of_values[1])


def get_most_used(): #todo: set all of the quotes to be unused once they all have been used th same # of times. No 1 quote can be used a 2nd time before they all have been used once.
    print('get most used quote')


def get_least_used_quotes():
    times_used = 0
    least_used = list()

    least_used_dict = quoteDict.quotes
    print(least_used_dict)

    for quote in quoteDict.quotes:
        # print(quote['used'])
        if quoteDict.quotes[quote]['used'] == times_used:
            least_used.append(quote)
        elif quote['used'] < times_used:
            least_used.clear()
            least_used.append(quote)

    return least_used


# Follows someone back if they follow this account.
def check_followers(conn, date):
    log.info("[%s]: Checking followers...", date)
    bot = conn.me()
    log.info(conn.followers())
    for follower in conn.followers():
        if not follower.following:
            try:
                conn.create_friendship(follower.id, follower.screen_name)
                log.info("ALERT: Now following %s!", follower.screen_name)
            except:
                log.info("[%s]: An unknown exception occurred while following", date)
        else:
            log.info("All followers are followed.")
    log.info("[%s]: Follower check COMPLETE.", date)


# Manages the process of sending a tweet.
def iteration(conn, date):
    log.info("[%s] Start of a new iteration.", date)

    log.info("Sending tweet...")
    if send_tweet(get_quote(), conn, date) is True:
        return True
    else:
        log.error("[%s]: Caught a tweepy error, trying again...", date)
        print("[%s]: Caught a tweepy error, trying again...", date)
        return False


# Main function
def main():
    quoteDict.get_least_used()
    base_dir = "./logs/"
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logfile = base_dir + "twitter-bot_" + datetime.datetime.now().strftime("%Y%m%d") + ".log"
    logging.basicConfig(filename=logfile, level=logging.INFO)
    log.info("Starting up for the first time...")

    try:
        conn = connect()
        log.info("Connected...")
    except tweepy.TweepyException as err:
        log.warning("Connection could not be made to Twitter:\n - %s", err)
    else:
        log.warning("[%s]: Connection could not be made to Twitter", date)

    # Sends a new tweet and checks for new followers, sleeps.
    while conn:
        # check_followers(conn, date)
        did_tweet = iteration(conn, date)
        if did_tweet is False:
            did_tweet = iteration(conn, date)
        else:
            log.info("Going to sleep for %s ", sleep_time)
            print("Sleeping...")
            time.sleep(SLEEP_FOR)


if __name__ == "__main__":
    main()
