import cohere
from dotenv import load_dotenv
import os, ssl 
import os 

import imaplib
import email

import smtplib
from email.message import EmailMessage



def populate_company_email_draft(user_email, user_name, user_phone, company_email, company_name): 

    subject = f"CCPA - Data Deletion Request for {company_name} on Behalf of {user_name}"
    filename = os.getenv("MAIL_FILE")

    with open(filename, "r") as file:
        contents = file.read()
        
        # TODO - Replace the following occurrences w/ user data: 
        
        contents = contents.replace("[COMPANY_NAME]", company_name)
        contents = contents.replace("[YOUR_NAME]", user_name)
        contents = contents.replace("[YOUR_EMAIL]", user_email)
        contents = contents.replace("[YOUR_PHONE_NUMBER]", user_phone)


    return subject, contents 


def send_email(user_email, user_first, user_last, user_phone, company_email, company_name): 
    
    load_dotenv() 
    GMAIL_USER = os.getenv("GMAIL_USER")
    APP_PASS = os.getenv("GMAIL_PASS")
 
    user_name = f"{user_first} {user_last}"
    subject, body = populate_company_email_draft(user_email, user_name, user_phone, company_email, company_name)

    em = EmailMessage()
    em['From'] = GMAIL_USER
    em['Cc'] = user_email 
    em['To'] = company_email
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(GMAIL_USER, APP_PASS)
        smtp.sendmail(GMAIL_USER, company_email, em.as_string())

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