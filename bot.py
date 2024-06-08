import requests
import time
from bs4 import BeautifulSoup
from slack_sdk import WebClient
from scripts.dbutils import init_db, is_timestamp_in_db, insert_message
from scripts.config import url, slack_token, channel

# Initialize Slack client
client = WebClient(token=slack_token)

def check_for_updates():

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the latest message and its timestamp
    latest_notice = soup.find('tr').find('td')
    date = latest_notice.find("title").text.strip()
    message = latest_notice.find("pre").text.strip()
   
    struct_time = time.strptime(date, "%d-%b-%Y %H:%M:%S")
    timestamp = int(time.mktime(struct_time))   
    
    print("Last entry: [{},{},{}]".format(timestamp,date,message))

    # Check if the timestamp is already in the database
    # if not prepare to send message to Slack
    if not is_timestamp_in_db(timestamp):

        print("Sending new message to {}...".format(channel))
        slack_blocks = '[ {"type": "divider"},'
        slack_blocks += '{"type": "section","text": {"type": "mrkdwn","text": ":fermilab: *Channel 13 Notification* on *' + date + '*'
        slack_blocks += '\n>' + message +'\n>_For more information, check <https://www-bd.fnal.gov/Elog|AD Elog>_."}},'
        slack_blocks += '{"type": "divider"}]'
        
        response = client.chat_postMessage(
            channel=channel,
            unfurl_links=True,
            blocks=slack_blocks,
	    text=f':fermilab: *Channel 13 Notification* on *{date}*\n{message}\n>_For more information, check <https://www-bd.fnal.gov/Elog|AD Elog>_.'
        )
        if response['ok']:
            insert_message(timestamp, date, message)
            print("Added to bot status db!")
        print(response)
    else:
        print("No updates to send!")


def main():
    init_db()
    check_for_updates()

if __name__ == "__main__":
    main()
