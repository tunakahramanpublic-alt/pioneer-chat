from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI
import os
import uuid
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://keen-madeleine-db435b.netlify.app"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
WORKFLOW_ID = "wf_69dc2de445a08190adc85f13727d38540280571ebd518534"

@app.get("/")
def home():
    return {
        "status": "ok",
        "version": "upload-nested-v1"
    }

@app.post("/api/chatkit/session")
def create_session():
    try:
        user_id = f"eczane-{uuid.uuid4()}"

        session = client.beta.chatkit.sessions.create(
            user=user_id,
            workflow={"id": WORKFLOW_ID},
            chatkit_configuration={
                "file_upload": {
                    "enabled": True,
                    "max_file_size": 20,
                    "max_files": 3
                }
            }
        )

        return {"client_secret": session.client_secret}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "trace": traceback.format_exc()
            }
        )
