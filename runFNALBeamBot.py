import argparse
import logging
import json
import requests
import time
import sys

from bs4 import BeautifulSoup
from slack_sdk import WebClient

from scripts.dbutils import init_db, is_timestamp_in_db, insert_message
from scripts.config import slack_token, slack_channels, log_directory, log_level, url 
from scripts.payload import load_payload, update_payload
from scripts.rotate import TimedPatternFileHandler

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

    logging.info('Last entry in channel 13: ["{}","{}","{}"]'.format(timestamp,date,message.replace('\r','')))

    # Check if the timestamp is already in the database
    # if not prepare to send message to Slack
    if not is_timestamp_in_db(timestamp):

        payload = load_payload()
        payload = update_payload(payload, date, message)        

        logging.debug(payload['blocks'])

        success = False
        try:
            
            # Initialize Slack client
            client = WebClient(token=slack_token)
            
            # Send messages to Slack channels
            for slack_channel in slack_channels:
            
                try: 
                    logging.info("Sending new message to {}...".format(slack_channel))
                    response = client.chat_postMessage(
                      channel=slack_channel,
                      unfurl_links=False,
                      blocks=payload['blocks'],
                      text=f':fermilab: *Channel 13 Notification* on *{date}*\n{message}\n>_For more information, check <https://www-bd.fnal.gov/Elog|AD Elog>_.'
                    )

		    # if (at least) one of the channels succeeds
                    if response['ok']:
                        success = True

                except Exception as e:
                    logging.error("Sending to {} caught an exception:\n{}".format(slack_channel,str(e)))
     
            # Update the db is at least one channel was able to get the message
            # if we wait for all of them to succeed, we risk sending multiple identical messages      
            if success:
                insert_message(timestamp, date, message)
                logging.info("Added to bot status db!")
	
        except Exception as e:
            logging.error("Slack initilization failed:\n{}".format(str(e)))
    
    else:
        logging.info("No updates to send!")

#----------------------------------------------------
#----------------------------------------------------

def main():

    ## Setup requested logging level
    logger = logging.getLogger()
    logger.setLevel(log_level.upper())
    
    logfile = log_directory + 'bot_%Y%m%d.log' 
    handler = TimedPatternFileHandler(logfile, when="MIDNIGHT", backupCount=7)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)    
    logger.addHandler(handler)

    logging.info('Logging setup completed. Starting the bot...')

    ## Setup the messages database
    init_db()
    logging.info('Database initialization completed.')
    
    ## Check for updates and send messages
    check_for_updates()

    logging.info("Exiting...")

#----------------------------------------------------

if __name__ == "__main__":

    try:
        main()

    except Exception as e:
        logging.error("Previously uncaught exception:\n{}".format(str(e)))
        logging.info("Exiting...")
        sys.exit(1)
