import json
import re
from scripts.config import message_template


def load_payload():

    with open(message_template, 'r') as file:
        payload = json.load(file)
        return payload       

def sanitize(string):

    # remove return characters that break Slack messages
    # replace \n or \r characters with periods
    new_string = string.replace('\n',' . ').replace('\r',' . ')

    # now clean up double or triple periods as needed!
    # first split based on whitespaces
    words = new_string.split()

    sanitized = ''
    last_word = ''
    for w in words:

         # if previous word ended in a period, don't add another one!
         if '.' in w and '.' in last_word:
             continue
             
         sanitized += w + ' '
         last_word = w   
	
    # if there were no periods and it was added by replacing a return character
    # there is a now a spurious whitespae, so let's remove it
    sanitized = sanitized.replace(' .','.')

    return sanitized

def update_payload(payload, date, message):

    message = sanitize(message)

    for block in payload['blocks']:

        if block['type'] == 'section' and 'text' in block:
            block['text']['text'] = block['text']['text'].replace('%%date%%', date).replace('%%message%%', message)

    return payload
