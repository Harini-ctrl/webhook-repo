
```markdown
# 🚀 GitHub Webhook Receiver Project

A Flask + MongoDB app that listens for GitHub webhook events (push, pull request, merge), stores them in a database, and displays them in a live-updating UI.  

This project is designed to **simulate handling GitHub webhook events** as part of the assignment.

---

## ✅ Features

- 📦 Receives GitHub webhook POST requests at `/webhook`
- 🗃️ Stores relevant event data in MongoDB
- 🖥️ Exposes `/events` endpoint to fetch recent events
- 🌐 Simple UI page at `/` that refreshes every 15 seconds to display new events

---

## ✅ Folder Structure

```

webhook-repo/
│
├── templates/
│   └── index.html         # HTML page for UI
├── app.py                 # Flask server code
├── requirements.txt       # All Python dependencies
└── README.md              # Project documentation

````

---

## ✅ Requirements

- Python 3.x
- MongoDB (local or Atlas)
- ngrok (for tunneling localhost to GitHub)

---

## ✅ Setup Instructions

### 1️⃣ Clone this repository
```bash
git clone https://github.com/yourusername/webhook-repo.git
cd webhook-repo
````

---

### 2️⃣ Create & Activate a Virtual Environment

✅ **Windows**:

```bash
python -m venv venv
venv\Scripts\activate
```

✅ **macOS/Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Make Sure MongoDB is Running

✅ For local MongoDB:

```bash
mongod
```

✅ Or update your `app.py` with your **MongoDB Atlas URI** if using cloud:

```python
client = MongoClient('your-atlas-uri')
```

---

### 5️⃣ Start the Flask Server

```bash
python app.py
```

✅ Flask will run on:

```
http://localhost:5000
```

---

### 6️⃣ Expose Localhost to Internet with ngrok

✅ In another terminal:

```bash
ngrok http 5000
```

✅ Example output:

```
Forwarding https://abc1234.ngrok.io -> http://localhost:5000
```

✅ Use this HTTPS URL **with /webhook** when setting up your GitHub webhook:

```
https://abc1234.ngrok.io/webhook
```

---

### 7️⃣ Configure GitHub Webhook

✅ In your **action-repo** on GitHub:

* Go to **Settings → Webhooks → Add webhook**
* **Payload URL**:

  ```
  https://YOUR_NGROK_ID.ngrok.io/webhook
  ```
* **Content Type**:

  ```
  application/json
  ```
* **Events**:

  * Choose **Let me select individual events**
  * ✅ Push
  * ✅ Pull requests
* Click **Add Webhook**

---

### 8️⃣ Test Your Webhook

✅ Make a **push** or **open a Pull Request** in your **action-repo**.

✅ Your Flask server will receive the event, parse it, and store it in MongoDB.

✅ Visit your UI:

```
http://localhost:5000
```

✅ See events displayed live, refreshing every 15 seconds!

---

## ✅ Example Event Display in UI

```
Harini-ctrl pushed to main on Fri, 4 July 2025 - 07:35 UTC
```

✅ Supports:

* push
* pull\_request (opened)
* merged pull\_request

---

## ✅ Regenerate requirements.txt

After installing new packages:

```bash
pip freeze > requirements.txt
```

---

## ✅ Notes

* The server stores timestamps in ISO 8601 UTC format.
* The frontend fetches the 20 most recent events every 15 seconds.
* The project includes clean logging for easy review and debugging.

---

## ✅ Author

Harini Srutakeerti
https://github.com/Harini-ctrl/

