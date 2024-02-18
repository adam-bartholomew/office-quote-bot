#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# The file for configurable properties.

# Standard libraries.
import datetime
import logging
from typing import Any

properties = {"consumer_key": "",
              "consumer_secret": "",
              "access_token": "",
              "access_secret": "",
              "sleep_for": "86400",  # represented in seconds: 24 hours
              "comment_char": "#",
              "double_line_char": "&",
              "log_format": "%(asctime)s.%(msecs)03d |:| %(levelname)s |:| %(message)s",
              "logging_date_format": "%m/%d/%Y %H:%M:%S",
              "base_log_dir": "./logs/",
              "base_log_extension": ".log",
              "use_connection": "False",
              "import_path": "C:/Users/adamb/PycharmProjects/office-quote-bot/imports",
              "archive_path": "C:/Users/adamb/PycharmProjects/office-quote-bot/archive/",
              "export_path": "C:/Users/adamb/PycharmProjects/office-quote-bot/exports/",
              "export_file_prefix": "dict_export_",
              "archive_file_prefix": "dict_archive_",
              "base_export_extension": ".txt",
              "base_archive_extension": ".zip",
              "allowed_import_filetypes": ".txt",
              "sound_dir": "C:/Users/adamb/PycharmProjects/office-quote-bot/sounds/",
              }

log_filename = properties.get("base_log_dir") + "twitter-bot_" + datetime.datetime.now().strftime("%Y%m%d") + properties.get('base_log_extension')
logging.basicConfig(filename=log_filename, format=properties.get('log_format'), level=logging.DEBUG, datefmt=properties.get('logging_date_format'))
log = logging.getLogger()


# Returns a boolean value for the use_connection property.
def get_use_connection() -> bool:
    use_conn = get_property_with_default("use_connection", False)
    if use_conn is not None and not isinstance(use_conn, bool):
        if isinstance(use_conn, str):
            use_conn = use_conn.strip()
            if use_conn.lower() == "true" or use_conn.lower() == "t" or use_conn.lower() == "yes" or use_conn.lower() == "y":
                use_conn = True
            else:
                use_conn = False
        elif isinstance(use_conn, (int, float)) and use_conn >= 0:
            use_conn = True
        else:
            use_conn = False
    return use_conn


# Returns the import path in proper format.
def get_python_import_path() -> str:
    import_path = get_property("import_path")
    if import_path is not None and isinstance(import_path, str):
        import_path = import_path.replace("\\", "/")
    return import_path


# Get a property.
# @param: name - The name of the property to get.
# Returns: Value
def get_property(name: str) -> str:
    if properties.get(name) and len(properties.get(name)) > 0:
        log.info(f"Got property '{name}' with value '{properties.get(name)}'")
        return properties.get(name)

    log.debug(f"Couldn't find the property '{name}'")


# Get a property by name with default value.
# @param: name - The name of the property to get.
# @param: default - The default property to return if property not found/set.
# Returns: Value or Default
def get_property_with_default(name: str, default: Any) -> Any:
    if get_property(name):
        return get_property(name)

    if get_property(name) is None and default is not None:
        log.info(f"Property '{name}' not found; returned provided default value '{default}'")
        return default

    log.debug(f"Couldn't get property '{name}' or return default value {default}... Returning None")
    return None
