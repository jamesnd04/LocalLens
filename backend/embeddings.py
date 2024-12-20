# external imports
from openai import OpenAI
from pinecone import Pinecone


# internal imports
from models import Place

# system
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY")).Index("places")


def create_embedding(text):
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model="text-embedding-3-large")
        .data[0]
        .embedding
    )


def upsert_embedding(place: Place):
    vectors_tuple = (
        place.name,
        create_embedding(place.editorial_summary),
        place.model_dump(),
    )
    pc.upsert(vectors=[vectors_tuple], namespace="places")


def get_query_embedding(query, k=8):
    query_response = pc.query(queries=[create_embedding(query)], top_k=k).to_dict()
    return query_response
