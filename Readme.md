## A Twitter Bot that tweets random quotes from the TV show "The Office".
#### Created by [Adam Bartholomew](https://www.linkedin.com/in/adam-bartholomew/) using [Python](https://www.python.org/) and [Tweepy](https://docs.tweepy.org/en/stable/index.html).
_With credit and inspiration from [Josh Richard](https://github.com/joshuarichard)_

#### Notes:
* This connects to my own personal Twitter account [here](https://twitter.com/The_Adumb).
* The bot used to be hosted via AWS on a EC2 free tier account, but I removed that in order to avoid being charged once I went past any service limits. Now it is only run locally.

#### Purpose:
* Learn and explore how to interact with an API. 
* Grow my knowledge of Python. 
* Explore any creative ideas.

#### Lessons Learned:
* How to set up a custom logger.
* How to package a library and import it into the main program.
* How to define dictionaries and functions to access/modify those dictionaries.
* How to read and write to and from different file types.

### Importing Quotes:
#### General Import Information
    The following config properties are used when importing a quote file:
        - import_path              | The path where import files should be placed.
        - allowed_import_filetypes | The file types allowed to be imported.
        - comment_char             | This character will be used to exclude lines during an import (txt only).

#### TXT
    1. All information about a quote in a ".txt" file should be on one line.
    2. The quote itself should not be surrounded by anything: quotation marks, brackets, parenthesis, etc.
    3. Any extra properties for the quote, i.e. speaker or used count, should be placed after the quote and within curly braces with a colon before the opening curly brace. 
        ":{"
    4. The extra property name should be enconclosed in single quotes followed by a colon and the value for that property.
    5. A line beginnning with the character defined in the comment_char property will be ignored and not be imported.
    6. If no extra properties are provided then default values will be used.

    The following example will add the quote "Et tu, Brute." with the properties of [source] and [used] equal to "Gaius Julius Caesar" and 1:
        Et tu, Brute.:{'source': 'Gaius Julius Caesar', 'used': 1}

#### XML
    1. The xml tag <quote> is required.
    2. The quote's text needs to be within <text> tags nested within each <quote> element.
    3. Any extra properties for the quote should also be in nested tags within the outer <quote> element, e.g. <source>, <used>
    4. A single root tag is needed but the name does not matter as long as it is unique and not named the same as any subtag, <dictionary> or <quotes> are good root tags.
    5. At this time no attributes are used.

    The following valid XML example will add the quote "Et tu, Brute." with the properties of [source] and [used] equal to "Gaius Julius Caesar" and 1:
    <dictionary>
        <quote>
            <text>Et tu, Brute.</text>
            <source>Gaius Julius Caesar</source>
            <used>1</used>
        </quote>
    </dictionary>

#### CSV
    1. The first row must contain headers.
    2. Each value must be separated by a comma.
    3. The best practice is to surround the quote text in quotes as it is necessary when the quote contains a comma.

    The following CSV example will add the quote "Et tu, Brute!" with the properties of [source] and [used] equal to "Gaius Julius Caesar" and 1:
    ---------------------------------------------    
    quote,source,used
    "Et tu, Brute!",Gaius Julius Caesar,1

#### JSON

### Exporting Quotes:
#### General Export Information
    The following config properties are used in the export process:
        - archive_path          | The location where the data will be exported.
        - archive_file_prefix   | The beginning of the export file name, something generic.
        - base_export_extension | The file type of the exported files.

####
    1. The quote and speaker dictionaries are exported as a flat .txt file.
    2. They come from the python dictionary that they are stored in while the program is running.

    The exported quotes will look like the example below:
        That's what she said!:{'source': 'Michael Scott', 'used': 1}
    

Further Reading and Library Documentation:
------------------------------------------
[Python](https://www.python.org/) | [Tweepy](http://www.tweepy.org/) | [Twitter](https://www.twitter.com/) | [LinkedIn](https://www.linkedin.com/in/adam-bartholomew/) | [GitHub](https://github.com/adam-bartholomew/)
