Whisper Transcriber & Summarizer
An intelligent web application built with Streamlit that leverages OpenAI's Whisper for highly accurate audio/video transcription and Hugging Face Transformers for concise text summarization.

🖼️ Application Preview
(Note: Please replace app_screenshot.png with an actual screenshot of your running application for the best result.)

✨ Features
Accurate Transcription: Utilizes various sizes of OpenAI's Whisper model (tiny, base, small, medium) to convert speech to text.

Multiple Input Methods:

File Upload: Transcribe from various audio and video file formats (.mp3, .mp4, .wav, .m4a, etc.).

YouTube URL: Directly transcribe audio from any YouTube video link.

AI-Powered Summarization: Generate a concise summary of the transcribed text using a pre-trained model from Hugging Face (facebook/bart-large-cnn).

Timestamp Generation: Optionally add timestamps to the transcript to easily sync text with the source audio/video.

Customizable Models: Choose the Whisper model that best fits your needs, balancing speed and accuracy.

Downloadable Transcripts: Download the final transcript as a .txt file for offline use.

Interactive UI: A clean, user-friendly, and responsive interface built with Streamlit.

🚀 Live Demo
(Note: After deploying your app on Streamlit Community Cloud, paste the public URL here.)

➡️ View Live Demo

🛠️ Tech Stack
Python: Core programming language.

Streamlit: For building the interactive web user interface.

OpenAI Whisper: For the core speech-to-text transcription.

Hugging Face Transformers: For the text summarization pipeline.

yt-dlp: For downloading audio from YouTube links.

ffmpeg: A critical system dependency for processing audio and video files.

⚙️ Setup and Local Installation
Follow these steps to run the application on your local machine.

1. Prerequisites
Python 3.9 or higher

FFmpeg: This is a system-level dependency and must be installed.

On macOS (using Homebrew):

Bash

brew install ffmpeg
On Debian/Ubuntu:

Bash

sudo apt update && sudo apt install ffmpeg
On Windows:

Download a static build from the FFmpeg official website.

Extract the archive.

Add the path to the bin directory (e.g., C:\ffmpeg\bin) to your system's Path environment variable.

2. Clone the Repository
Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
3. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

Bash

python -m venv venv
Activate the environment:

On macOS/Linux:

Bash

source venv/bin/activate
On Windows:

Bash

.\venv\Scripts\Activate
4. Install Dependencies
Install all the required Python packages from the requirements.txt file.

Bash

pip install -r requirements.txt
5. Run the Application
Launch the Streamlit app with the following command:

Bash

streamlit run app.py
The application should now be open and running in your default web browser!

usage
Select an Input Method: Choose between "Upload a File" or "Enter a YouTube URL".

Configure Settings (Sidebar):

Select a Whisper Model: Choose a model based on your desired balance of speed and accuracy.

Add Timestamps: Check the box if you want timestamps included in the final transcript.

Provide Input: Upload a file or paste a YouTube URL.

Transcribe: Click the "Transcribe" button. The process may take some time depending on the file size and the selected model. The first run for any model will be slower as the model needs to be downloaded.

Review and Use Results:

The transcript will appear in the text area.

Click "Download Transcript" to save it as a text file.

Click "Generate Summary" to get an AI-powered summary of the content.

☁️ Deployment
This application is ready for deployment on Streamlit Community Cloud. To ensure a successful deployment, make sure your GitHub repository contains the following three files:

app.py: The main application script.

requirements.txt: The list of Python dependencies.

packages.txt: A file containing the single word ffmpeg to instruct Streamlit Cloud to install the system dependency.

📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.

🙏 Acknowledgments
OpenAI for the powerful Whisper model.

Hugging Face for the easy-to-use Transformers library.

Streamlit for making web app development in Python so enjoyable.