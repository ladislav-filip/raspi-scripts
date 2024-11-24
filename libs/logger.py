from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_error(message):
    # create message text with timestamp
    message = f"{get_timestamp()} - ERROR: {message}"
    print(message)

def log_info(message):
    # create message text with timestamp
    message = f"{get_timestamp()} - INFO: {message}"
    print(message)    