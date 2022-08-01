#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# This file is for retrieving and storing the quotes and the relevant information used by the main script.

# Standard libraries.
import os
import glob
import datetime
import logging
import json
import csv
import xml.etree.ElementTree as elementTree
from zipfile import ZipFile, BadZipFile

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
EXPORT_PATH = config.get_property("export_path")
EXPORT_FILE_PREFIX = config.get_property("export_file_prefix")
ARCHIVE_FILE_PREFIX = config.get_property("archive_file_prefix")
EXPORT_EXT = config.get_property("base_export_extension")
ARCHIVE_EXTENSION = config.get_property_with_default("base_archive_extension", ".zip")
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


# Checks to see if a given quote has been used at least once.
# @param - quote: The quote we are going to check.
def is_used(quote):
    return bool(quote_dict[quote]['used'] > 0)


# Sets the used value of a specific quote.
# @param - quote: The quote we are going to update.
# @param - value: The new value for the used property.
def set_used(quote, value):
    log.info(f"Setting used to {value} for quote \"{quote}\"")
    quote_dict[quote]['used'] = value


# Increases the used value of a quote by 1.
# @param - quote: The quote object to increase.
def increase_used_by_one(quote):
    log.info(f"Increasing 'used' by 1 for: \"{quote}\"")
    value = quote_dict[quote]['used']
    set_used(quote, value + 1)


# Sets all quotes used values back to 0.
def mark_all_quotes_as_unused():
    for quote in quote_dict:
        set_used(quote, 0)


# Checks to see if the quote is valid - not empty, null, and does not begin with the comment character.
# @param - quote: The quote value to check.
def is_valid_quote(quote):
    log.info(f"Checking the quote value provided: {quote}")
    if quote is None or len(quote.strip()) < 1 or quote.strip()[0] == COMMENT_CHAR:
        return False

    return True


# Checks to see if the used value is valid - not negative and an integer.
# @param - used: The used value to check.
def is_valid_used(used):
    log.info(f"Checking the used value provided: {used}")

    try:
        int(used)
        used = int(used)
        if not isinstance(used, int) or used < 0 or used is None:
            return False
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True


# Checks to see if the source value is valid - not empty and a string.
# @param - source: The source value to check.
def is_valid_source(source):
    log.info(f"Checking the source value provided: {source}")

    if not isinstance(source, str) or len(source.strip()) < 1 or source is None:
        return False

    try:
        str(source)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True


# Checks the entire dictionary and resets any bad data.
def check_dictionary():
    log.info(f"Checking each quote's 'used' and 'source' values to be valid")
    for quote in quote_dict:
        if quote_dict[quote]['used'] < 0 or not isinstance(quote_dict[quote]['used'], int) or quote_dict[quote]['used'] is None:
            set_used(quote, 0)
        if not isinstance(quote_dict[quote]['source'], str) or len(quote_dict[quote]['source']) < 1:
            quote_dict[quote]['source'] = "Unknown"


# Add a new quote to the quote_dict.
# @param - dictionary: The dictionary object to add quotes to.
# @param - quote: The new quote to be added.
# @param - source: The quote speaker.
# @param - used: The number of times the quote has been used.
def add_new_quote(dictionary, quote, source, used):
    dictionary[quote] = {}
    dictionary[quote]['source'] = source
    dictionary[quote]['used'] = used
    add_new_speaker(source)
    log.info(f"New quote added to dict - \"{quote}\": {dictionary[quote]}")


# Import new quotes from files into the default office quote dict.
def import_new_sayings():
    print(f"Importing new quotes from files")
    log.info(f"Importing new quotes from files")
    new_quote_dict = dict()
    for filename in glob.glob(os.path.join(IMPORT_PATH, '*')):
        log.info(f"Attempting to import from file \"{filename}\"")
        # Import quotes from a txt file into the default office quote dict
        if filename.endswith('.txt'):
            import_file_txt(new_quote_dict, filename)

        # Import quotes from a csv file into the default office quote dict
        if filename.endswith('.csv'):
            import_file_csv(new_quote_dict, filename)

        # Import quotes from a xml file into the default office quote dict
        if filename.endswith('.xml'):
            import_file_xml(new_quote_dict, filename)

        # Import quotes from a json file into the default office quote dict
        if filename.endswith('.json'):
            print("json file")


