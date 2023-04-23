import cohere
from dotenv import load_dotenv
import os 

import imaplib
import email

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def populate_company_email_draft(data): 

    filename = os.getenv("MAIL_FILE")

    with open(filename, "r") as file:
        contents = file.read()
        
        # TODO - Replace the following occurrences w/ user data: 
        
        contents = contents.replace("[COMPANY_NAME]", None)
        contents = contents.replace("[YOUR_NAME]", None)
        contents = contents.replace("[YOUR_EMAIL]", None)
        contents = contents.replace("[YOUR_PHONE_NUMBER]", None)


    return contents 


def send_email(user_email, user_first, user_last, user_phone, company_email): 
    
    load_dotenv() 
    GMAIL_USER = os.getenv("GMAIL_USER")
    GMAIL_PASS = os.getenv("GMAIL_PASS")

    message = MIMEMultipart()
    message['Subject'] = 'Subject line of your email'
    message['From'] = "OUR_EMAIL_ADDRESS"
    message['CC'] = user_email 
    message['To'] = company_email

    body = body # TODO -- load in the email and update necessary fields 

    message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS)

    # send the email
    text = message.as_string()
    server.sendmail(message['From'], message['To'], message['CC'], text) # check the CC process
    server.quit()

    print('Email sent successfully!')


def parse_email_to_get_inbox(): 

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

# Generate main email template (only to be called once) via CoHere

def main(): 

    load_dotenv()   
    cohere_api_key = os.getenv("COHERE_KEY")
    co = cohere.Client(cohere_api_key)

    prompt = "Generate CCPA compliant email demanding that Company X deletes my data" 

    prediction = co.generate(
                model='large',
                prompt=prompt,
                max_tokens=10)

    res = prediction.generations[0].text


    filename = os.getenv("MAIL_FILE")

    if not os.path.isfile(filename):
        with open(filename, "w") as file:
            file.write(res)

        
if __name__ == "__main__": 
    main() 