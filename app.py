from utils import fetch_reply
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')

    # Create reply
    resp = MessagingResponse()
    resp.message(fetch_reply(msg,sender))
    # resp.message("You said: {}".format(msg)).media("https://dictionary.cambridge.org/images/thumb/black_noun_002_03536.jpg")
    return str(resp)

if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)