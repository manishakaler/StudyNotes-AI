import os
from dotenv import load_dotenv
from google import genai
from sqlalchemy import select
from db import SessionLocal, Transcript
import streamlit as st


load_dotenv()

API_KEY= None, MODEL_NAME = None
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = os.getenv("GEMINI_API_KEY")

if hasattr(st, "secrets") and "MODEL_NAME" in st.secrets:
    MODEL_NAME = st.secrets["MODEL_NAME"]
else:
    MODEL_NAME = os.getenv("MODEL_NAME")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set.")
if not API_KEY:
    raise RuntimeError("Please select a gemini model.")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = os.getenv("MODEL_NAME")


def get_all_transcripts():
    with SessionLocal() as session:
        stmt = select(Transcript).order_by(Transcript.created_at.desc())
        return session.execute(stmt).scalars().all()
    

def get_transcript_by_id(transcript_id: int):
    with SessionLocal() as session:
        return session.get(Transcript, transcript_id)
    

def save_transcript(title: str, content: str):
    with SessionLocal() as session:
        existing = session.execute(
            select(Transcript).where(Transcript.title == title)
        ).scalar_one_or_none()

        if existing:
            existing.content = content
            session.commit()
            session.refresh(existing)
            return existing, "updated"
        
        transcript = Transcript(title=title, content=content)
        session.add(transcript)
        session.commit()
        session.refresh(transcript)
        return transcript, "created"


def generate_notes(transcript: str) -> str:
    prompt = f"""
You are helping a university student study from a lecture transcipt.

Generate the output in following sections:

## Summary
Give a concise summary of the lecture

## Key Concepts & Examples
List the main concepts with 1-2 sentence explainations followed by important examples, case studies, or illustrations mentioned.

## Likely Exam Questions
Write 5 likely exam questions based on the lecture

Transcript:
{transcript}
"""
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text

def answer_question(transcript: str, question: str) -> str:
    prompt = f"""
You are a helpful teaching assistant helping a student study from a lecture transcript.

You must follow these rules:

1. You can ONLY use information that is explicitly present in the transcript.
2. You must NOT use outside knowledge or anything you "know" from pretraining.
3. If the transcript does not contain enough information to answer,
   or if the question is unclear / random / unrelated,
   you MUST answer with exactly:

   I couldn't find a clear answer to that in the provided transcript.

4. Never try to guess or infer beyond what is written in the transcript.

Now decide:

- First, check if the question can be answered based only on the transcript.
- If it cannot, reply with exactly:
  I couldn't find a clear answer to that in the provided transcript.

- If it can, answer in this format:

### Simple Explanation
Explain the concept clearly in 2-4 sentences.

### Deeper Understanding
Give a few bullet points with a slightly deeper explanation.

### From This Lecture
Explain how this concept appeared in the lecture transcript.


Transcript:
{transcript}

Question:
{question}
"""
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text