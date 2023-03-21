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
from yattag import Doc, indent

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
        "source": speaker_dict[2], "used": 1},

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

    "1234567890"*28 + "A": {
        "source": "Test", "used": 0}
}


# Returns a dictionary of the most used quote(s).
def get_most_used_dict() -> dict:
    most_used_value = max(props['used'] for quote, props in quote_dict.items())
    most_used = {}
    # Adds quotes to the return dict if the used value matches the most_used_value calculated above.
    for quote in quote_dict:
        if quote_dict[quote]['used'] == most_used_value:
            most_used[quote] = {}
            most_used[quote]['source'] = quote_dict[quote]['source']
            most_used[quote]['used'] = quote_dict[quote]['used']

    log.info(f"There are {len(most_used)} items in the most used dictionary, each has been used {most_used_value} times.")
    return most_used


# Returns a dictionary of the least used quote(s).
def get_least_used_dict() -> dict:
    least_used_value = min(props['used'] for quote, props in quote_dict.items())
    least_used = {}
    # Adds quotes to the return dict if the used value matches the most_used_value calculated above.
    for quote in quote_dict:
        if quote_dict[quote]['used'] == least_used_value:
            least_used[quote] = {}
            least_used[quote]['source'] = quote_dict[quote]['source']
            least_used[quote]['used'] = quote_dict[quote]['used']

    log.info(f"There are {len(least_used)} items in the least used dictionary, each has been used {least_used_value} times.")
    return least_used


# Checks to see if a given quote has been used at least once.
# @param: quote - The quote we are going to check.
# Returns: Boolean
def is_used(quote: str) -> bool:
    return bool(quote_dict[quote]['used'] > 0)


# Sets the used value of a specific quote.
# @param: quote - The quote we are going to update.
# @param: value - The new value for the used property.
def set_used(quote: str, value: int):
    log.info(f"Setting used to {value} for quote \"{quote}\"")
    quote_dict[quote]['used'] = value


# Increases the used value of a quote by 1.
# @param: quote - The quote object to increase.
def increase_used_by_one(quote: str):
    log.info(f"Increasing 'used' by 1 for: \"{quote}\"")
    value = quote_dict[quote]['used']
    set_used(quote, value + 1)


# Sets all quotes used values back to 0.
def mark_all_quotes_as_unused():
    for quote in quote_dict:
        set_used(quote, 0)


# Checks to see if the quote is valid - not empty, null, and does not begin with the comment character.
# @param: quote - The quote value to check.
# Returns: Boolean
def is_valid_quote(quote: str) -> bool:
    log.info(f"Checking the quote value provided: {quote}")
    if quote is None or len(quote.strip()) < 1 or quote.strip()[0] == COMMENT_CHAR:
        return False
    return True


# Checks to see if the used value is valid - not negative and an integer.
# @param: used - The used value to check.
# Returns: Boolean
def is_valid_used(used: int) -> bool:
    log.info(f"Checking the used value provided: {used}")
    try:
        int(used)
        used = int(used)
        if not isinstance(used, int) or used < 0 or used is None:
            return False
    except(ValueError, TypeError):
        return False
    else:
        return True


# Check to make sure used value is an integer or can be cast to an integer, if not return 0.
# @param: used - The used value to check.
# Returns: Integer
def validate_used(used: int | str) -> int:
    log.info(f"Checking the used value provided: {used}")
    try:
        int(used)
        used = int(used)
    except(TypeError, ValueError):
        return 0
    else:
        if used < 0:
            return 0
        return used


# Checks to see if the source value is valid - not empty and a string.
# @param: source - The source value to check.
# Returns: Boolean
def is_valid_source(source: str) -> bool:
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


# Checks to see if the source value is valid - not empty and a string.
# @param: source - The source value to check.
# Returns: String
def validate_source(source: str) -> str:
    log.info(f"Checking the source value provided: {source}")
    try:
        str(source)
    except(ValueError, TypeError):
        return "Unknown"
    else:
        if not isinstance(source, str) or len(str(source)) < 1:
            return "Unknown"
        return source


