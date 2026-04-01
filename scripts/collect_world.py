import requests, json, os

def fetch_churches(country):
    print(f"📡 Запрос данных для: {country}...")
    url = "https://overpass-api.de"
    
    # Собираем данные: Название, Город, Сайт, Координаты
    query = f"""
    [out:json][timeout:180];
    area["name"="{country}"]->.searchArea;
    (node["amenity"="place_of_worship"]["religion"="christian"](area.searchArea);
     way["amenity"="place_of_worship"]["religion"="christian"](area.searchArea););
    out center;
    """
    
    try:
        r = requests.post(url, data={'data': query})
        data = r.json()
        
        clean = []
        for e in data.get('elements', []):
            t = e.get('tags', {})
            clean.append({
                "n": t.get("name", "Unknown"),
                "c": t.get("addr:city", "N/A"),
                "w": t.get("website", "N/A"),
                "lat": e.get("lat", e.get("center", {}).get("lat")),
                "lon": e.get("lon", e.get("center", {}).get("lon"))
            })
        
        os.makedirs("database", exist_ok=True)
        path = f"database/{country.lower().replace(' ', '_')}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(clean, f, ensure_ascii=False, indent=2)
        print(f"✅ Готово: {len(clean)} объектов в {path}")
        
    except Exception as e:
        print(f"❌ Ошибка {country}: {e}")

if __name__ == "__main__":
    # Список стран для твоей глобальной Web3-сети
    target_countries = ["Russia", "Vatican City", "Italy", "USA", "Brazil"]
    for country in target_countries:
        fetch_churches(country)
