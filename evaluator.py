
import requests
from PIL import Image
import base64
import io
import time

from langchain_google_genai import ChatGoogleGenerativeAI

from settings import EVALUATOR_MODEL

llm = ChatGoogleGenerativeAI(model=EVALUATOR_MODEL)
    
def evaluate_image(image_url: str, query: str) -> bool:
    """Evaluate image based on user preference in query and filter out low quality listings"""
    print(f"image_url = {image_url}")
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(io.BytesIO(response.content))
        
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        prompt = f"""Evaluate this property image. 
                    Return only 'KEEP' or 'REJECT' and the reason why to keep it
                    KEEP if: clear, well-lit, shows actual property and matches user query somewhat {query}
                    REJECT if: blurry, dark, placeholder, or very low quality

                    Image: data:image/jpeg;base64,{img_str}
                    """
        
        result = llm.invoke(prompt).content.strip()
        return "KEEP" in result.upper()
        
    except Exception as e:
        print(f"ERROR EVALUATING IMAGE: {e}")
        return True
        
def filter_quality_houses(houses: list, query: str) -> list:
    filtered = []

    for i, house in enumerate(houses):
        if house.get("images") and house["images"]: 
            for i in range(5):
                result = evaluate_image(house["images"][i], query) 
                filtered.append(house) if result else None
                print(f"{i+1}/{len(houses)} processed. Result: {result}")
            
                # For Gemini rate limits, about 30 reqs/min
                if i < len(houses) - 1:
                    time.sleep(3)
    return filtered
    
    