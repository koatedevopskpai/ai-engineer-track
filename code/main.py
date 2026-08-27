# main.py #
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Engineer Hello", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Hello from the AI Engineer Track"}


@app.get("/health")
def health():
    return {"status": "ok"}


class EchoIn(BaseModel):
    text: str
    repeat: int = 1


@app.post("/echo")
def echo(body: EchoIn):
    return {"echo": [body.text] * body.repeat}