# Checks the entire dictionary and resets any bad data.
def check_dictionary():
    log.info("Checking each quote's 'used' and 'source' values to be valid")
    for quote in quote_dict:
        if quote_dict[quote]['used'] < 0 or not isinstance(quote_dict[quote]['used'], int) or quote_dict[quote]['used'] is None:
            set_used(quote, 0)
        if not isinstance(quote_dict[quote]['source'], str) or len(quote_dict[quote]['source']) < 1:
            quote_dict[quote]['source'] = "Unknown"


# Checks to see if a quote, case-insensitive, exists in the dictionary.
# @param: dictionary - The dictionary to check.
# @param: quote - The quote to check.
# Returns: Boolean - True if the quote exists otherwise False.
def is_quote_in_dict(dictionary: dict, quote: str) -> bool:
    log.debug(f"Checking dictionary for: \"{quote.lower()}\"")
    for key in dictionary.keys():
        if quote.lower() == key.lower():
            log.info(f"\"{quote.lower()}\" was found.")
            return True

    log.info(f"\"{quote.lower()}\" was not found.")
    return False


# Add a new quote to the dict.
# @param: dictionary - The dictionary object to add quotes to.
# @param: quote - The new quote to be added.
# @param: source - The quote speaker.
# @param: used - The number of times the quote has been used.
def add_new_quote(dictionary: dict, quote: str, source: str, used: int):
    if not is_quote_in_dict(quote_dict, quote):
        dictionary[quote] = {}
        dictionary[quote]['source'] = source
        dictionary[quote]['used'] = used
        add_new_speaker(source)
        log.info(f"New quote added to dict - \"{quote}\":{dictionary[quote]}")
    else:
        log.info(f"This quote already exists in the dictionary and has not been added: \"{quote}\"")


# Import new quotes from files into the default office quote dict.
def import_new_sayings():
    print("Importing new quotes from files")
    log.info("Importing new quotes from files")
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
            import_file_json(new_quote_dict, filename)


# Import quotes from a .txt file and add to default quote dictionary.
# @param: dictionary - The dictionary we should add data to.
# @param: filename - The full file path and name that we will read data in from.
def import_file_txt(dictionary: dict, filename: str):
    log.info(f"Opening TXT file '{filename}'")
    with open(filename, 'r') as f:
        for line in f.readlines():
            # Make sure the values provided are valid, if not replace with default values.
            if not is_valid_quote(line):
                continue

            line_data = line.split(':{')
            if len(line_data) > 1:
                used = validate_used(line_data[1].split(', ')[1].split(': ')[1].replace('}', '').replace('"', '').replace("'", ''))
                source = validate_source(line_data[1].split(', ')[0].split(': ')[1].replace('}', '').strip('"').strip("'"))
            else:
                used = 0
                source = "Unknown"
            add_new_quote(dictionary, line_data[0], source, used)

    # Finally, add all new quotes to the existing dictionary.
    quote_dict.update(dictionary)


# Get the CSV header information.
# @param: header_row - A single row from the top of a csv file with the header values.
# Returns: Integer - indices for csv positional information.
def get_csv_header_data(header_row: list) -> (int, int, int):
    # Get the field indices from the header.
    index, quote_ind, source_ind, used_ind = 0, 0, 0, 0
    for field in header_row:
        if field == 'text' or field == 'quote':
            quote_ind = index
            index += 1
        elif field == 'source' or field == 'speaker':
            source_ind = index
            index += 1
        elif field == 'used' or field == 'count':
            used_ind = index
            index += 1
        else:
            index += 1
    log.info(f"CSV header info - quote_text index: {quote_ind}, source index: {source_ind}, used index: {used_ind}")
    return quote_ind, source_ind, used_ind


# Get the CSV row information.
# @param: row - A single row of csv information.
# @param: quote_ind - The index of the quote data in the row.
# @param: source_ind - The index of the source data in the row.
# @param: used_ind - The index of the used data in the row.
# Returns: String, String, Integer
def get_csv_row_data(row_data: list, quote_ind: int, source_ind: int, used_ind: int) -> (str, str, int):
    quote_text = row_data[quote_ind].strip('"').strip("'").strip()
    source = row_data[source_ind].strip()
    used = row_data[used_ind]
    return quote_text, source, used


