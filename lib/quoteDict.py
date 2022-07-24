#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# This file is for retrieving and storing the quotes and the relevant information used by the main script.

# Standard libraries.
import os
import glob
import datetime
import logging

# Custom libraries.
import config

# Get config info
COMMENT_CHAR = config.get_property("comment_char")
DOUBLE_LINE_CHAR = config.get_property("double_line_char")
IMPORT_PATH = config.get_property("import_path")
DATE_FORMAT = config.get_property("logging_date_format")
LOG_FORMAT = config.get_property("log_format")
BASE_LOG_DIR = config.get_property("base_log_dir")
BASE_LOG_EXT = config.get_property("base_log_extension")
ARCHIVE_PATH = config.get_property("archive_path")
ARCHIVE_FILE_PREFIX = config.get_property("archive_file_prefix")
BASE_EXPORT_EXT = config.get_property("base_export_extension")
ALLOWED_IMPORT_FILETYPES = config.get_property("allowed_import_filetypes")

# Create variables.
log_filename = BASE_LOG_DIR + "twitter-bot_" + datetime.datetime.now().strftime("%Y%m%d") + BASE_LOG_EXT
logging.basicConfig(filename=log_filename, format=LOG_FORMAT, level=logging.DEBUG, datefmt=DATE_FORMAT)
log = logging.getLogger()

# Dictionary of default Speaker values for quotes
speaker_dict = {
    -1: "Unknown",
    0: "Michael Scott",
    1: "Jim Halpert",
    2: "Dwight Schrute",
    3: "Kevin Malone",
    4: "Creed Bratton",
    5: "Andrew Bernard",
    6: "Phyllis Vance",
    7: "Darryl Philbin",
    8: "Pam Beasley",
    9: "Angela Martin",
    10: "Oscar Martinez",
    11: "Todd Packer",
    12: "Jan Levenson",
    13: "Toby Flenderson"
}

