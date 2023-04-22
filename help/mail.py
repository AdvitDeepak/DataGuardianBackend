import cohere
from dotenv import load_dotenv
import os 

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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