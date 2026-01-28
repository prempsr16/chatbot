from openai import AzureOpenAI
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os

app = FastAPI()

client = AzureOpenAI(
    api_key=os.getenv("7vyPmoL0ax5yW627gDWLkSN6E3hsQmSOnJrH3VUbwb2JN6Zn6NLCJQQJ99CAAC5RqLJXJ3w3AAAAACOGX4hk"),
    api_version="2024-02-01",
    azure_endpoint="https://test-foundry-surana.openai.azure.com/"
)

DEPLOYMENT = "gpt-4.1"

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(req: ChatRequest):

    def stream():
        response = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": req.question}
            ],
            stream=True
        )

        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return StreamingResponse(stream(), media_type="text/plain")
