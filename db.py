import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = "sqlite:///lecture_notes.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Transcript(Base):
    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    content: Mapped[str] =mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))


def init_db():
    Base.metadata.create_all(bind=engine)


