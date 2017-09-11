#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A twitter bot that tweets random quotes from "The Office".
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
    dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if line != "":
        try:
            connection.update_status(status=line)
            return True
        except tweepy.TweepError as error:
            log.error(error)
            log.info("error occured at %s", dateTime)
            return False

# Chooses a line from the dictionary.
def choose_line():
    log.info("Choosing line.")
    fileName = open(DICTIONARY_PATH, "r")
    fileList = fileName.readlines()
    fileName.close()

    numberOfLines = 0
    for line in fileList:
        numberOfLines += 1

    random.seed()
    randomInt = random.randint(0, numberOfLines)

    pointer = 0
    for line in fileList:
        if pointer == randomInt:
            if line[0] != COMMENT_CHAR:
                log.info("pointer = %s, randomInt = %s, numberOLines = %s ", pointer, randomInt, numberOfLines)
                log.info("Line Chosen: %s : %s", randomInt, line)
                return line
            else:
                iteration()
        else:
            pointer += 1

#def check_for_duplicates(line, connection):

# Follows someone back if they follow this account.
def check_followers():
    log.info("Checking followers...")
    connection = connect()
    theBot = connection.me()
    #log.info(connection.followers())
    for follower in connection.followers():
        if follower.following == False:
            log.info("ALERT: Now following %s!", follower.screen_name)
            userName = follower.screen_name
            userId = follower.id
            connection.create_friendship(userId, userName)
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
    if (send_tweet(line, connection) is True):
        dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log.info("Tweet sent with the line: %s at time %s", line, dateTime)
        print("Tweet sent with the line: %s at time %s", line, dateTime)
        return True
    else:
        dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log.info("Caught a tweepy error. at %s Trying again...", dateTime)
        print("Caught a tweepy error. at %s Trying again...", dateTime)
        return False

# Main.
def main():
    logging.basicConfig(filename="./logs/twitter-bot.log", level=logging.INFO)
    log.info("Starting up for the first time...")
    log.info("Reading dictionary located at %s", DICTIONARY_PATH)

    # Sends a new tweet every hour and checks for new followers.
    while True:
        check_followers()
        didTweet = iteration()
        if (didTweet is False):
            didTweet = iteration()
        else:
            time.sleep(SLEEP_FOR)

if __name__ == "__main__":
	main()