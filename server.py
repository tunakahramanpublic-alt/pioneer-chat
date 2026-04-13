from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import uuid

app = FastAPI()

origins = [
    "https://keen-madeleine-db435b.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
WORKFLOW_ID = "wf_69dc2de445a08190adc85f13727d38540280571ebd518534"

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/api/chatkit/session")
def create_session():
    user_id = f"eczane-{uuid.uuid4()}"

    session = client.beta.chatkit.sessions.create(
        user=user_id,
        workflow={"id": WORKFLOW_ID},
        file_upload={
            "enabled": True,
            "max_file_size": 20,
            "max_files": 3
        }
    )

    return {"client_secret": session.client_secret}
