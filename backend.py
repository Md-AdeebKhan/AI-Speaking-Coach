from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_memory = []

class TextInput(BaseModel):
    text: str

@app.post("/coach")
def coach(data: TextInput):

    conversation_memory.append({"role":"user","content":data.text})

    system_prompt = """
You are an English Speaking Coach.

For every user message:
1. Provide grammar correction
2. Suggest a better sentence
3. Give a short simple explanation
4. Continue conversation naturally
"""

    messages = [{"role":"system","content":system_prompt}] + conversation_memory

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    reply = response.choices[0].message.content

    conversation_memory.append({"role":"assistant","content":reply})

    return {"reply": reply}