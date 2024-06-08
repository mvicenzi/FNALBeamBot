import json
from scripts.config import message_template

def load_payload():

    with open(message_template, 'r') as file:
        payload = json.load(file)
        return payload       

def update_payload(payload, date, message):

    for block in payload['blocks']:

        if block['type'] == 'section' and 'text' in block:
            block['text']['text'] = block['text']['text'].replace('%%date%%', date).replace('%%message%%', message)

    return payload
