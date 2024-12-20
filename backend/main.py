# built-in
import os
from dotenv import load_dotenv

# external imports
from fastapi import FastAPI
from openai import OpenAI
from pinecone import Pinecone

# internal imports
from models import Place, ProfileParams, Message
from agent import (
    get_list_for_itinerary,
)

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("places")


@app.get("/")
def read_root():
    return {"Hello World"}


@app.post("/itinerary")
def get_itinerary(profile_data: ProfileParams) -> list[Place]:
    places = get_list_for_itinerary(profile_data)
    return places


@app.post("/chat")
def chat_with_agent(message: Message) -> str:
    response = client.chat.completeions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": message.role, "content": message.content},
        ],
        response_format=Message,
    )

    return response.choices[0].message.content
