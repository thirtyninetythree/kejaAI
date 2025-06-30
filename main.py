import asyncio
import json
import time
from typing import List
from evaluator import filter_quality_houses
from dotenv import load_dotenv

from helpers import format_property_data
from navigator import get_all_house_details, search_houses
load_dotenv()

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

async def main():
    """Main function for local execution"""
    
    query = "2 bedroom apartment in Westlands under 50000 KES. Lots of natural light"
    
    # Run the search
    try:
        # Run the search
        # houses = asyncio.run(search_houses(query))
        houses = [
            "https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096488",
            # "https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096542",
            # "https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096557",
            # "https://www.property24.co.ke/2-bedroom-apartment-flat-to-rent-in-westlands-116091129"
        ]

        # house_details = []
        # for house in houses:
        #     details = await get_all_house_details(house, counter)
        #     house_details.append(format_property_data(details))
        
        # save_results(house_details, query, "house_details.json")

        house_details = [{'images': ['https://www.property24.com/Images/Property/116096488/116096488_1_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_2_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_3_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_4_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_5_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_6_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_7_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_8_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_9_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_10_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_11_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_12_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_13_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_14_400x400.jpg'], 
                          'link': 'https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096488', 'description': "Three bedroom not ensuite apartment for rent in Westlands. Though an older development, the apartment is well maintained and sits on a large compound with a garden, ideal as a children's play area. The location is also close to several churches and a mosque, making it convenient for spiritual needs.", 
                          'exact_location': 'Sarit Centre Karuna Rd, Westlands, Nairobi', 
                          'building_amenities': ['gym', 'swimming pool', 'parking', '24hr security']}]


        # # In main() function, after houses = asyncio.run(search_houses(query)):
        quality_houses = filter_quality_houses(house_details, query)
        
        # Save to file
        save_results(quality_houses, query, "evaluated_houses.json")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
     asyncio.run(main()) 