# Imports
import os
from twilio.rest import Client
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from datetime import datetime

# Constants
ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
PRINTER_IP = "IP_GOES_HERE"

# Variables
ink_levels = []
ink_empty = False
ink_low = False
message_chunk_start = "Copier ink is "
message_chunk_state = ""
message_chunk_levels = ""
final_message = ""

# Twilio client setup
print(datetime.now(), " Creating Twilio client...")
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Pull root HTML using Selenium
print(datetime.now(), " Opening printer webpage...")
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get("http://" + PRINTER_IP)
time.sleep(10)
print(datetime.now(), " Saving page...")
page_source = driver.page_source
driver.quit()

# Make HTML into some beautiful soup
print(datetime.now(), " Parsing page...")
soup = BeautifulSoup(page_source, 'lxml')

# Save relevant ink level values from page
for i in range(1, 5):
    ink_levels.append(int(soup.find(class_="LevelPer" + str(i)).get("value")))
# Check which status is necessary
for ink in ink_levels:
    if ink == 0: 
        ink_empty = True
        break
    if ink < 10:
        ink_low = True

# Assign status for inclusion in final message
if ink_empty:
    message_chunk_state = "EMPTY"
elif ink_low:
    message_chunk_state = "LOW"
else:
    message_chunk_state = "OK"

# Check if necessary to send SMS
if message_chunk_state != "OK":
    # Setup levels section to print
    message_chunk_levels = " - Yel {}%, Mag {}%, Cya {}%, Bla {}%".format(ink_levels[0], ink_levels[1], ink_levels[2], ink_levels[3])

    # Concatenate final message to send to user
    final_message = message_chunk_start + message_chunk_state + message_chunk_levels
    print(datetime.now(), " Sending message: " + final_message)

    # Tell Twilio to send the text
    message = client.messages \
        .create(
            body=final_message,
            from_='TWILIO_NUMBER_HERE',
            to='USER_NUMBER_HERE'
        )

    print(datetime.now(), " Sent message ID " + message.sid + " to user.")
else:
    print("Ink levels OK, message not sent.")