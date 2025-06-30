import json
import re

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

# # Example usage with your data
# raw_data = """Successfully extracted all information. 
# Images: [https://www.property24.com/Images/Property/116096488/116096488_1_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_2_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_3_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_4_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_5_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_6_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_7_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_8_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_9_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_10_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_11_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_12_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_13_400x400.jpg, https://www.property24.com/Images/Property/116096488/116096488_14_400x400.jpg]
# Link: https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096488
# Description: Three bedroom not ensuite apartment for rent in Westlands. Though an older development, the apartment is well maintained and sits on a large compound with a garden, ideal as a children's play area. The location is also close to several churches and a mosque, making it convenient for spiritual needs.
# Exact Location: Sarit Centre Karuna Rd, Westlands, Nairobi
# Building Amenities: gym, swimming pool, parking, 24hr security"""

# query = "2 bedroom apartment in Westlands under 50000 KES. Lots of natural light"

# # Format the data
# formatted_data = format_property_data(query, raw_data)

# # Print as JSON
# print(json.dumps(formatted_data, indent=2))