# Import quotes from a .txt file.
# @param - dictionary: The dictionary we should add data to.
# @param - filename: The full file path and name that we will read data in from.
def import_file_txt(dictionary, filename):
    log.info(f"Opening TXT file '{filename}'")
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not is_valid_quote(line):
                break

            line_data = line.split(':{')

            if len(line_data) > 1:
                source = line_data[1].split(', ')[0].split(': ')[1].replace('}', '').strip('"').strip("'")
                try:
                    int(line_data[1].split(', ')[1].split(': ')[1].replace('}', '').replace('"', '').replace("'", ''))
                    used = int(
                        line_data[1].split(', ')[1].split(': ')[1].replace('}', '').replace('"', '').replace("'", ''))
                except ValueError:
                    log.info(f"Used value is not an integer, setting to 0")
                    used = 0
            else:
                source = "Unknown"
                used = 0

            # Add the new quote to the working dictionary.
            add_new_quote(dictionary, line_data[0], source, used)

    # Finally, add all new quotes to the existing dictionary.
    quote_dict.update(dictionary)


# Get the CSV header information.
# @param - header_row: A single row from the top of a csv file with the header values.
def get_csv_header_data(header_row):
    # Get the field indices from the header.
    index, quote_ind, source_ind, used_ind = 0, 0, 0, 0
    for field in header_row:
        if field == 'quote' or field == 'text':
            quote_ind = index
            index += 1
        elif field == 'source' or field == 'speaker':
            source_ind = index
            index += 1
        elif field == 'used':
            used_ind = index
            index += 1
        else:
            index += 1
    log.info(f"CSV header info - quote_text index: {quote_ind}, source index: {source_ind}, used index: {used_ind}")
    return quote_ind, source_ind, used_ind


# Get the CSV row information.
# @param - row: A single row of csv information.
# @param - quote_ind: The index of the quote data in the row.
# @param - source_ind: The index of the source data in the row.
# @param - used_ind: The index of the used data in the row.
def get_csv_row_data(row_data, quote_ind, source_ind, used_ind):
    quote_text = row_data[quote_ind].strip('"').strip("'").strip()
    source = row_data[source_ind].strip()
    used = row_data[used_ind]
    return quote_text, source, used


# Import quotes from a .csv file.
# @param - dictionary: The dictionary we should add data to.
# @param - filename: The full file path and name that we will read data in from.
def import_file_csv(dictionary, filename):
    log.info(f"Opening CSV file '{filename}'")

    with open(filename, 'r') as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)

        # Get the field indices from the header row.
        quote_ind, source_ind, used_ind = get_csv_header_data(header)

        # get quote info for each data row.
        for row in csv_reader:
            quote_text, source, used = get_csv_row_data(row, quote_ind, source_ind, used_ind)
            if not is_valid_quote(quote_text):  # If the quote text is not valid skip the current row.
                continue
            try:
                int(used)
            except ValueError:
                log.info(f"CSV - Used value is not an integer, setting to 0")
                used = 0
            else:
                used = int(used)

            # Make sure the values provided are valid, if not replace with default values.
            if not is_valid_source(source):
                source = "Unknown"
            if not is_valid_used(used):
                used = 0

            add_new_quote(dictionary, quote_text, source, used)

        # Finally, add all new quotes to the existing dictionary.
        quote_dict.update(dictionary)


# Import quotes from a .json file.
# @param - dictionary: The dictionary we should add data to.
# @param - filename: The full file path and name that we will read data in from.
def import_file_json(dictionary, filename):
    log.info(f"Opening JSON file '{filename}.'")
    with open(filename, 'r') as f:
        print("json")


