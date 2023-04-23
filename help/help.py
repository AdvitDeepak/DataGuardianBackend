"""
help.py -- code that updates the table whenever needed 

- 

"""

from urllib.parse import urlparse 
from dotenv import load_dotenv
import openai 
import os 
import re

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
