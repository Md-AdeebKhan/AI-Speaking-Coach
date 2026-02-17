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
- Text-to-Speech: gTTS / Edge-TTS
- Python

## Project Structure
backend.py — FastAPI backend  
frontend.py — Streamlit frontend  
requirements.txt  
README.md  

## How to Run Locally
1. Clone repository  
   git clone <repo-url>  
   cd <repo-folder>

2. Install dependencies  
   pip install -r requirements.txt

3. Add environment variables  
   Create `.env` file:  
   GROQ_API_KEY=your_api_key_here

4. Run backend  
   uvicorn backend:app --reload

5. Run frontend  
   streamlit run frontend.py

## Deployment
Backend deployed on Render (FastAPI)  
Frontend deployed on Streamlit Cloud  

## Demo
Users can speak or type sentences, receive grammar feedback, improved sentence suggestions, and continue a conversational interaction with the AI speaking coach.