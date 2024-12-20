# external imports
from openai import OpenAI
import requests
import time


# internal imports
from models import (
    ExpandEditorialInputParams,
    Role,
    Place,
    ProfileParams,
)
from embeddings import upsert_embedding, get_query_embedding

# system
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
perplexity = OpenAI(
    api_key=os.getenv("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai"
)
sample = "I live in the United States and I love to travel. I am a software engineer and I enjoy hiking and reading books. I love to be outside and enjoy the Earth, I want to go somewhere I can experience nature."
location = "New York"


def evaluate_interests_by_profile(
    description: str,
) -> None:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": Role.SYSTEM,
                "content": "You are a helpful travel advisor called LocalLens. You are helping users find places personalized places to visit based on their interests.",
            },
            {
                "role": Role.USER,
                "content": "Describe some keywords of potential and current interests based on the description, for example if the description says they like spicy food, include spicier cuisines in the response like hispanic food.",
            },
            {
                "role": Role.USER,
                "content": "Restrict outputs to just the keywoards and a couple of adjectives like 'spicy foods' or 'interactive enviornment', and restrict the output to 1 interest, not compounded. Here is the description:"
                + description,
            },
        ],
    )
    return response.choices[0].message.content


def get_places_by_interests(interests_with_location: str) -> dict:
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={interests_with_location}&key={os.getenv("GOOGLE_PLACES_API_KEY")}"
    payload = {}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def get_places_from_profile(profile: ProfileParams) -> dict:
    print("Profile Description: " + profile.description)
    evaluated_interests = evaluate_interests_by_profile(description=profile.description)
    interests_with_location = evaluated_interests + " in " + profile.location
    print("\nInterests with location: " + interests_with_location)
    return get_places_by_interests(interests_with_location=interests_with_location)


def get_recommendations_from_places(places_dict: dict) -> dict:
    names = {}
    for place in places_dict["results"]:
        names[place["name"]] = place["place_id"]
    return names


def expand_editorial_from_gpt(input: ExpandEditorialInputParams) -> str:
    response = perplexity.chat.completions.create(
        model="llama-3.1-sonar-small-128k-chat",
        messages=[
            {"role": Role.SYSTEM, "content": "You are a helpful travel advisor."},
            {
                "role": Role.USER,
                "content": "Provide more information about the place given, and make sure it relates to the editorial summary, and ONLY return five sentences of the description as the output. Here is the place: "
                "place: "
                + input.place_name
                + " . Here is the editorial summary: "
                + input.editorial_summary,
            },
        ],
    )
    return response.choices[0].message.content


def get_editorial_from_gpt(place_name: str) -> str:
    response = perplexity.chat.completions.create(
        model="llama-3.1-sonar-small-128k-chat",
        messages=[
            {"role": Role.SYSTEM, "content": "You are a helpful travel advisor."},
            {
                "role": Role.USER,
                "content": "Provide more information about the place given, and create an editorial summary, and ONLY return five sentences of the description as the output. Here is the place: "
                "place: " + place_name,
            },
        ],
    )
    return response.choices[0].message.content


def get_places_list_from_recommendations(places_recommendations: dict) -> list[Place]:
    time1 = time.time()
    places = []
    for name, place_id in places_recommendations.items():
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_address,types,photos,rating,editorial_summary&key={os.getenv('GOOGLE_PLACES_API_KEY')}"
        payload = {}
        headers = {"Accept": "application/json"}
        response = requests.request("GET", url, headers=headers, data=payload).json()
        address = response["result"]["formatted_address"]
        types = response["result"]["types"]
        rating = response["result"]["rating"]
        if "editorial_summary" in response["result"].keys():
            overview = response["result"]["editorial_summary"]["overview"]
            editorial_summary = expand_editorial_from_gpt(
                input=ExpandEditorialInputParams(
                    place_name=name, editorial_summary=overview
                )
            )
        else:
            editorial_summary = get_editorial_from_gpt(place_name=name)

        current_place = Place(
            name=name,
            address=address,
            types=types,
            rating=rating,
            editorial_summary=editorial_summary,
        )
        places.append(current_place)
    time2 = time.time()
    print("Time to get places: " + str(time2 - time1))
    return places


def upsert_places(places: list[Place]) -> None:
    for place in places:
        upsert_embedding(Place(**place))


def find_places_by_query(query: str) -> list[Place]:
    resulting_places = []
    query_response = get_query_embedding(query)
    for key, value in query_response.items():
        place = Place(
            name=key,
            address=value["address"],
            types=value["types"],
            rating=value["rating"],
            editorial_summary=value["editorial_summary"],
        )
        resulting_places.append(place)

    return resulting_places


def get_list_for_itinerary(profile_data: ProfileParams) -> list[Place]:
    places_dict = get_places_from_profile(profile=profile_data)
    recommendations = get_recommendations_from_places(places_dict=places_dict)
    places = get_places_list_from_recommendations(
        places_recommendations=recommendations
    )
    # upsert_places(places=places)
    return places
