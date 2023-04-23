# DigitalGuardianBackend

Backend for DigitalGuardian, a legal agent to exercise your data privacy rights! 


## Installation/Usage 

- Clone this repo to your local machine
- Create a conda env using `conda env create -f dg.yml`
- Activate the conda env using `conda activate dg` 

- Create a `.env` file that contains the following: 

```
OPENAI_KEY = "TBD"
COHERE_KEY = "TBD"
AIRTABLE_API_KEY = 'TBD'
AIRTABLE_BASE_ID = 'TBD'
AIRTABLE_COMPANY_TABLE = 'Company'
AIRTABLE_USER_TABLE = 'User'
AIRTABLE_HISTORY_TABLE = 'History'
MAIL_FILE = "mail.txt"

GMAIL_USER = "dataguardiantech@gmail.com"
GMAIL_PASS = "TBD"
APP_PASS = "TBD"
```

- Launch the server by running `python main.py`
- By default, the server will be hosted on `127.0.0.1:5000`

## Resources 

For more resources, feel free to checkout our ![main project page]()