# Dictionary of default Quotes
quote_dict = {
    "That's what she said!": {
        "source": speaker_dict[0], "used": 1},
    "Zippity Zoppity give me the Boppity!": {
        "source": speaker_dict[0], "used": 1},
    "I love inside jokes, love to be a part of one someday.": {
        "source": speaker_dict[0], "used": 1},
    "Sometimes I'll start a sentence and I don't even know where it's going. I just hope I find it along the way.": {
        "source": speaker_dict[0], "used": 1},
    "I am Beyonce always.": {
        "source": speaker_dict[0], "used": 1},
    "I DECLARE BANKRUPTCY!": {
        "source": speaker_dict[0], "used": 1},
    "I'm not superstitious, but I am a little stitious.": {
        "source": speaker_dict[0], "used": 1},
    "Hi, I'm date Mike... Nice to meet me!": {
        "source": speaker_dict[0], "used": 1},
    "We are all Homos... Homo Sapiens.": {
        "source": speaker_dict[0], "used": 1},
    "Just poopin'. You know how I be.": {
        "source": speaker_dict[0], "used": 1},
    "I hate so much about the things you choose to be.": {
        "source": speaker_dict[0], "used": 1},
    "Just tell him to call me ASAP as possible.": {
        "source": speaker_dict[0], "used": 1},
    "Abraham Lincoln once said that, 'If you're a racist I will attack you with the North.'": {
        "source": speaker_dict[0], "used": 1},
    "Suddenly she's not yo ho no mo'.": {
        "source": speaker_dict[0], "used": 1},
    "Well, happy birthday, Jesus. Sorry your party's so lame.": {
        "source": speaker_dict[0], "used": 1},
    "Dwight, you ignorant slut!": {
        "source": speaker_dict[0], "used": 1},
    "The worst thing about prison was... the dementors!": {
        "source": speaker_dict[0], "used": 1},
    "You don't know me; you've just seen my penis.": {
        "source": speaker_dict[0], "used": 1},
    "I should have burned this place down when I had the chance.": {
        "source": speaker_dict[0], "used": 1},
    "Would I rather be feared or loved? Easy, both. I want people to be afraid of how much they love me.": {
        "source": speaker_dict[0], "used": 1},
    "Do you think that smoking drugs is cool? Do you think that doing alcohol is cool?": {
        "source": speaker_dict[0], "used": 1},
    "I tried to talk to Toby and be his friend, but that is like trying to be friends with an evil snail.": {
        "source": speaker_dict[0], "used": 1},
    "You know what they say. 'Fool me once, strike one, but fool me twice... strike three.'": {
        "source": speaker_dict[0], "used": 1},
    "There's such a thing as good grief. Just ask Charlie Brown.": {
        "source": speaker_dict[0], "used": 1},
    "I need a username. And I have a great one. Little Kid Lover. That way people will know exactly where my priorities are at.": {
        "source": speaker_dict[0], "used": 1},
    "And I knew exactly what to do. But in a much more real sense, I had no idea what to do.": {
        "source": speaker_dict[0], "used": 1},
    "Oh God, my mind is going a mile an hour.": {
        "source": speaker_dict[0], "used": 1},
    "I hate disappointing just one person, and I really hate disappointing everyone. But I love Burlington Coat Factory.": {
        "source": speaker_dict[0], "used": 1},
    "Wikipedia is the best thing ever. Anyone in the world can write anything they want about any subject. So you know you are getting the best possible information.": {
        "source": speaker_dict[0], "used": 1},

    "The Taliban's the worst... Great Heroin, though.": {
        "source": speaker_dict[4], "used": 1},
    "That is Northern Lights Cannabis Indica.": {
        "source": speaker_dict[4], "used": 1},
    "I've been involved with a number of cults, both as a leader and as a follower. You have more fun as a follower, but you make more money as a leader.": {
        "source": speaker_dict[4], "used": 1},
    "If I can't scuba, then what's this all been about? What am I working toward?": {
        "source": speaker_dict[4], "used": 1},
    "Darnell's a chump.": {
        "source": speaker_dict[4], "used": 1},
    "You deal with this, or you, me, Sammy, Phyllis, the chick you hit with the car...we're goners.": {
        "source": speaker_dict[4], "used": 1},
    "Nobody steals from Creed Bratton and gets away with it. The last person to do this disappeared. His name? Creed Bratton.": {
        "source": speaker_dict[4], "used": 1},
    "I sprout mung beans on a damp paper towel in my desk drawer. Very nutritious, but they smell like death.": {
        "source": speaker_dict[4], "used": 1},
    "You're paying way too much for worms, man. Who's your worm guy?": {
        "source": speaker_dict[4], "used": 1},
    "You ever notice you can only ooze two things: sexuality and pus.": {
        "source": speaker_dict[4], "used": 1},
    "I already won the lotto. I was born in the U-S of A baby!": {
        "source": speaker_dict[4], "used": 1},

    "Sorry I annoyed you with my friendship.": {
        "source": speaker_dict[5], "used": 1},
    "Really? Well, maybe you should look in the smart part of your brain.": {
        "source": speaker_dict[5], "used": 1},
    "I always think one step ahead... like a carpenter... who makes stairs.": {
        "source": speaker_dict[5], "used": 1},
    "Andy Bernard does not lose contests, he wins them... or he quits them because they are unfair.": {
        "source": speaker_dict[5], "used": 1},
    "I mean for the record I prefer women... but off the record I'm kind of confused.": {
        "source": speaker_dict[5], "used": 1},
    "Women cannot resist a man singing show tunes. It's so powerful, a lot of men can't resist a man singing show tunes.": {
        "source": speaker_dict[5], "used": 1},
    "You know what? Maybe you're in the ceiling.": {
        "source": speaker_dict[5], "used": 1},
    "You're the deuce I never want to drop.": {
        "source": speaker_dict[5], "used": 1},
    "I wish there was a way to know you were in the good old days before you actually left them.": {
        "source": speaker_dict[5], "used": 1},
    "Every little boy fantasizes about his fairy-tale wedding.": {
        "source": speaker_dict[5], "used": 1},
    "Do not test my politeness.": {
        "source": speaker_dict[5], "used": 1},
    "The fire's shooting at us!": {
        "source": speaker_dict[5], "used": 2},

    "Who is Justice Beaver?": {
        "source": speaker_dict[2], "used": 2},
    "Absolutely I do.": {
        "source": speaker_dict[2], "used": 1},
    "Reject a woman, and she will never let it go, one of the many defects of their kind. Also, weak arms.": {
        "source": speaker_dict[2], "used": 1},
    "Before I do anything I ask myself 'Would an idiot do that?' And if the answer is yes, I do not do that thing.": {
        "source": speaker_dict[2], "used": 1},
    "Today, smoking is gonna save lives.": {
        "source": speaker_dict[2], "used": 1},
    "I am fast. To give you a reference point I am somewhere between a snake and a mongoose... And a panther.": {
        "source": speaker_dict[2], "used": 1},
    "I sat at my desk all day with a rifle that shoots potatoes at 60 pounds per square inch. Can you imagine if I was deranged?": {
        "source": speaker_dict[2], "used": 1},
    "Through concentration, I can raise and lower my cholesterol at will.": {
        "source": speaker_dict[2], "used": 1},
    "My maternal grandfather was the toughest guy I ever knew. World War II veteran, killed twenty men, and spent the rest of the war in an Allied prison camp.": {
        "source": speaker_dict[2], "used": 1},
    "How would I describe myself? Three words. Hard-working. Alpha male. Jackhammer. Merciless. Insatiable.": {
        "source": speaker_dict[2], "used": 1},
    "Why are all these people here? There are too many people on this earth. We need a new plague.": {
        "source": speaker_dict[2], "used": 1},
    "You couldn't handle my undivided attention.": {
        "source": speaker_dict[2], "used": -1},

    "Lord, beer me strength.": {
        "source": speaker_dict[1], "used": 1},
    "I don't understand the desire to push sweet potato fries on me. I just want regular fries.": {
        "source": speaker_dict[1], "used": 1},
    "Right now this is just a job. If I advance any higher in this company, then this would be my career. And well, if this were my career I'd have to throw myself in front of a train.": {
        "source": speaker_dict[1], "used": 0},
    "Bears. Beets. Battlestar Galactica.": {
        "source": speaker_dict[1], "used": 0},

    "Are you on Email?": {
        "source": speaker_dict[3], "used": 0},
}


