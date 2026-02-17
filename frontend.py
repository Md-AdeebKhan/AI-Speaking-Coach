import streamlit as st
import requests
import tempfile
import os
import asyncio
from dotenv import load_dotenv
from groq import Groq
import edge_tts
from streamlit_mic_recorder import mic_recorder

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Speaking Coach", layout="wide")

# ---------- EDGE-TTS FUNCTION ----------
async def speak(text, filename):
    communicate = edge_tts.Communicate(
        text,
        voice="en-US-JennyNeural",
        rate="+12%",
        pitch="+2Hz"
    )
    await communicate.save(filename)

# ---------- FIXED HEADER ----------
st.markdown("""
<style>
.fixed-header {
    position: fixed;
    top: 55px;
    left: 0;
    right: 0;
    background: white;
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid #e6e6e6;
    z-index: 9999;
}
.header-title { font-size: 34px; font-weight: 800; }
.header-subtitle { font-size: 13px; color: #777; }
.block-container { padding-top: 170px; }
.chat-separator {
    height: 1px;
    background-color: #e0e0e0;
    margin-top: 12px;
    margin-bottom: 12px;
}
</style>

<div class="fixed-header">
    <div class="header-title">🎙️ AI Speaking Coach</div>
    <div class="header-subtitle">
        Practice speaking English with real-time personalized coaching feedback
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- SESSION MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- DISPLAY CHAT ----------
for role, msg in st.session_state.messages:
    avatar = "🤖" if role == "assistant" else "🙂"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg)
    st.markdown("<div class='chat-separator'></div>", unsafe_allow_html=True)

# ---------- MIC ----------
audio = mic_recorder(start_prompt="🎤", stop_prompt="Stop")

# ---------- CHAT INPUT ----------
user_text = st.chat_input("Type your sentence...")

# ---------- VOICE INPUT ----------
if audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio["bytes"])
        txt = groq_client.audio.transcriptions.create(
            file=open(f.name, "rb"),
            model="whisper-large-v3"
        )
    user_text = txt.text

# ---------- SEND ----------
if user_text:

    st.session_state.messages.append(("user", user_text))
    with st.chat_message("user", avatar="🙂"):
        st.markdown(user_text)

    typing_placeholder = st.empty()
    typing_placeholder.info("🤖 Coach is thinking...")

    response = requests.post(
    "https://ai-speaking-coach-backend.onrender.com/coach",
    json={"text": user_text}
)

    typing_placeholder.empty()

    reply = response.json()["reply"]

    st.session_state.messages.append(("assistant", reply))
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(reply)

    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    asyncio.run(speak(reply, audio_file.name))
    st.audio(audio_file.name)