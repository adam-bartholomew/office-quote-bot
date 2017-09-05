#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy
import time
import sys
import datetime
import logging
import random

from config import config
 
API_KEY = config["api_key"]
API_SECRET = config["api_secret"]
ACCESS_TOKEN = config["access_token"]
ACCESS_SECRET = config["access_secret"]
COMMENT_CHAR = config["comment_char"]
DICTIONARY_PATH = config["dictionary_path"]
SLEEP_FOR = int(config["sleep_for"])

log = logging.getLogger()

# Setup connection with Twitter
def connect():
	auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = tweepy.API(auth)

	return api

# Sends a tweet given the line as an argument. 
#       line - the line to tweet.
#       connection - instance of the api to use.
def send_tweet(line, connection):
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if line != "":
        try:
            connection.update_status(status=line)
            return True
        except tweepy.TweepError as e:
            log.error(e)
            log.info("error occured at %s", date_time)
            return False

# Chooses a line from the dictionary
def choose_line():
    file_name = open(DICTIONARY_PATH, "r")
    file_list = file_name.readlines()
    file_name.close()

    num_of_lines = 0
    for line in file_list:
        num_of_lines += 1

    random.seed()
    r_int = random.randint(0, num_of_lines)

    pointer = 0
    for line in file_list:
        if pointer == r_int:
            if line[0] != COMMENT_CHAR:
                log.info("pointer = %s, rInt = %s, num_of_lines = %s ", pointer, r_int, num_of_lines)
                return line
            else:
                iteration()
        else:
            pointer += 1

#def check_line(line, connection):

# Manages the process of sending a tweet
def iteration():
    log.info("Connecting to twitter...")
    connection = connect()
    line = ""
    log.info("Connected.")

    log.info("Choosing word to tweet...")
    line = choose_line()

    log.info("Sending tweet...")
    if (send_tweet(line, connection) is True):
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log.info("Tweet sent with the line: %s at time %s", line, date_time)
        return True
    else:
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log.info("Caught a tweepy error. at %s Trying again...", date_time)
        return False

# Main
def main():
    logging.basicConfig(filename="./logs/twitter-bot.log", level=logging.INFO)
    log.info("Starting up for the first time...")
    log.info("Reading dictionary located at %s", DICTIONARY_PATH)

    while True:
        did_tweet = iteration()
        if (did_tweet is False):
            did_tweet = iteration()
        else:
            time.sleep(SLEEP_FOR)

if __name__ == "__main__":
	main()