# https://creator-vault-iaxy.onrender.com/
# uvicorn main:app --host 0.0.0.0 --port 10000

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Youtuber, SessionLocal
from pydantic import BaseModel
import schemas

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.responses import FileResponse

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Gemini's AI enhancer
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Gmail config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "russelldcosta7@gmail.com"
SENDER_PASSWORD = "ofaz bxcf wgsj epxw"         #From Google App Passwords

origins = ["https://creator-vault-react.vercel.app",  "http://localhost:3000",]

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)   # OR use ["*"] for dev (not for production) 

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






@app.get("/manifest.json")
def manifest():
    return FileResponse("path/to/manifest.json")




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









class EnhanceInput(BaseModel):
    user_text: str

@app.post("/enhance-text")
def enhance_text(data: EnhanceInput):
    headers = {"Content-Type": "application/json"}
    prompt = f"You're responsible for rewriting the following text to sound more professional, clearer, and engaging which will be sent to Big Youtubers:\n\n{data.user_text}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    res = requests.post(GEMINI_URL, headers=headers, json=body)

    if res.status_code == 200:
        result = res.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        return {"enhanced_text": text}
    else:
        raise HTTPException(status_code=500, detail="AI service failed")