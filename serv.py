"""
serv.py -- code that defines the REST API's endpoints 

The following are the valid endpoints: 
- /update_user (POST)
- /get_user (GET)
- /update_history (POST)
- /update_website(POST)

"""

from flask import Flask, request, jsonify
from table import update_user_airtable, get_user_airtable, update_history_airtable, update_website_airtable


def create_app(): 

    app = Flask(__name__)


    # 0) GET - just for testing purposes to ensure server is healthy
    
    @app.route('/', methods=['GET'])
    def default():
        return {'response' : "Working API server"}, 200


    
    # 1) POST - we get the user's information (based on whatever fields are populated)
    
    @app.route('/update_user', methods=['POST'])
    def update_user(): 

        data = request.get_json() 
        cnt = update_user_airtable(data["user_email"], data["fields_to_update"])
        
        return{'response' : f"Updated {cnt} fields"}, 200 


    
    # 2) POST - Get all the user's information (based on the inputted user id)
    
    @app.route('/get_user', methods=['GET'])
    def get_user():
       
        user_email = request.args.get('user_email')

        user_info = get_user_airtable(user_email)
        return jsonify(user_info), 200 


    
    # 3) POST - Get history of users (in order to determine companies)
    
    @app.route('/update_history', methods=['POST'])
    def update_history(): 

        data = request.get_json()
        user_email = data["user_email"]["email"]
        print(user_email)
        history = data["history"]
        print(len(history))
        update_history_airtable(user_email, history)

        return{'response' : f"Updated history"}, 200 
 


    # 4) POST - Get websites chosen by the user (in order to send the emails)

    @app.route('/update_websites', methods=['POST'])
    def update_websites():
        data = request.get_json() 
        user_email = data["user_email"]
        history = data["history"]
        update_website_airtable(user_email, history)
        return{'response' : f"Emailed"}, 200 

    return app
   
