import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the URL from environment variable, fallback to Sello
URL = os.getenv("LOUNAS_SOURCE_URL", "https://lounaat.info/kauppakeskus-sello-espoo")



def fetch_sello_lunch_menus() -> List[Dict[str, Any]]:
    """
    Fetches the Sello shopping mall lunch menus for today.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # We find the main menu container elements
    menu_containers = soup.select(".menu.item")
    
    restaurants_data = []
    
    for container in menu_containers:
        # Extract restaurant name
        name_tag = container.select_one("h3 a") or container.select_one("h3")
        if not name_tag:
            continue
        restaurant_name = name_tag.text.strip()
        
        # Extract distance/address metadata if available
        dist_tag = container.select_one(".item-footer .dist")
        distance = dist_tag.text.strip() if dist_tag else None
        address = dist_tag.get("title", "").strip() if dist_tag else None
        
        # Extract lunch hours if available
        hours_tag = container.select_one(".item-header .lunch")
        lunch_hours = hours_tag.text.strip() if hours_tag else None
        
        # Extract menu items
        dishes = []
        
        # Check if menu list is empty/missing (like Compass Group links)
        missing_link = container.select_one(".item-body a.missing")
        if missing_link:
            dishes.append({
                "name": missing_link.text.strip(),
                "price": None,
                "info": None,
                "link": missing_link.get("href")
            })
        else:
            menu_items = container.select(".item-body ul li")
            for item in menu_items:
                # Price
                price_tag = item.select_one(".price")
                price = price_tag.text.strip() if price_tag else None
                
                # Dish name
                dish_tag = item.select_one(".dish")
                if dish_tag:
                    # Clean up dish name by stripping trailing diet links text if BeautifulSoup joins them
                    # (BeautifulSoup text might join 'Dish Name' and 'l g' diets)
                    # We can clone and decompose anchor tags inside dish_tag to get clean name
                    dish_clone = BeautifulSoup(str(dish_tag), "html.parser")
                    for a_tag in dish_clone.find_all("a"):
                        a_tag.decompose()
                    dish_name = dish_clone.text.strip()
                else:
                    dish_name = item.text.strip()
                
                # Info/Description
                info_tag = item.select_one(".info")
                info = info_tag.text.strip() if info_tag else None
                
                dishes.append({
                    "name": dish_name,
                    "price": price,
                    "info": info
                })
        
        restaurants_data.append({
            "restaurant": restaurant_name,
            "lunch_hours": lunch_hours,
            "distance": distance,
            "address": address,
            "menu": dishes
        })
        
    return restaurants_data

if __name__ == "__main__":
    import json
    try:
        data = fetch_sello_lunch_menus()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error fetching menus: {e}")
