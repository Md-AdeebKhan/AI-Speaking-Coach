import streamlit as st
import requests, subprocess, sys, time, socket, tempfile, os
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# start backend if not running
if socket.socket().connect_ex(("127.0.0.1", 8000)) != 0:
    subprocess.Popen([sys.executable, "-m", "uvicorn", "backend:app"])
    time.sleep(2)

st.title("AI Speaking Coach")
st.caption("Practice speaking, get grammar feedback, and receive helpful AI responses in real time.")
mode = st.radio("Choose input:", ["Text", "Voice"])

user_text = None

if mode == "Text":
    t = st.text_input("Type your sentence")
    if st.button("Send") and t:
        user_text = t

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

if user_text:
    r = requests.post("http://127.0.0.1:8000/coach", json={"text": user_text})
    reply = r.json()["reply"]
    st.write(reply)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        gTTS(reply).save(f.name)
        st.audio(f.name)
