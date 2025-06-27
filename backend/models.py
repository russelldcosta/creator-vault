from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Define Base
Base = declarative_base()

# SQLAlchemy model
class Youtuber(Base):
    __tablename__ = "youtubers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    link = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True)
    subscribers = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)

#DB setup (SQLite for now)
DATABASE_URL = "sqlite:///./youtubers.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create the table(s)
Base.metadata.create_all(bind=engine)
