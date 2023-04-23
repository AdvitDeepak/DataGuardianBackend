"""
main.py -- code that starts up the REST API server 

"""

from serv import create_app 
from flask_cors import CORS
import os 

HOST = "localhost"
PORT = 5001


if __name__ == "__main__": 

    app = create_app()
    CORS(app)

    print("PID:", os.getpid())
    app.run(host=HOST, port=PORT)
