# read environment variable "MyKey" and print its value
import os

# print actual time and date, format is YYYY-MM-DD HH:MM:SS
from datetime import datetime

# Get the current date and time
now = datetime.now()

# Format the date and time
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

# Print the formatted date and time
print(formatted_now)

timestamp_str = "2024-11-23T13:00:23.766804787Z"
# remove part after dot
timestamp_str = timestamp_str.split(".")[0]

print(timestamp_str)
parsed_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
print(parsed_timestamp)