# Returns a dictionary of the most used quote(s)
def get_most_used_dict():
    most_used_value = max(props['used'] for quote, props in quote_dict.items())  # Get the highest 'used' value
    most_used = {}
    for quote in quote_dict:
        if quote_dict[quote]['used'] == most_used_value:  # Add quote to the return dict if the used value matches the most_used_value from above
            most_used[quote] = {}
            most_used[quote]['source'] = quote_dict[quote]['source']
            most_used[quote]['used'] = quote_dict[quote]['used']

    log.info(f"There are {len(most_used)} items in the most used dictionary, each has been used {most_used_value} times.")
    return most_used


# Returns a dictionary of the least used quote(s)
def get_least_used_dict():
    least_used_value = min(props['used'] for quote, props in quote_dict.items())  # Get the lowest 'used' value
    least_used = {}
    for quote in quote_dict:
        if quote_dict[quote]['used'] == least_used_value:  # Add quote to the return dict if used value matches the least_used_value from above
            least_used[quote] = {}
            least_used[quote]['source'] = quote_dict[quote]['source']
            least_used[quote]['used'] = quote_dict[quote]['used']

    log.info(f"There are {len(least_used)} items in the least used dictionary, each has been used {least_used_value} times.")
    return least_used


# Checks to see if a given quote has been used at least once
def is_used(quote):
    return bool(quote_dict[quote]['used'] > 0)


