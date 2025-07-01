import asyncio
import json
from typing import List
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from settings import NAVIGATOR_MODEL

# Initialize the model
llm = ChatGoogleGenerativeAI(model=NAVIGATOR_MODEL)

load_dotenv()
async def search_houses(query: str) -> List[str]:
    """Search for houses based on natural language query"""

    prompt = f"""
        Your goal is to find rental properties based on the user's query: "{query}"

        STEP 1 - SEARCH SETUP:
        1. Go to https://www.property24.co.ke/apartments-flats-to-rent
        2. Use the location search box to enter location from user query
        3. Set property type to "Apartment/Flat" 
        4. Set price filter to maximum price from user query
        5. Set bedrooms filter based on user query e.g 2+
        6. Click search/filter button

        STEP 2 - EXTRACT PROPERTY DATA:
        1. After search results load, extract ONLY:
        - Link to property detail page (full URL)
        2. Return as JSON array: [{{"link": "url"}}] 

        CRITICAL: Your final response should be ONLY the JSON array, nothing else.
        """
    
    # Create agent with proper browser config
    agent = Agent(
        task=prompt,
        llm=llm,
    )
    
    print(f"🔍 Searching: {query}")
    result = await agent.run()
    return result

async def get_all_house_details(link: str) -> dict:
    prompt = f"""
        Navigate to this property listing: {link}
    
        STEP 1 - IMAGE EXTRACTION:
        - Look for image galleries, carousels, or photo sections
        - Extract ALL images from these sections and ONLY these sections
        - The images must be large and show the listing property and ONLY images of the property
        - Right click on the image and select copy link
        - Ensure URLs are complete (start with http/https)
        - ONLY include property photos, exclude logos/ads/avatars
        
        STEP 2 - DATA EXTRACTION:
        - Description: Look for property description, details, or summary sections
        - Location: Find street address, road name, area details (not just city)
        - Amenities: Look for building features, facilities, or amenities lists


        Return ONLY this JSON format:
        {{
            "images": ["https://image1.jpg", "https://image2.jpg"],
            "link": "{link}",
            "description": "Full property description text here",
            "exact_location": "Road/Avenue/Street name where building is located",
            "building_amenities": ["gym", "swimming pool", "parking", "24hr security", etc]
        }}
        """
 
    agent = Agent(
        task=prompt,
        llm=llm,
    )

    print(f"🔍 Getting images from: {link}")
    history = await agent.run()
    return history.final_result()
