# InkMonitor

Checks ink levels on an Olivetti MF223 MFD or similar and notifies the user when ink is low. Note: this readme is very sparse, I will improve it when I have more time

## How does it work?
InkMonitor uses Selenium with a headless browser (I've chosen Chromium) to pull the HTML from the printer dashboard page. This is due to weird JS and cookie stuff which I couldn't be bothered to reverse-engineer into an HTTP request. It then parses the HTML with BeautifulSoup and extracts each of the 4 ink levels from the page.
If any ink level is below 10%, the user is sent an SMS message to warn them, and if a cartridge is empty, the user is sent a different message warning them of the empty cartridge. If all cartridges are above 10% no message is sent.

## Requirements
Make sure you have all these installed or set up (more info coming when I have more time)
- Twilio account SID and auth token
- Local IP address of the MFD
- Selenium and ChromeDriver
- BeautifulSoup4
- LXML
- Python 3

## Install
Once the requirements are met, put the Twilio account SID and auth token in `/etc/environment` as below:
```
TWILIO_ACCOUNT_SID="acc sid here"
TWILIO_AUTH_TOKEN="auth token here"
```
Then hardcode the printer IP (it's late, I can't be bothered to put that in env as well lol):
- Find `PRINTER_IP` near the top of the code
- Change `IP_GOES_HERE` to the local IP address of the printer
Go to the bottom of the code and change:
- `TWILIO_NUMBER_HERE` to the number assigned to you by Twilio
- `USER_NUMBER_HERE` to whatever number you want to sent the SMS to (if on Twilio trial, it needs to be a verified caller ID)
Test by running
```bash
python3 ink-monitor.py
```
If it works you could add a cronjob!! I'd suggest weekly, here's how to do it for every Monday at 14:00
- Run `crontab -e`
- Add
  ```
  0 14 * * 1 /usr/bin/python3 /path/to/ink-monitor.py >> /path/to/ink-monitor.log 2>&1
  ```
- (make sure to change /path/to to the actual path to!)
- Ctrl-X, Y, enter
Now the test should run every Monday at 2pm, you can check the file ink-monitor.log to see if it's worked!!
