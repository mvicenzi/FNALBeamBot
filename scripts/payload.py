import json
import re
from scripts.config import message_template


def load_payload():

    with open(message_template, 'r') as file:
        payload = json.load(file)
        return payload       

def sanitize_single_line(string):

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
         if '.' in w and (('.' in last_word) or (':' in last_word) or ("!" in last_word)):
             continue
             
         sanitized += w + ' '
         last_word = w   
	
    # if there were no periods and it was added by replacing a return character
    # there is a now a spurious whitespace, so let's remove it
    sanitized = sanitized.replace(' .','.')

    return sanitized

def sanitize_multiple_lines(string):

    # split the message around the return character that breaks Slack messages
    # each element is a line, but some are whitespace only lines
    # remove lines with only one whitespace or one period!
    lines = string.split('\r')
    lines = [ s.lstrip(' ').rstrip(' ') for s in lines if not s.isspace() ]
    lines = [ s for s in lines if s != "." ]
    message = ""
    
    # we now rebuild the message by putting together the lines
    # simple add '\n' unless it's only one line or the last line
    for i,l in enumerate(lines):

        line = l
	# if there is already a period at the end, that's great
        # otherwise add it to satisfy everybody's OCD
        if ((l[-1] != '.') and (l[-1] != '!') and (l[-1] != ':')):
            line += '.'

        if i==0 and len(lines)<2: #only 1 line     
            message += line
        elif i == len(lines)-1: #last line
            message += line
        else: 
            message += line + '\n'

    return message

def update_payload(payload, date, message):

    message = sanitize_multiple_lines(message)

    # if payload has a '>' character for the Slack quote style,
    # they'll break on the '\n' in the Slack message
    # if so, change '\n' to '\n>'
    for block in payload['blocks']:

        if block['type'] == 'section' and 'text' in block:

            template = block['text']['text']
            index = template.find('%%message%%')
            if template[index-1] == '>':
                message = message.replace('\n','\n>')

            block['text']['text'] = block['text']['text'].replace('%%date%%', date).replace('%%message%%', message)

    return payload
