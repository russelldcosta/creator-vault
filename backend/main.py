# https://creator-vault-iaxy.onrender.com/
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Youtuber, SessionLocal
from pydantic import BaseModel
import schemas

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "russelldcosta7@gmail.com"
SENDER_PASSWORD = "ofaz bxcf wgsj epxw"         #From Google App Passwords

origins = [
    "https://your-frontend.vercel.app",  # ✅ Replace with your real frontend URL
    "http://localhost:3000",             # Optional: for local testing
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,               # OR use ["*"] for dev (not for production)
    allow_credentials=True,
    allow_methods=["*"],                 # ✅ Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],                 # ✅ Allow all headers (e.g. Content-Type)
)

# Dependency
def get_db():
    db = SessionLocal()
    try:        yield db
    finally:    db.close()


def save_youtuber(username, link, email, subscribers, genre):
    db = SessionLocal()
    try:
        existing = db.query(Youtuber).filter(Youtuber.link == link).first()
        if existing:                        return  # already in db
        yt = Youtuber(username=username, link=link, email=email, subscribers=subscribers, genre=genre,)
        db.add(yt)
        db.commit()
        print(f"✅ Saved to DB: {email}")
    except Exception as e:                  print(f"❌ DB Error: {e}")
    finally:                                db.close()








# Request model
class EmailRequest(BaseModel):
    subject: str
    body: str

@app.post("/send-emails")
def send_emails(payload: EmailRequest):
    db: Session = SessionLocal()
    youtubers = db.query(Youtuber).filter(Youtuber.email.isnot(None)).all()

    if not youtubers:   raise HTTPException(status_code=404, detail="No emails found.")

    for youtuber in youtubers:
        # Personalize email
        personalized_subject = payload.subject.replace("{{name}}", youtuber.username)
        personalized_body = payload.body.replace("{{name}}", youtuber.username)

        # Compose message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = youtuber.email
        msg["Subject"] = personalized_subject
        msg.attach(MIMEText(personalized_body, "plain"))

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, youtuber.email, msg.as_string())
        except Exception as e:      print(f"❌ Failed to send to {youtuber.username}: {e}")

    db.close()
    return {"message": "Emails sent successfully"}