# Import quotes from a .csv file and add to default quote dictionary.
# @param: dictionary - The dictionary we should add data to.
# @param: filename - The full file path and name that we will read data in from.
def import_file_csv(dictionary: dict, filename: str):
    log.info(f"Opening CSV file '{filename}'")

    with open(filename, 'r') as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)

        # Get the field indices from the header row.
        quote_ind, source_ind, used_ind = get_csv_header_data(header)

        # Get quote info for each data row.
        for row in csv_reader:
            quote_text, source, used = get_csv_row_data(row, quote_ind, source_ind, used_ind)

            # Make sure the values provided are valid, if not replace with default values.
            if not is_valid_quote(quote_text):
                continue
            used = validate_used(used)
            source = validate_source(source)
            add_new_quote(dictionary, quote_text, source, used)

        # Finally, add all new quotes to the existing dictionary.
        quote_dict.update(dictionary)


# Get the values out of the provided json data row.
# @param: row_data - A single row of json information.
# Returns: String, String, Integer
def get_json_row_data(row_data: dict) -> (str, str, int):
    quote_text, source, used = None, None, None
    for index, value in enumerate(row_data):
        if value == 'text' or value == 'quote':
            quote_text = row_data[value]
        if value == 'source' or value == 'speaker':
            source = row_data[value]
        if value == 'used' or value == 'count':
            used = row_data[value]
        if quote_text is not None:
            quote_text = quote_text.strip('"').strip("'").strip()  # Format the quote text.
    return quote_text, source, used


# Import quotes from a .json file and add to default quote dictionary.
# @param: dictionary - The dictionary we should add data to.
# @param: filename - The full file path and name that we will read data in from.
def import_file_json(dictionary: dict, filename: str):
    log.info(f"Opening JSON file '{filename}.'")
    with open(filename, 'r') as f:
        json_data = json.load(f)

        # Iterate through each JSON quote object.
        for quote_data in json_data['quotes']:
            quote_text, source, used = get_json_row_data(quote_data)

            # Make sure the values provided are valid, if not replace with default values.
            if not is_valid_quote(quote_text):
                continue
            used = validate_used(used)
            source = validate_source(source)
            add_new_quote(dictionary, quote_text, source, used)

        # Finally, add all new quotes to the existing dictionary.
        quote_dict.update(dictionary)


# Get the child XML elements of the provided XML item.
# @param: item - The XML quote item and all its sub elements.
# Returns: String, String, Integer
def get_quote_xml_properties(item: elementTree.Element) -> (str, str, int):
    print(type(item))
    quote_text, source, used = None, None, None
    for child in item:
        if child.tag == 'text' or child.tag == 'quote':
            quote_text = child.text
        if child.tag == 'source' or child.tag == 'speaker':
            source = child.text
        if child.tag == 'used' or child.tag == 'count':
            used = child.text
    return quote_text, source, used


# Import quotes from a .xml file and add to default quote dictionary.
# @param: dictionary - The dictionary we should add data to.
# @param: filename - The full file path and name that we will read data in from.
def import_file_xml(dictionary: dict, filename: str):
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
            source = validate_source(source)
            used = validate_used(used)
            add_new_quote(dictionary, quote_text.strip(), source.strip(), int(used))

        # Finally, add all new quotes to the existing dictionary.
        quote_dict.update(dictionary)


# Export the current quote dictionary to a xml file.
# @param: quote_filename - The export file for quotes.
# @param: speaker_filename - The export file for speakers.
def export_current_dicts_xml(quote_filename: str, speaker_filename: str):
    log.info("Exporting to XML.")
    with open(quote_filename, "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r")
        doc, tag, text = Doc().tagtext()
        with tag('quotes'):
            for key, value in quote_dict.items():
                with tag('quote'):
                    with tag('text'):
                        text(key)
                    for k, v in value.items():
                        if k == 'source':
                            with tag('source'):
                                text(v)
                        if k == 'used':
                            with tag('used'):
                                text(v)
        result = indent(
            doc.getvalue(),
            indentation=' ' * 4,
            newline='\r'
        )
        f.write(result)

    with open(speaker_filename, "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r")
        doc, tag, text = Doc().tagtext()
        with tag('speakers'):
            for key, value in speaker_dict.items():
                with tag('speaker'):
                    with tag('id'):
                        text(key)
                    with tag('name'):
                        text(value)
        result = indent(
            doc.getvalue(),
            indentation=' ' * 4,
            newline='\r'
        )
        f.write(result)


