# app.py

import streamlit as st
import whisper
import os
import tempfile
import yt_dlp
import shutil
import time
from transformers import pipeline # For summarization

# --- HELPER FUNCTION ---
# Helper function to format seconds into [HH:MM:SS]
def format_timestamp(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"[{int(h):02d}:{int(m):02d}:{int(s):02d}]"

# --- MODEL LOADING WITH CACHING ---
@st.cache_resource
def load_whisper_model(model_name):
    model = whisper.load_model(model_name)
    return model

# New cached function to load the summarization model
@st.cache_resource
def load_summarizer():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return summarizer

# --- MAIN PROCESSING FUNCTION ---
def process_and_transcribe(file_path, success_message, selected_model, add_timestamps):
    model = load_whisper_model(selected_model)
    st.session_state['transcription_result'] = None
    st.session_state['file_ready_for_download'] = False
    
    spinner_message = f"Transcribing using the '{selected_model}' model... Please wait."
    with st.spinner(spinner_message):
        try:
            result = model.transcribe(file_path, fp16=False)
            st.success(success_message)
            
            # Create timestamped or plain text based on user choice
            if add_timestamps:
                transcript_text = ""
                for segment in result['segments']:
                    start_time = format_timestamp(segment['start'])
                    text = segment['text']
                    transcript_text += f"{start_time} {text.strip()}\n"
                st.session_state['transcription_result'] = transcript_text.strip()
            else:
                st.session_state['transcription_result'] = result["text"]

            st.session_state['file_ready_for_download'] = True
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Always delete the temporary file/folder
            if os.path.exists(file_path):
                dir_path = os.path.dirname(file_path)
                if "yt_dlp_temp" in dir_path:
                    shutil.rmtree(dir_path, ignore_errors=True)
                else:
                    os.remove(file_path)

# --- UI SETTINGS ---
st.set_page_config(page_title="Transcribe & Summarize", page_icon="🎙️", layout="wide")
st.title("🎙️ Transcribe & Summarize Audio/Video")
st.info("This app transcribes and summarizes speech from your uploaded files or a YouTube link.")
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    model_choice = st.selectbox(
        "Select Whisper Model",
        ("tiny", "base", "small", "medium"),
        index=1,
        help="Larger models offer higher accuracy but are slower. 'tiny' is the fastest."
    )
    
    st.divider()
    
    add_timestamps = st.checkbox(
        "Add Timestamps to Transcript",
        value=True,
        help="Display the start time for each transcribed segment."
    )

    st.divider()
    st.markdown("Developed by: Techmaster")
    st.markdown("Powered by [OpenAI Whisper](https://openai.com/research/whisper) & [Streamlit](https://streamlit.io)")

# --- USER INPUT OPTIONS (MAIN PAGE) ---
input_method = st.radio(
    "Please select an input method:",
    ('Upload a File', 'Enter a YouTube URL'),
    key="input_method_radio",
    horizontal=True
)

st.divider()

# --- MAIN FUNCTIONALITY ---
if input_method == 'Upload a File':
    uploaded_file = st.file_uploader(
        "Upload an audio or video file",
        type=['mp3', 'mp4', 'wav', 'm4a', 'avi', 'mov']
    )
    
    if uploaded_file is not None:
        if st.button("Transcribe File ✨", type="primary"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_file_path = tmp_file.name
            
            process_and_transcribe(temp_file_path, f"Transcription complete for '{uploaded_file.name}':", model_choice, add_timestamps)

elif input_method == 'Enter a YouTube URL':
    url = st.text_input(
        "Paste the YouTube video link here:",
        placeholder="https://www.youtube.com/watch?v=..."
    )
    
    if url:
        if st.button("Transcribe from URL ✨", type="primary"):
            temp_dir = tempfile.mkdtemp(prefix="yt_dlp_temp_")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                # Add a User-Agent header to mimic a browser request
                'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    downloaded_file_name = ydl.prepare_filename(info_dict).replace(info_dict['ext'], 'mp3')
                
                process_and_transcribe(downloaded_file_name, f"Transcription complete for '{info_dict['title']}':", model_choice, add_timestamps)
            except Exception as e:
                st.error(f"An error occurred while downloading the video: {e}")
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)

# --- RESULT DISPLAY AND DOWNLOAD / SUMMARIZATION ---
if 'transcription_result' in st.session_state and st.session_state['transcription_result'] is not None:
    st.divider()
    st.subheader("📄 Transcription Result")
    
    transcript_text = st.session_state['
