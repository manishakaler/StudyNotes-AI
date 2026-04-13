# Lecture Notes AI Assistant

Lecture Notes AI Assistant is a Streamlit-based study assistant that turns lecture transcripts into structured notes and grounded question answering. The project is built as a practical AI application with a clear path toward a retrieval-based study system.

## Overview

This project helps students study from long lecture transcripts by generating:
- summaries,
- key concepts,
- important examples,
- likely exam questions, and
- grounded answers to student questions.

The current version stores transcripts and uses the selected transcript as the knowledge source for note generation and Q&A.

## Why I built this

Lecture transcripts are long, noisy, and difficult to revise from directly. I wanted to build a practical student-facing AI tool that reduces that friction while also serving as a good project for hands-on practice in LLM applications, prompt design, and the foundations of RAG.

## Tech stack

- **Python**
- **Streamlit** for the UI
- **Google Gemini API**
- **Gemini 2.5 Flash-Lite** as the default model
- **python-dotenv** for environment variable management
- **SQLAlchemy + SQLite** for transcript storage

## Why this stack

- **Streamlit** makes it easy to build and test the app quickly.
- **Python** keeps the code simple and works well for AI, NLP, and retrieval tasks.
- **Gemini 2.5 Flash-Lite** was chosen because it is fast, free‑tier‑friendly, and strong enough for the main tasks in this app (transcript summarization and grounded Q&A). It gives good latency and cost for many small calls, while leaving a clear upgrade path to heavier Gemini models if future versions need deeper reasoning or larger context windows.
- **SQLAlchemy + SQLite** gives the project a structured storage layer without adding much setup overhead.

## Current version (v1)

### Features
- Save lecture transcripts in the system.
- Add transcripts by uploading a `.txt` file or pasting transcript text.
- Select a saved transcript from the database.
- Generate structured study notes.
- Extract key concepts and important examples.
- Generate likely exam questions.
- Ask questions about the selected lecture.
- Return answers grounded in the selected transcript.

This version is the **first step toward a retrieval-based study assistant**.
It already:
- uses lecture transcripts as the main knowledge source, and
- generates notes and answers that stay grounded in that transcript.

Right now, the app keeps the pipeline simple by sending the selected transcript directly to the model. This keeps the system easy to understand and gives it a solid base for retrieval improvements in future versions.

## Planned versions

### v2 – Stronger study assistant
- Cleaner UI with separate areas for notes and Q&A.
- Better explanations for questions, written more like a teaching assistant.
- Flashcard generation for memorization and exam prep.
- Basic chunking of long transcripts into smaller sections.
- Simple retrieval over the most relevant chunks inside one transcript.

### v3 – Full RAG foundation
- Preprocessing to remove filler words and clean noisy transcripts.
- Better handling of real, unstructured lecture transcripts.
- Optional audio/video to transcript support.
- Chunk storage for long lectures.
- Vector embeddings for transcript chunks.
- Semantic retrieval over the most relevant chunks instead of sending the full transcript.
- Support for retrieval across multiple lectures.
- A stronger ingestion and retrieval pipeline that moves the project toward a full RAG system.

## Long-term direction

The long-term goal is to grow this into a course-level RAG system:
- transcripts are cleaned and split into chunks,
- chunks are converted into vector embeddings and indexed,
- questions retrieve the most relevant chunks across lectures,
- answers are generated from retrieved context instead of the full transcript,
- flashcards and other study tools are built on top of the same data,
- and eventually the system supports the full flow from lecture audio/video to searchable study material.
