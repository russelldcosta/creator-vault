from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Youtuber, SessionLocal
import schemas


app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/youtubers/", response_model=schemas.YoutuberRead)
def create_youtuber(yt: schemas.YoutuberCreate, db: Session = Depends(get_db)):
    existing = db.query(Youtuber).filter(Youtuber.link == str(yt.link)).first()
    if existing:
        print("-- Duplicate Youtuber, Skipped. --")
        return existing

    db_yt = Youtuber(**yt.model_dump(mode="json"))  #converts the Pydantic model — including HttpUrl — to plain JSON-safe Python types (str, int, etc.).
    db.add(db_yt)
    db.commit()
    db.refresh(db_yt)
    return db_yt


@app.get("/youtubers/", response_model=list[schemas.YoutuberRead])
def get_youtubers(db: Session = Depends(get_db)):
    return db.query(Youtuber).all()
