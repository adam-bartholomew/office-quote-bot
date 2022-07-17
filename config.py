properties = {"consumer_key": "",
              "consumer_secret": "",
              "access_token": "",
              "access_secret": "",
              "sleep_for": "880000",  # in seconds: 24 hours
              "comment_char": "#",
              "double_line_char": "&",
              "log_format": "[%(asctime)s] %(levelname)s:%(message)s",
              "logging_date_format": "%m/%d/%Y %I:%M:%S %p",
              "base_log_dir": "./logs/",
              "base_log_extension": ".log",
              "use_connection": False,
              "import_path": "C:/Users/adamb/OneDrive/Desktop/Quotes/new_imports/",
              "archive_path": "C:/Users/adamb/OneDrive/Desktop/Quotes/archive/",
              "archive_file_prefix": "dict_archive_",
              "base_export_extension": ".txt",
              }


# Returns a boolean value for the use_connection property.
def get_use_connection():
    use_conn = properties["use_connection"]
    if use_conn is not None and not isinstance(use_conn, bool):
        if isinstance(use_conn, str):
            use_conn = properties["use_connection"].strip()
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
def get_python_import_path():
    import_path = properties["import_path"]
    if import_path is not None and isinstance(import_path, str):
        import_path = import_path.replace("\\", "/")
    return import_path

