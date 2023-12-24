import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC6b925a966845e3e503120bd4ca1e0586'
    TWILIO_SYNC_SERVICE_SID = 'IS80202065bc53a07603bc21001f9d9ded'
    TWILIO_API_KEY = 'SKbbe8aa1cac6d7b080f59f717f208d015'
    TWILIO_API_SECRET = 'dqK47RHNJf8ZFYtD2PiWkswsuuafUc6A'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# A function to download text and store it in text file
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']    # “text” is the name which was given to the textarea in html and then store this in the text_from_notepad variable.

    with open('workfile.txt', 'w') as f:    # ‘f’ stores the data which we are writing into the file.

        f.write(text_from_notepad)

    path_to_store_txt = "workfile.txt"
    
# This send_file() function helps us to save the file in the mentioned folder with the mentioned name
    return send_file(path_to_store_txt, as_attachment=True)


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
