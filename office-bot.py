#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A Twitter bot that tweets random quotes from "The Office".
# Created by Adam Bartholomew.

# Import needed modules.
import tweepy
import time
import sys
import datetime
import logging
import random
import json

from config import config

# Get information from config file. TODO: conceal the tokens for the api
API_KEY = config["api_key"]
API_SECRET = config["api_secret"]
ACCESS_TOKEN = config["access_token"]
ACCESS_SECRET = config["access_secret"]
COMMENT_CHAR = config["comment_char"]
DOUBLE_LINE_CHAR = config["double_line_char"]
DICTIONARY_PATH = config["dictionary_path"]
SLEEP_FOR = int(config["sleep_for"])

# Create logger.
log = logging.getLogger()


# Setup connection with Twitter.
def connect():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    connection = tweepy.API(auth)
    return connection


# Sends a tweet given the line and connection to the api.
#       line - the line to tweet.
#       connection - instance of the api to use.
def send_tweet(line, connection):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if line != "":
        try:
            connection.update_status(status=line)
            return True
        except tweepy.TweepError as error:
            log.error(error)
            log.info("error occurred at %s", date)
            return False


# Chooses a line from the dictionary.
def choose_line():
    log.info("Choosing line.")
    filename = open(DICTIONARY_PATH, "r")
    filelist = filename.readlines()
    filename.close()

    lines = 0
    for line in filelist:
        lines += 1

    random.seed()
    random_int = random.randint(0, lines)

    pointer = 0
    for line in filelist:
        if pointer == random_int:
            if line[0] != COMMENT_CHAR:
                log.info("pointer = %s, random_int = %s, numberOLines = %s ", pointer, random_int, lines)
                log.info("Line Chosen: %s : %s", random_int, line)
                return line
            else:
                iteration()
        else:
            pointer += 1


# def check_for_duplicates(line, connection):

# Follows someone back if they follow this account.
def check_followers():
    log.info("Checking followers...")
    connection = connect()
    bot = connection.me()
    # log.info(connection.followers())
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
    connection = connect()
    line = ""
    log.info("Connected.")

    log.info("Choosing tweet...")
    line = choose_line()

    log.info("Sending tweet...")
    if send_tweet(line, connection) is True:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log.info("Tweet sent with the line: %s at time %s", line, date)
        print("Tweet sent with the line: %s at time %s", line, date)
        return True
    else:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log.info("Caught a tweepy error. at %s Trying again...", date)
        print("Caught a tweepy error. at %s Trying again...", date)
        return False


# Main.
def main():
    logging.basicConfig(filename="./logs/twitter-bot.log", level=logging.INFO)
    log.info("Starting up for the first time...")
    log.info("Reading dictionary located at %s", DICTIONARY_PATH)

    # Sends a new tweet every hour and checks for new followers.
    while True:
        check_followers()
        did_tweet = iteration()
        if did_tweet is False:
            did_tweet = iteration()
        else:
            time.sleep(SLEEP_FOR)


if __name__ == "__main__":
    main()
