"""
table.py -- code that implements the REST API's endpoints 

- /update_user (POST)    --> update_user_airtable() 
- /get_user (GET)        --> get_user_airtable()
- /update_history (POST) --> update_websites_airtable() 
- /update_website(POST)  --> 

"""

import os 
from airtable import airtable
from urllib.parse import urlparse 


from dotenv import load_dotenv
from help.mail import send_email 
from help.help import openai_call_to_get_email

load_dotenv() 
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_USER_TABLE = os.getenv("AIRTABLE_USER_TABLE")
AIRTABLE_HISTORY_TABLE = os.getenv("AIRTABLE_HISTORY_TABLE")
AIRTABLE_COMPANY_TABLE = os.getenv("AIRTABLE_COMPANY_TABLE")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

global airtable_user_table
global airtable_history_table
global airtable_company_table

airtable_user_table = airtable.Airtable(
    AIRTABLE_BASE_ID, AIRTABLE_USER_TABLE, AIRTABLE_API_KEY)

airtable_history_table = airtable.Airtable(
    AIRTABLE_BASE_ID, AIRTABLE_HISTORY_TABLE, AIRTABLE_API_KEY)

airtable_company_table = airtable.Airtable(
    AIRTABLE_BASE_ID, AIRTABLE_COMPANY_TABLE, AIRTABLE_API_KEY)

# ================================================================ #

# Helper Funcs: None 

def update_user_airtable(user_email, fields_to_update): 
    entries = airtable_user_table.search('User', user_email)
    if len(entries) == 0: 
        airtable_user_table.insert(fields_to_update) 
    else: airtable_user_table.update(entries[0]['id'], fields_to_update)



# Helper Funcs: None 

def get_user_airtable(user_email):
    entries = airtable_user_table.search('User', user_email)

    if len(entries) == 0: return None
    else: user_profile = entries[0]['fields']

    hist_entries = airtable_history_table.search('User', user_email)

    if len(hist_entries) == 0: user_data =  []
    else: user_data = hist_entries['fields']

    return {"user_profile": user_profile, "user_data": user_data}
    


# Helper Funcs: None 

def update_history_airtable(user_email, history): 
    website_counts = {}

    for site in history:
        parsed_url = urlparse(site['url'])
        domain = parsed_url.netloc.split('.')

        if len(domain) > 2: company_name = domain[-2]
        else: company_name = domain[0]
        
        if company_name in website_counts: website_counts[company_name] += 1
        else: website_counts[company_name] = 1


    for website, count in website_counts.items():
        entries = airtable_history_table.search([ 'User', user_email, 'Company', website ])
        
        if len(entries) == 0:
            airtable_history_table.insert({
                'User': user_email,
                'Company': website,
                'Times Visited': count,
                'Status': "Visited"
            })
        else:
            airtable_history_table.update(entries['id'], {'Times Visited': entries['fields']['Times Visited'] + count})



# Helper Funcs: send_email

def update_website_airtable(user_email, websites):

    entries = airtable_user_table.search('User', user_email)

    if len(entries) == 0: return None 

    user_first = entries[0]['First Name']
    user_last = entries[0]['Last Name']
    user_phone = entries[0]['Phone Number']


    for website in websites: 
        entries = airtable_company_table.search('Company', website)

        if len(entries) == 0:
            # Call openai function to add to company table  
            company_email = openai_call_to_get_email(website)
            airtable_company_table.insert({'Company' : website, "Email" : company_email})
        else: 
            company_email = entries[0]['Email']
        
        entries = airtable_history_table.search({'User': user_email, 'Company': website})
        
        if len(entries) == 0: return None 

        status = entries[0]['Status']

        if status == "Visited": 
            send_email(user_email, user_first, user_last, user_phone, company_email, website)
            airtable_history_table.update(entries[0]['id'], {'Status': "Pending"})
