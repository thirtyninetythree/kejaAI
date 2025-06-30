Problem
House hunting is hard. Too many options to sift through. 
Takes too much time
Stressful because you're making an important decision with little information
Apartment hunting in Nairobi is fragmented across multiple platforms

Features
Computer Use agent that searches for houses for you in a specified area, price, house size and tries to match you general interior design directions. It uses natural language prompts: Natural language apartment search ("2 bedroom in Westlands under 50k") or Find me a quiet 2BR near a good primary school under 45k 30 min commute

HouseListObject {thumbnail: link to thumbnail image, link: link to to the property detail page} 
HouseDetailObject { link: link to the property detail page, images: [list of listing images], description: text description of property the property including price and exact location(if exists)

3 STEPS
Model 1 navigates to correct websites, searches and get the results. Passes onto model 2
<!-- Model 2 evaluates based on the thumbnail - this is to remove listings that are too low quality. Passes back a vetted list to model 1
Web scrape to get all images of the house from the carousel.  -->
Model 1 receives a list of house detail links. Navigates to them and grabs all the images and other extra metadata - exact location, other amenities within the building. THis is it's own step because it can be pararrelized. 
Model 2 now has a evaluates look at the house images, looks at the neighbourhood amenities using mcp. 

2 models: one to navigate and another to evaluate a listing for image or vibe match, evaluate the location for amenities and life index, commute distance
Model 1: Navigator
Uses search and user query location, bedrooms, and price to set the right filters on the website. 
It navigates the website(scrolls) and gathers all the results from the list page into this format: 
{thumbnail: link to thumbnail image, link: link to to the property detail page} - these are to be passed on to the evaluator model

Model 2: Evaluator
Receives a house json object, from the thumbnail it uses a club embedding model to eliminate houses which are too low quality.
It navigates the available images on the house detail page, eliminating or accepting using the clip embedding
Has access to a clip embedding model to evaluate the images of a place to match the vibe
Has access to maps MCP server to look for nearby amenities or other useful institutions like police station or hospital
It uses to MCP to give you a neighbourhood context. Places to go visit, gyms, malls, shops etc, searches for more info about the general area etc

Cost
Expect it to get cheaper as we 'index' more properties

Maps mcp server to start with where you want to live, find all houses there, get their images, match and compare to find your favourite
We could have two image evaluator models: CLIP(image to text matching from user prompts), DINOv2(image similairty after user uploads image)
