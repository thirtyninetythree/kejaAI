import asyncio
from typing import List
from evaluator import filter_quality_houses
from helpers import format_property_data, save_results
from navigator import get_all_house_details, search_houses


async def run_property_pipeline(query: str, max_concurrent: int = 5) -> List[dict]:
    """Main pipeline orchestrator"""
    # 1. Search -> URLs
    urls = await search_houses(query)
    
    # 2. Scrape -> Raw details (concurrent)
    raw_details = await scrape_properties_concurrent(urls, max_concurrent)
    
    # 3. Filter -> Quality properties
    filtered = filter_quality_houses(raw_details, query)
    
    # 4. Save & return
    save_results(filtered, query)
    return filtered

async def scrape_properties_concurrent(urls: List[str], max_concurrent: int) -> List[dict]:
    """Scrape multiple properties concurrently with rate limiting"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def scrape_with_limit(url):
        async with semaphore:
            return await scrape_single_property(url)
    
    tasks = [scrape_with_limit(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)

async def scrape_single_property(url: str, max_retries: int = 3) -> dict:
    """Scrape single property with retry logic"""
    for attempt in range(max_retries):
        try:
            await asyncio.sleep(2)  # Rate limiting
            details = await get_all_house_details(url)
            return format_property_data(details)
        except Exception as e:
            if attempt == max_retries - 1:
                return {"error": str(e), "url": url}
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

def filter_valid_properties(properties: List[dict]) -> List[dict]:
    """Remove failed scrapes before quality filtering"""
    return [p for p in properties if "error" not in p]

async def main():
    query = "2 bedroom apartment in Westlands under 50000 KES lots of natural light"
    # results = await run_property_pipeline(query)
    url =  "https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096488",
    results = await scrape_single_property(url)
    print(f"✅ Found {len(results)} quality properties")



# async def main():
#     """Main function for local execution"""
    
#     query = "2 bedroom apartment in Westlands under 50000 KES. Lots of natural light"
    
#     # Run the search
#     try:
#         # Run the search
#         # urls = asyncio.run(search_houses(query))
#         houses = [
#             "https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096488",
#             # "https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096542",
#             # "https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096557",
#             # "https://www.property24.co.ke/2-bedroom-apartment-flat-to-rent-in-westlands-116091129"
#         ]

#         house_details = []
#         for house in houses:
#             details = await get_all_house_details(house)
#             house_details.append(format_property_data(details))
        
#         save_results(house_details, query, "house_details.json")

#         # house_details = [{'images': ['https://www.property24.com/Images/Property/116096488/116096488_1_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_2_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_3_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_4_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_5_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_6_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_7_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_8_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_9_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_10_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_11_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_12_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_13_400x400.jpg', 'https://www.property24.com/Images/Property/116096488/116096488_14_400x400.jpg'], 
#         #                   'link': 'https://www.property24.co.ke/3-bedroom-apartment-flat-to-rent-in-westlands-116096488', 'description': "Three bedroom not ensuite apartment for rent in Westlands. Though an older development, the apartment is well maintained and sits on a large compound with a garden, ideal as a children's play area. The location is also close to several churches and a mosque, making it convenient for spiritual needs.", 
#         #                   'exact_location': 'Sarit Centre Karuna Rd, Westlands, Nairobi', 
#         #                   'building_amenities': ['gym', 'swimming pool', 'parking', '24hr security']}]


#         # # # In main() function, after houses = asyncio.run(search_houses(query)):
#         # quality_houses = filter_quality_houses(house_details, query)
        
#         # # Save to file
#         # save_results(quality_houses, query, "evaluated_houses.json")
        
#     except Exception as e:
#         print(f"❌ Error: {e}")

if __name__ == "__main__":
     asyncio.run(main()) 