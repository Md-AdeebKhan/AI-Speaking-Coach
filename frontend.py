import streamlit as st
import requests, tempfile, os
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("AI Speaking Coach")
st.caption("Practice speaking, get grammar feedback, and receive helpful AI responses in real time.")

mode = st.radio("Choose input:", ["Text", "Voice"])
user_text = None

# TEXT
if mode == "Text":
    t = st.text_input("Type your sentence")
    if st.button("Send") and t:
        user_text = t

# VOICE
else:
    audio = mic_recorder(start_prompt="Speak", stop_prompt="Stop")
    if audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio["bytes"])
            txt = groq_client.audio.transcriptions.create(
                file=open(f.name, "rb"),
                model="whisper-large-v3"
            )
        user_text = txt.text
        st.write("You said:", user_text)

# CALL BACKEND
if user_text:
    r = requests.post(
        "https://ai-speaking-coach-85ox.onrender.com/coach",
        json={"text": user_text}
    )
    reply = r.json()["reply"]
    st.write(reply)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        gTTS(reply).save(f.name)
        st.audio(f.name)
