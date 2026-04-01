import requests
import json
import os

def get_churches(country="Russia"):
    overpass_url = "https://overpass-api.de"
    query = f'[out:json][timeout:90];area["name"="{country}"]->.searchArea;(node["amenity"="place_of_worship"]["religion"="christian"](area.searchArea);way["amenity"="place_of_worship"]["religion"="christian"](area.searchArea););out center;'
    
    response = requests.post(overpass_url, data={'data': query})
    data = response.json()
    results = [{'name': e.get('tags', {}).get('name', 'N/A'), 'city': e.get('tags', {}).get('addr:city', 'N/A')} for e in data.get('elements', [])]
    
    # СОХРАНЯЕМ В КОРЕНЬ (важно для робота)
    with open("Russia_churches.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Собрано: {len(results)}")

if __name__ == "__main__":
    get_churches("Russia")