# Get the child XML elements of the provided XML item.
# @param - item: The quote tag from the XML file.
def get_quote_xml_properties(item):
    quote_text, source, used = None, None, None
    for child in item:
        if child.tag == 'text' or child.tag == 'saying':
            quote_text = child.text
        if child.tag == 'source':
            source = child.text
        if child.tag == 'used':
            used = child.text
    return quote_text, source, used


# Import quotes from a .xml file.
# @param - dictionary: The dictionary we should add data to.
# @param - filename: The full file path and name that we will read data in from.
def import_file_xml(dictionary, filename):
    log.info(f"Opening XML file '{filename}'")
    with open(filename, 'r') as f:
        tree = elementTree.parse(f)
        root = tree.getroot()

        # Loop through each quote element.
        for item in root.findall('./quote'):
            # Get the expected child elements from the current quote tag.
            quote_text, source, used = get_quote_xml_properties(item)

            # Make sure the values provided are valid, if not replace with default values.
            if not is_valid_quote(quote_text):
                continue
            if not is_valid_source(source):
                source = "Unknown"
            if not is_valid_used(used):
                used = 0

            # Add the new quote to the working dictionary.
            add_new_quote(dictionary, quote_text.strip(), source.strip(), int(used))

        # Finally, add all new quotes to the existing dictionary.
        quote_dict.update(dictionary)


# Export the current dict of sayings to a file
def export_current_dicts():
    print(f"Exporting current working dicts")
    log.info(f"Exporting current working dicts")
    quotes_export_filename = f"{EXPORT_PATH}{EXPORT_FILE_PREFIX}quotes_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{EXPORT_EXT}"
    speakers_export_filename = f"{EXPORT_PATH}{EXPORT_FILE_PREFIX}speaker_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{EXPORT_EXT}"
    log.info(f"Exporting current working dicts to:\nQuote Dict: {quotes_export_filename}\nSpeaker Dict: {speakers_export_filename}")

    check_dictionary()

    with open(quotes_export_filename, "w") as f:
        for key, value in quote_dict.items():
            f.write('%s:%s\n' % (key, value))

    with open(speakers_export_filename, "w") as f:
        for key, value in speaker_dict.items():
            f.write('%s:%s\n' % (key, value))

    log.info(f"Export complete")


# Zip up the exported files.
def archive_all_exports():
    file_paths = []
    new_zip_name = f"{ARCHIVE_PATH}{ARCHIVE_FILE_PREFIX}{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{ARCHIVE_EXTENSION}"
    log.info(f"Archiving to: {new_zip_name}")

    # Crawl through the export directory
    for root, directories, files in os.walk(EXPORT_PATH):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # Write each file in the export location to a zip.
    try:
        with ZipFile(new_zip_name, 'w') as zipfile:
            for file in file_paths:
                filename = str(file.split("/")[-1])
                zipfile.write(file, arcname=filename)
    except FileNotFoundError:
        log.error(f"File {file} was not found")
    except BadZipFile:
        log.error(f"Exception writing to the zip file: {new_zip_name}")
    else:
        log.info(f"Successfully archived all export files into: {new_zip_name}")
        for file in os.listdir(EXPORT_PATH):
            os.remove(os.path.join(EXPORT_PATH, file))
            print(file)


# Add new speaker to speaker_dict
# @param - speaker: The new speaker being added.
def add_new_speaker(new_speaker):
    new_speaker = str(new_speaker.strip('"').strip("'")).title()
    for key, speaker in speaker_dict.items():
        if speaker.title() == new_speaker:
            log.info(f"Speaker already exists, not adding to dict: key={key}, name='{new_speaker}'")
            return False

    # If we get to this point the speaker is not in the dict, add them
    speaker_dict[max(k for k, v in speaker_dict.items())+1] = new_speaker
    log.info(f"New speaker was added: id={max(k for k, v in speaker_dict.items())}, name={new_speaker}")
