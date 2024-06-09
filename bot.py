import argparse
import signal
import logging
import json
import requests
import time
import sys

from bs4 import BeautifulSoup
from slack_sdk import WebClient

from scripts.dbutils import init_db, is_timestamp_in_db, insert_message
from scripts.config import slack_token, slack_channel
from scripts.config import log_directory, url 
from scripts.payload import load_payload, update_payload

#----------------------------------------------------

def check_for_updates():

    date = None
    message = None
    timestamp = None

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
 
        for h1 in soup.find_all('h1'):
            if "Forbidden" in h1.text.strip():
                raise ConnectionError('Channel 13 page {}\nUnable to access the notifications page... are you on the Fermilab network?'.format(h1.text.strip()))

        # Extract the latest message and its timestamp
        latest_notice = soup.find('tr').find('td')
        date = latest_notice.find("title").text.strip()
        message = latest_notice.find("pre").text.strip()    
   
        struct_time = time.strptime(date, "%d-%b-%Y %H:%M:%S")
        timestamp = int(time.mktime(struct_time))   
   
    except Exception as e:
        logging.error("Scraping caught an exception:\n{}".format(str(e)))
        return

    logging.info('Last entry in channel 13: ["{}","{}","{}"]'.format(timestamp,date,message))

    # Check if the timestamp is already in the database
    # if not prepare to send message to Slack
    if not is_timestamp_in_db(timestamp):

        logging.info("Sending new message to {}...".format(slack_channel))

        payload = load_payload()
        payload = update_payload(payload, date, message)        
    
        # Initialize Slack client
        try: 
            client = WebClient(token=slack_token)

            response = client.chat_postMessage(
              channel=slack_channel,
              unfurl_links=False,
              blocks=payload['blocks'],
              text=f':fermilab: *Channel 13 Notification* on *{date}*\n{message}\n>_For more information, check <https://www-bd.fnal.gov/Elog|AD Elog>_.'
              )

            if response['ok']:
                insert_message(timestamp, date, message)
                logging.info("Added to bot status db!")

        except Exception as e:
            logging.error("Sending to Slack caught an exception:\n{}".format(str(e)))

    else:
        logging.info("No updates to send!")

#----------------------------------------------------

def signal_handler(sig, frame):
    logging.info('Keyboard interrupt. Stopping the bot!')
    sys.exit(0)

#----------------------------------------------------

def main(args):

    signal.signal(signal.SIGINT, signal_handler)

    ## Setup logging if requested
    logfile = '/dev/null'
    current_time = time.strftime('%Y%m%d')
    if args.logging:
        logfile = log_directory + 'bot_' + current_time + '.log'
    logging.basicConfig(filename=logfile,
                        level=logging.INFO,
                        filemode='a',
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Logging setup completed. Starting the bot...')

    ## Setup the messages database
    init_db()
    logging.info('Database initialization completed.')
    
    ## Check for updates and send messages
    while True:
        check_for_updates()
        time.sleep(int(args.wait))

#----------------------------------------------------

if __name__ == "__main__":

    args = argparse.ArgumentParser()
    args.add_argument("-w", "--wait", default=120)
    args.add_argument("-l", "--logging", default=True)
    main(args.parse_args())
