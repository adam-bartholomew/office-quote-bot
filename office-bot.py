#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A Twitter bot that tweets random quotes from "The Office".
# Created by Adam Bartholomew.

# Import needed modules.
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


# Setup connection with Twitter.
def connect():
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    connection = tweepy.API(auth)
    return connection


# Sends a tweet given the line and connection to the api.
#       quote - what to tweet.
#       connection - api connection
def send_tweet(quote, connection):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if quote != "":
        try:
            #connection.update_status(status=quote)
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

    # pointer = 0
    # for line in filelist:
    #    if pointer == random_int:
    #        if line[0] != COMMENT_CHAR:
    #            log.info("pointer = %s, random_int = %s, numberOLines = %s ", pointer, random_int, lines)
    #            log.info("Line Chosen: %s : %s", random_int, line)
    #            return line
    #        else:
    #           iteration()
    #  else:
    #      pointer += 1


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
def iteration():
    log.info("Connecting to twitter...")
    try:
        connection = connect()
    except tweepy.TweepyException as err:
        log.warning("Connection could not be made to Twitter:\n - %s", err)
    else:
        log.info("Connected...")

    quote = get_quote()

    log.info("Sending tweet...")
    if send_tweet(quote, connection) is True:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log.info("Tweet sent with the quote: %s at time %s", quote, date)
        print("Tweet sent with the quote: [%s] at time %s", quote, date)
        return True
    else:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log.error("Caught a tweepy error. at %s Trying again...", date)
        print("Caught a tweepy error. at %s Trying again...", date)
        return False


# Main function
def main():
    base_dir = "./logs/"
    date = datetime.datetime.now().strftime("%Y%m%d")
    logfile = base_dir + "twitter-bot_" + date + ".log"
    logging.basicConfig(filename=logfile, level=logging.INFO)
    log.info("Starting up for the first time...")

    # Sends a new tweet and checks for new followers, sleeps.
    while True:
        # check_followers()
        did_tweet = iteration()
        if did_tweet is False:
            did_tweet = iteration()
        else:
            time.sleep(SLEEP_FOR)


if __name__ == "__main__":
    main()
