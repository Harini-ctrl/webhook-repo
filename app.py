from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)

# ========================
# MongoDB Connection Setup
# ========================
# Replace with your Atlas URI if needed
client = MongoClient('mongodb://localhost:27017/')
db = client['webhookdb']
events_collection = db['events']


# ========================
# Home Route
# ========================
# Serves the UI page
@app.route('/')
def home():
    print("[INFO] GET / → Rendering index.html")
    return render_template('index.html')


# ========================
# Webhook Receiver Route
# ========================
# Receives POST requests from GitHub Webhooks
@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json

    print("\n=== [Webhook Received] ===")
    print(f"Event Type: {event_type}")

    parsed = parse_event(event_type, payload)

    if parsed:
        events_collection.insert_one(parsed)
        print(f"[DB] Inserted Event: {parsed}")
    else:
        print("[WARN] Ignored unhandled or invalid event.")

    print("=== [Webhook Processing Complete] ===\n")
    return jsonify({"status": "received"}), 200


# ========================
# Events Fetch Route
# ========================
# Returns the 20 most recent events as JSON
@app.route('/events', methods=['GET'])
def get_events():
    events = list(events_collection.find().sort("timestamp", -1).limit(20))
    for e in events:
        e['_id'] = str(e['_id'])
    print(f"[INFO] GET /events → Returned {len(events)} events")
    return jsonify(events)


# ========================
# Event Parsing Helper
# ========================
# Transforms GitHub webhook payload into our DB schema
def parse_event(event_type, payload):
    utc_time = datetime.now(pytz.UTC).isoformat()

    if event_type == "push":
        try:
            result = {
                "action": "push",
                "author": payload["pusher"]["name"],
                "from_branch": None,
                "to_branch": payload["ref"].split("/")[-1],
                "timestamp": utc_time
            }
            print(f"[PARSE] Push Event Parsed: {result}")
            return result
        except (KeyError, TypeError) as e:
            print(f"[ERROR] Failed to parse push event: {e}")
            return None

    if event_type == "pull_request":
        try:
            action = payload.get("action")
            pr = payload["pull_request"]
            author = pr["user"]["login"]
            from_branch = pr["head"]["ref"]
            to_branch = pr["base"]["ref"]
            merged = pr.get("merged", False)

            if action == "opened":
                result = {
                    "action": "pull_request",
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": utc_time
                }
                print(f"[PARSE] Pull Request Opened Parsed: {result}")
                return result
            elif action == "closed" and merged:
                result = {
                    "action": "merge",
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": utc_time
                }
                print(f"[PARSE] Merge Event Parsed: {result}")
                return result
            else:
                print(f"[INFO] Ignored PR action: {action}")
        except (KeyError, TypeError) as e:
            print(f"[ERROR] Failed to parse pull_request: {e}")
            return None

    print(f"[WARN] Unhandled Event Type: {event_type}")
    return None


# ========================
# App Runner
# ========================
if __name__ == '__main__':
    print("🚀 Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)
