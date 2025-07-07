import asyncio
from typing import List
from evaluator import evaluate_house_details
from helpers import format_property_data, save_results
from navigator import search_houses


async def run_property_pipeline(query: str, max_concurrent: int = 5) -> List[dict]:
    """Main pipeline orchestrator"""
    # 1. Search -> URLs
    urls = await search_houses(query)
    print(urls)
    
    # 2. Scrape -> Raw details (concurrent)
    raw_details = await scrape_properties_concurrent(urls, max_concurrent)
    
    # 4. Save & return
    save_results(raw_details, query)
    return raw_details

async def scrape_properties_concurrent(urls: List[str], max_concurrent: int, query: str) -> List[dict]:
    """Scrape multiple properties concurrently with rate limiting"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def scrape_with_limit(url):
        async with semaphore:
            return await scrape_single_property(url, query)
    
    tasks = [scrape_with_limit(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)

async def scrape_single_property(url: str, query: str, max_retries: int = 3) -> dict:
    """Scrape single property with retry logic"""
    for attempt in range(max_retries):
        try:
            await asyncio.sleep(2)  # Rate limiting
            details = await evaluate_house_details(url, query)
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
    urls = await search_houses(query)
    print(urls)
    # results = await scrape_single_property(url)
    # print(f"✅ Found {len(results)} quality properties")

if __name__ == "__main__":
     asyncio.run(main()) 