# Export the current quote dictionary to a xml file.
# @param: quote_filename - The export file for quotes.
# @param: speaker_filename - The export file for speakers.
def export_current_dicts_txt(quote_filename: str, speaker_filename: str):
    log.info("Exporting to TXT.")
    with open(quote_filename, "w") as f:
        for key, value in quote_dict.items():
            f.write('%s:%s\n' % (key, value))

    with open(speaker_filename, "w") as f:
        for key, value in speaker_dict.items():
            f.write('%s:%s\n' % (key, value))


# Export the current quote dictionary to a csv file.
# @param: quote_filename - The export file for quotes.
# @param: speaker_filename - The export file for speakers.
def export_current_dicts_csv(quote_filename: str, speaker_filename: str):
    log.info("Exporting to CSV.")
    with open(quote_filename, "w", newline="") as f:
        headers = ["Quote", "Source", "Used"]
        writer = csv.writer(f)
        writer.writerow(headers)
        for key, value in quote_dict.items():
            row = list()
            row.append(key)
            for k, v in value.items():
                row.append(v)
            writer.writerow(row)

    with open(speaker_filename, "w", newline="") as f:
        headers = ["Id", "Name"]
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(speaker_dict.items())


# Export the current quote dictionary to a json file.
# @param: quote_filename - The export file for quotes.
# @param: speaker_filename - The export file for speakers.
def export_current_dicts_json(quote_filename: str, speaker_filename: str):
    log.info("Exporting to JSON.")
    json_quote_array = [{'text': i, 'source': quote_dict[i]['source'], 'used': quote_dict[i]['used']} for i in quote_dict]
    json_quote_dict = {"quotes": json_quote_array}
    json_speaker_dict = [{'id': k, 'name': v} for k, v in speaker_dict.items()]
    with open(quote_filename, "w", newline="") as f:
        json.dump(json_quote_dict, f, indent=4)
    with open(speaker_filename, "w", newline="") as f:
        json.dump(json_speaker_dict, f, indent=4)


# Export the current quote dictionary to a file.
def export_current_dicts():
    quotes_export_filename = f"{EXPORT_PATH}{EXPORT_FILE_PREFIX}quotes_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{EXPORT_EXT}"
    speakers_export_filename = f"{EXPORT_PATH}{EXPORT_FILE_PREFIX}speaker_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{EXPORT_EXT}"
    log.info(f"Exporting current working dicts to:\nQuote Dict: {quotes_export_filename}\nSpeaker Dict: {speakers_export_filename}")
    print("Exporting current working dicts")

    check_dictionary()

    if EXPORT_EXT == ".xml":
        export_current_dicts_xml(quotes_export_filename, speakers_export_filename)
    elif EXPORT_EXT == ".csv":
        print("csv export")
        export_current_dicts_csv(quotes_export_filename, speakers_export_filename)
    elif EXPORT_EXT == ".json":
        print("json export")
        export_current_dicts_json(quotes_export_filename, speakers_export_filename)
    else:
        export_current_dicts_txt(quotes_export_filename, speakers_export_filename)

    log.info("Exporting complete")


# Zip up the exported files and place in the archive directory.
def archive_all_exports():
    file_paths = []
    new_zip_name = f"{ARCHIVE_PATH}{ARCHIVE_FILE_PREFIX}{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{ARCHIVE_EXTENSION}"
    log.info("Start archive process.")

    # Crawl through the export directory to create the full filepath for the files to archive.
    for root, directories, files in os.walk(EXPORT_PATH):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # Zip up all the files in export location.
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
    log.info(f"Archive complete: {new_zip_name}")


# Add a new speaker to speaker_dict.
# @param: speaker - The new speaker being added.
def add_new_speaker(new_speaker: str) -> bool:
    new_speaker = str(new_speaker.strip('"').strip("'")).title()
    for key, speaker in speaker_dict.items():
        if speaker.title() == new_speaker:
            log.info(f"Speaker already exists, not adding to dict: key={key}, name='{new_speaker}'")
            return False

    # If we get to this point the speaker is not in the dict, add them
    ind = max(k for k, v in speaker_dict.items())+1
    speaker_dict[ind] = new_speaker
    log.info(f"New speaker was added: id={ind}, name={new_speaker}")
