import json
import re
from typing import List

def format_property_data(raw_property_data: str) -> dict:
    """
    Format raw property data string into structured JSON object
    """
    # Parse the raw string to extract structured data
    images = []
    link = ""
    description = ""
    location = ""
    amenities = []
    
    # Extract images using regex
    images_match = re.search(r'Images: \[(.*?)\]', raw_property_data)
    if images_match:
        images_str = images_match.group(1)
        # Split by comma and clean up URLs
        images = [url.strip() for url in images_str.split(',')]
    
    # Extract link
    link_match = re.search(r'Link: (https://[^\n]+)', raw_property_data)
    if link_match:
        link = link_match.group(1).strip()
    
    # Extract description
    desc_match = re.search(r'Description: (.*?)\nExact Location:', raw_property_data, re.DOTALL)
    if desc_match:
        description = desc_match.group(1).strip()
    
    # Extract location
    location_match = re.search(r'Exact Location: (.*?)\nBuilding Amenities:', raw_property_data)
    if location_match:
        location = location_match.group(1).strip()
    
    # Extract amenities
    amenities_match = re.search(r'Building Amenities: (.*?)$', raw_property_data)
    if amenities_match:
        amenities_str = amenities_match.group(1).strip()
        # Split by comma and clean up
        amenities = [amenity.strip() for amenity in amenities_str.split(',')]
    
    # Create structured property object
    property_obj = {
        "images": images,
        "link": link,
        "description": description,
        "exact_location": location,
        "building_amenities": amenities
    }
    
    return property_obj

def save_results(houses: List[str], query: str, filename: str = "search_results.json"):
    """Save results to JSON file"""
    results = {
        "query": query,
        "total_properties": len(houses),
        "properties": [str(house) for house in houses]
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Results saved to {filename}")
