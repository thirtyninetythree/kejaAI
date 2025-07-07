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
        Find rental properties for: "{query}"

        SEARCH EXECUTION:
        1. Navigate to https://www.property24.co.ke/apartments-flats-to-rent
        2. Parse query and fill filters:
        - Location: Extract area/neighborhood from query
        - Property type: "Apartment/Flat" 
        - Price: Set max price filter from query (e.g. "under 50000" → max 50000)
        - Bedrooms: Extract number + set filter (e.g. "2 bedroom" → 2+)
        3. Submit search and wait for results

        EXTRACTION:
        - From search results page, extract ALL property detail page URLs
        - Get complete URLs (https://www.property24.co.ke/...)
        - Skip ads, featured listings, or non-property links

        OUTPUT FORMAT:
        Return ONLY this JSON array:
        [
        {{"link": "https://www.property24.co.ke/property-url-1"}},
        {{"link": "https://www.property24.co.ke/property-url-2"}}
        ]
        """
    
    # Create agent with proper browser config
    agent = Agent(
        task=prompt,
        llm=llm,
    )
    
    print(f"🔍 Searching: {query}")
    result = await agent.run()
    return result.final_result()
