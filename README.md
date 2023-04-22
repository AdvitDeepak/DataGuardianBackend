# DigitalGuardian

Work in progress! 

## Installation/Usage 

- Clone this repo to your local machine
- Create a conda env using `conda env create -f dg.yml`
- Activate the conda env using `conda activate dg` 

- Create a `.env` file that contains the following: 

'''
OPENAI_KEY = "TBD"
COHERE_KEY = "TBD"
AIRTABLE_API_KEY = 'keyxYSDAiK8dePwPY'
AIRTABLE_BASE_ID = 'appqIgPRLfvB3CY0w'
AIRTABLE_COMPANY_EMAILS = 'Company Emails'
MAIL_FILE = "mail.txt"

GMAIL_USER = "dataguardiantech@gmail.com"
GMAIL_PASS = "babxyZ-wifvi6-gawpes"
'''

- Launch the server by running `python main.py`
- By default, the server will be hosted on `127.0.0.1:5000`