# Sets the used value of a specific quote
def set_used(quote, value):
    log.info(f"Setting used to {value} for quote \"{quote}\"")
    quote_dict[quote]['used'] = value


# Increases the used value of a quote by 1.
def increase_used_by_one(quote):
    log.info(f"Increasing 'used' by 1 for: \"{quote}\"")
    value = quote_dict[quote]['used']
    set_used(quote, value + 1)


# Sets all quotes used values back to 0.
def mark_all_quotes_as_unused():
    for quote in quote_dict:
        set_used(quote, 0)


# Sets any "bad" used values to 0 - negative or non int types.
def check_dictionary():
    log.info(f"Checking each quote's 'used' values to be valid.")
    for quote in quote_dict:
        if quote_dict[quote]['used'] < 0 or not isinstance(quote_dict[quote]['used'], int) or quote_dict[quote]['used'] is None:
            set_used(quote, 0)


# Import quotes from a txt file into the default office quote dict.
def import_new_sayings_dict():
    print(f"Importing new quotes from file.")
    log.info(f"Importing new quotes from file.")
    new_quote_dict = dict()
    for filename in glob.glob(os.path.join(config.get_python_import_path(), '*' + ALLOWED_IMPORT_FILETYPES)):  # todo: add the allowed input file types as a prop in the config file and allow different file types to be imported.
        log.info(f"Opening '{filename}.'")
        with open(filename, 'r') as f:
            for line in f.readlines():
                if line[0] == COMMENT_CHAR or len(line) < 1:
                    break

                line_data = line.split(':{')

                if len(line_data) > 1:
                    source = line_data[1].split(', ')[0].split(': ')[1].replace('}', '').strip('"').strip("'").title()
                    try:
                        int(line_data[1].split(', ')[1].split(': ')[1].replace('}', '').replace('"', '').replace("'", ''))
                        used = int(line_data[1].split(', ')[1].split(': ')[1].replace('}', '').replace('"', '').replace("'", ''))
                    except ValueError:
                        log.info(f"Used value is not an integer, setting to 0")
                        used = 0
                else:
                    source = 'Unknown'
                    used = 0

                new_quote_dict[line_data[0]] = {}
                new_quote_dict[line_data[0]]['source'] = source
                new_quote_dict[line_data[0]]['used'] = used
                add_new_speaker(source)
                log.info(f"New quote added to dict - '{line_data[0]}': {new_quote_dict[line_data[0]]}")
    quote_dict.update(new_quote_dict)


# Export the current dict of sayings to a file
def export_current_dicts():
    print(f"Exporting current working dicts.")
    log.info(f"Exporting current working dicts.")
    quotes_export_filename = f"{ARCHIVE_PATH}{ARCHIVE_FILE_PREFIX}quotes_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{BASE_EXPORT_EXT}"
    speakers_export_filename = f"{ARCHIVE_PATH}{ARCHIVE_FILE_PREFIX}speaker_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{BASE_EXPORT_EXT}"
    log.info(f"Exporting current working dicts to:\nQuote Dict: {quotes_export_filename}\nSpeaker Dict: {speakers_export_filename}")

    check_dictionary()

    with open(quotes_export_filename, "w") as f:
        for key, value in quote_dict.items():
            f.write('%s:%s\n' % (key, value))

    with open(speakers_export_filename, "w") as f:
        for key, value in speaker_dict.items():
            f.write('%s:%s\n' % (key, value))

    log.info(f"Export complete.")


# Add new speaker to speaker_dict
def add_new_speaker(new_speaker):
    new_speaker = str(new_speaker.strip('"').strip("'")).title()
    for key, speaker in speaker_dict.items():
        if speaker.title() == new_speaker:
            log.info(f"Speaker already exists, not adding to dict: key={key}, name='{new_speaker}'")
            return False

    # If we get to this point the speaker is not in the dict, add them
    speaker_dict[max(k for k, v in speaker_dict.items())+1] = new_speaker
    log.info(f"New speaker was added: id={max(k for k, v in speaker_dict.items())}, name={new_speaker}")
