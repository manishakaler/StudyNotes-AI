import os
from pathlib import Path
import streamlit as st
from db import init_db

from utils import(
    get_all_transcripts,
    get_transcript_by_id,
    generate_notes,
    save_transcript,
    answer_question
)


st.set_page_config(page_title="Lecuture Notes AI Assistant", layout="wide")



init_db()

# Session state
defaults = {
    "notes": "",
    "answer": "",
    "selected_transcript_id": None,
    "transcript_text": "",
    "main_transcript_text": "",
    "transcript_title": "",
    "title_input": "",
    "text_disabled": False,
    "question": "",
    "clear_requested": False,
}

for key,value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def clear_transcript_state():
    st.session_state.selected_transcript_id = None
    st.session_state.transcript_text = ""
    st.session_state.main_transcript_text = ""
    st.session_state.transcript_title = ""
    st.session_state.text_disabled = False
    st.session_state.notes = ""
    st.session_state.answer = ""
    st.session_state.question = ""
    st.session_state.clear_requested = True

if st.session_state.clear_requested:
    st.session_state.title_input = ""
    st.session_state.clear_requested = False

st.title("Lecuture Notes AI Assistant")

upload_col, title_col, save_col = st.columns([2,2,1])


with upload_col:
    uploaded_file = st.file_uploader("Upload transcript (.txt)", type=["txt"])

    if uploaded_file is not None:
        uploaded_text = uploaded_file.getvalue().decode("utf-8")
        default_title = os.path.splitext(uploaded_file.name)[0]
        st.session_state.transcript_text = uploaded_text
        st.session_state.main_transcript_text = uploaded_text
        st.session_state.transcript_title = default_title
        st.session_state.title_input = default_title
        st.session_state.text_disabled = False
        st.session_state.selected_transcript_id = None
        st.session_state.notes = ""
        st.session_state.answer = ""
    

# saved transcripts

transcripts = get_all_transcripts()
transcript_options = ["None"] + [
    f"{t.id} - {t.title}" for t in transcripts
]

selected_label = st.selectbox("Select saved transcript", transcript_options)

if selected_label != "None":
    selected_id = int(selected_label.split(" - ")[0])

    if selected_id != st.session_state.selected_transcript_id:
        transcript = get_transcript_by_id(selected_id)
        st.session_state.selected_transcript_id = transcript.id
        st.session_state.transcript_text = transcript.content
        st.session_state.main_transcript_text = transcript.content
        st.session_state.transcript_title = transcript.title
        # st.session_state.title_input = transcript.title
        st.session_state.text_disabled = True
        st.session_state.notes = ""
        st.session_state.answer = ""
else:
    if st.session_state.selected_transcript_id is not None and st.session_state.text_disabled:
        # clear_transcript_state()
        st.session_state.selected_transcript_id = None
        st.session_state.text_disabled = False

with title_col:
    title_input = st.text_input(
        "Transcript title",
        key="title_input"
        )
    
with save_col:
    st.write("")  # spacer
    st.write("")  
    if st.button("Save Transcript", use_container_width=True):
        if not title_input.strip():
            st.error("Please enter a title.")
        elif not st.session_state.transcript_text.strip():
            st.error("No transcript content to save")
        else:
            transcript, action = save_transcript(
                title_input.strip(),
                st.session_state.transcript_text
            )
            st.session_state.selected_transcript_id = transcript.id
            st.session_state.transcript_title = transcript.title
            st.session_state.text_disabled = True

            if action == "created":
                st.success(f"Saved transcript: {transcript.title}")
            else:
                st.success(f"Updated transcript: {transcript.title}")


# row 3 : trancript box

st.text_area(
    "Transcript",
    height=320,
    placeholder="Paste your transcript here",
    disabled=st.session_state.text_disabled,
    key="main_transcript_text"
)

# keep session state in sync when editable 
if not st.session_state.text_disabled:
    st.session_state.transcipt_text = st.session_state.main_transcript_text

# Row 4 : bottom right buttons

left_spacer, clear_col, generate_col = st.columns([6,1,1.4])

with clear_col:
    if st.button("Clear", type="secondary", use_container_width=True):
        clear_transcript_state()
        st.rerun()

with generate_col:
    if st.button("Generate Notes", use_container_width=True):
        if not st.session_state.transcript_text.strip():
            st.error("Pleasre select, upload, or paste a transcript first")
        else:
            with st.spinner("Generating notes........"):
                st.session_state.notes = generate_notes(st.session_state.transcript_text)

# Output tabs

tab1, tab2 = st.tabs(["Notes", "Ask Questions"])


with tab1:
    
    if st.session_state.notes:
        st.markdown(st.session_state.notes)
    else:
        st.info("Generated notes will appear here.")

with tab2:
    question = st.text_input("Do you have any questions about this lecture?")

    if question != st.session_state.question:
        st.session_state.answer = ""
        st.session_state.question = question
    
    if st.button("Ask"):
        if not st.session_state.transcript_text.strip():
            st.error("Please select, upload or paste a transcript first.")
        elif not question.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Generating answer...."):
                st.session_state.answer= answer_question(st.session_state.transcript_text, question)

    if st.session_state.get("answer"):
        st.subheader("Answer")
        st.write(st.session_state.answer)


