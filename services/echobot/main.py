import os
import time
import hmac
import hashlib
from flask import Flask, request, abort, jsonify

app = Flask(__name__)

SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET', '')

def verify_slack_request(req):
    timestamp = req.headers.get('X-Slack-Request-Timestamp', '')
    if not timestamp:
        return False
    # protect against replay
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False
    sig_basestring = f"v0:{timestamp}:{req.get_data(as_text=True)}"
    my_sig = 'v0=' + hmac.new(
        SLACK_SIGNING_SECRET.encode('utf-8'),
        sig_basestring.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    slack_sig = req.headers.get('X-Slack-Signature', '')
    return hmac.compare_digest(my_sig, slack_sig)

@app.route('/', methods=['GET'])
def index():
    return 'EchoBot is running'

@app.route('/events', methods=['POST'])
def events():
    if not verify_slack_request(request):
        abort(401)
    data = request.json
    # URL verification challenge
    if data.get('type') == 'url_verification':
        return jsonify({'challenge': data.get('challenge')})
    # handle event callbacks
    # minimal example: respond to app_mention by echoing text (use bot token in production)
    event = data.get('event', {})
    if event.get('type') == 'app_mention':
        # in production, post message back to Slack using SLACK_BOT_TOKEN
        text = event.get('text')
        # no external call here — placeholder
        app.logger.info(f"Mention received: {text}")
    return ('', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
