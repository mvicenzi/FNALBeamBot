import json
from scripts.config import message_template

def load_payload():

    with open(message_template, 'r') as file:
        payload = json.load(file)
        return payload       

def sanitize(string):

    # remove \n or \r characters
    new_string = string.replace('\n','').replace('\r','')
    # remove double spaces (in case of "\r \r blabla" )
    sanitized = " ".join(new_string.split())
    return sanitized

def update_payload(payload, date, message):

    message = sanitize(message)

    for block in payload['blocks']:

        if block['type'] == 'section' and 'text' in block:
            block['text']['text'] = block['text']['text'].replace('%%date%%', date).replace('%%message%%', message)

    return payload
