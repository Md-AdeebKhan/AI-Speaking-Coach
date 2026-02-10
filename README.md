# AI Speaking Coach

An interactive AI-powered speaking coach that helps users improve their English by providing grammar feedback, better sentence suggestions, short explanations, and conversational assistance in real time.

## Features

- Text and Voice Input support
- Automatic Speech-to-Text transcription
- Grammar correction and fluency suggestions
- Short explanation of mistakes
- Natural conversational responses
- Text-to-Speech AI voice response
- Simple web interface built with Streamlit
- FastAPI backend powered by Groq LLM

## Tech Stack

- Frontend: Streamlit
- Backend: FastAPI
- LLM: Groq (LLaMA 3 Instant)
- Speech-to-Text: Groq Whisper
- Text-to-Speech: gTTS
- Python

## Project Structure

backend.py # FastAPI backend (AI logic)
frontend.py # Streamlit frontend interface
requirements.txt
README.md


## How to Run Locally

1. Clone the repository
   git clone <repo-url>
   cd <repo-folder>


2. Create virtual environment and install dependencies


3. Add environment variables
   Create a `.env` file:
   GROQ_API_KEY=your_api_key_here

4. Run the application
   streamlit run frontend.py

   
The backend will start automatically and the app will open in your browser.

## Demo

The application allows students to speak or type sentences, receive grammar feedback, and continue a conversational interaction with the AI coach.


pip freeze > requirements.txt
git add .
git commit -m "AI Speaking Coach submission"
git push

