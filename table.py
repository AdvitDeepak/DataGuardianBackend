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
    else: user_data = [d['fields'] for d in hist_entries]

    return {"user_profile": user_profile, "user_data": user_data}
    


# Helper Funcs: None 
def check_company_match(company_name, data):
    for d in data:
        fields = d.get('fields', {})
        if fields.get('Company') == company_name:
            return True
    return False
def update_history_airtable(user_email, history): 
    website_counts = {}

    for site in history:
        parsed_url = urlparse(site)
        domain = parsed_url.netloc.split('.')

        if len(domain) > 2: company_name = domain[-2]
        else: company_name = domain[0]
        
        if company_name in website_counts: website_counts[company_name] += 1
        else: website_counts[company_name] = 1

    entries = airtable_history_table.search('User', user_email)
    company_names = []
    if len(entries) > 0:
        company_names = {record['fields']['Company'] for record in entries}
    for website, count in website_counts.items():
        print(website)
        print(count)
        print(entries)
        if website not in company_names:
            airtable_history_table.insert({
                'User': user_email,
                'Company':  website,
                'Times Visited': count,
                'Status': "Unguarded"
            })
        else:
            airtable_history_table.update(entries[0]['id'], {'Times Visited': entries[0]['fields']['Times Visited'] + count})



# Helper Funcs: send_email

def update_website_airtable(user_email, websites):

    entries = airtable_user_table.search('User', user_email)

    if len(entries) == 0: return None 
    user_first = entries[0]["fields"]['First Name']
    user_last = entries[0]["fields"]['Last Name']
    user_phone = entries[0]["fields"]['Phone Number']

    entries = airtable_history_table.search('User', user_email)
    company_statuses = {}
    if len(entries) > 0:
        company_statuses = {record['fields']['Company']:(record["fields"]['Status'], record['id']) for record in entries}
    
    for website in websites: 
        entries = airtable_company_table.search('Company', website)
        print(entries)
        if len(entries) == 0:
            # Call openai function to add to company table  
            company_email = openai_call_to_get_email(website)
            airtable_company_table.insert({'Company' : website, "Email" : company_email})
        else: 
            company_email = entries[0]["fields"]['Email']

        if company_statuses[website][0] == "Unguarded": 
            send_email(user_email, user_first, user_last, user_phone, company_email, website)
            airtable_history_table.update(company_statuses[website][1], {'Status': "Pending"})
