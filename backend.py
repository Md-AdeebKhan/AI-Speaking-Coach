from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class TextInput(BaseModel):
    text: str

@app.post("/coach")
def coach(data: TextInput):

    prompt = f"""
You are an AI English Speaking Coach and Assistant.

STEP 1 — Language Feedback
- Check grammar of the sentence.
- If incorrect: provide corrected sentence + short explanation.
- If correct: write "Sentence is already correct."

STEP 2 — Assistant Response
- Answer the user's question naturally and helpfully.

Respond strictly in this format:

Language Feedback:
Corrected sentence:
Explanation:

Assistant Response:

User input: {data.text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"reply": response.choices[0].message.content}
