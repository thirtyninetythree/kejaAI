
from browser_use import Agent
import requests
from PIL import Image
import base64
import io
import time

from langchain_google_genai import ChatGoogleGenerativeAI

from settings import EVALUATOR_MODEL

llm = ChatGoogleGenerativeAI(model=EVALUATOR_MODEL)


async def evaluate_house_details(link: str, query: str) -> dict:
    prompt = f"""
        `Navigate to {link} and evaluate against query: "{query}"

        EVALUATION PROCESS:
        - Scroll through all property images (galleries, carousels, lazy-loaded)
        - Analyze image quality: lighting, clarity, completeness of property showcase
        - Extract description, exact street location, building amenities
        - Score how well property matches user requirements

        SCORING SYSTEM (1-10):
        - Query match (bedrooms, location, price, features): 40%
        - Image quality (lighting, clarity, room coverage): 30%
        - Amenities relevance: 20%
        - Location accuracy: 10%

        Return JSON:
        {{
        "link": "{link}",
        "description": "Full property description",
        "exact_location": "Street/Road name with area",
        "building_amenities": ["gym", "parking", "security"],
        "evaluation_score": 8.5,
        "evaluation_reason": "3BR matches query, excellent natural light in photos, prime Westlands location"
        }}
        """
    agent = Agent(
        task=prompt,
        llm=llm,
    )

    print(f"🔍 Getting images from: {link}")
    history = await agent.run()
    return history.final_result()

