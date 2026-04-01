import requests
import json

def get_churches(country="Russia"):
    print(f"Начинаю сбор данных по стране: {country}...")
    
    # Запрос к Overpass API (OSM) на 2026 год
    overpass_url = "https://overpass-api.de"
    query = f"""
    [out:json][timeout:60];
    area["name"="{country}"]->.searchArea;
    (
      node["amenity"="place_of_worship"]["religion"="christian"](area.searchArea);
      way["amenity"="place_of_worship"]["religion"="christian"](area.searchArea);
    );
    out center;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': query})
        data = response.json()
        
        results = []
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            results.append({
                'name': tags.get('name', 'N/A'),
                'city': tags.get('addr:city', 'N/A'),
                'street': tags.get('addr:street', 'N/A'),
                'website': tags.get('website', 'N/A'),
                'lat': element.get('lat', element.get('center', {}).get('lat')),
                'lon': element.get('lon', element.get('center', {}).get('lon'))
            })
            
        with open(f"{country}_churches.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
            
        print(f"Готово! Собрано объектов: {len(results)}")
        
    except Exception as e:
        print(f"Ошибка при сборе: {e}")

if __name__ == "__main__":
    get_churches("Russia")
