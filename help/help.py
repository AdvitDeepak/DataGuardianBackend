"""
help.py -- code that updates the table whenever needed 

- 

"""

from urllib.parse import urlparse 
from dotenv import load_dotenv
import openai 
import os 
import re


import imaplib
import email


def from_history_get_companies(): 

    # log in to your email account
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('your_email@gmail.com', 'your_password')
    mail.select('inbox')

    # search for messages matching a specific criteria
    result, data = mail.search(None, 'FROM', 'sender@example.com')

    # iterate through the messages and extract information
    for num in data[0].split():
        result, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        print('Message subject:', msg['subject'])
        print('From:', msg['from'])
        print('To:', msg['to'])
        print('Date:', msg['date'])
        print('Message body:', msg.get_payload())
        print('---------------------------------------')

    # log out of your email account
    mail.close()
    mail.logout()




def openai_call_to_get_email(company_name): 

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_KEY")
 
    message = f"Find the email of {company_name}'s data privacy team. The email address should be returned as the output, and it should be a valid email.?"
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the email address from the response using regular expressions
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    email = re.findall(email_regex, response.choices[0].text)[0]

    return email 
