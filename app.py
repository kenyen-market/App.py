from flask import Flask
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route("/")
def home():
    return "TSMC Watcher is running."

@app.route("/notify")
def notify():
    message = Mail(
        from_email=os.environ.get("FROM_EMAIL"),
        to_emails=os.environ.get("TO_EMAIL"),
        subject="TSMC Watcher 啟動通知",
        plain_text_content="你的 Web Service 已經成功啟動，將會開始追蹤台積電股價。"
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        return f"Email sent! Status: {response.status_code}"
    except Exception as e:
        return f"Email 發送失敗：{e}"
