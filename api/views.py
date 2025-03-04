import requests
from bs4 import BeautifulSoup
import json
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os
import certifi
import os
from django.http import JsonResponse
from django.conf import settings

os.environ["SSL_CERT_FILE"] = certifi.where()

# Configuration de geopy
geolocator = Nominatim(user_agent="pharmacies_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_coordinates(address):
    try:
        location = geocode(f"{address}, Togo")
        return (location.latitude, location.longitude) if location else (None, None)
    except:
        return (None, None)

def fetch_pharmacies_data():
    url = 'https://www.inam.tg/pharmacies-de-garde/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'tablepress-189'})

    pharmacies = []
    for idx, row in enumerate(table.find_all('tr')[1:], start=1):
        cols = row.find_all('td')
        if len(cols) != 3:
            continue

        nom = cols[0].text.strip()
        telephone = cols[1].text.strip().replace('☎', '').strip()
        emplacement = cols[2].text.strip()
        
        # Nettoyage du numéro de téléphone
        if telephone.startswith('22'):
            telephone = f"+228 {telephone}"
        else:
            telephone = f"+228 {telephone[1:]}" if len(telephone) == 8 else telephone

        # Géocodage
        latitude, longitude = get_coordinates(nom)

        pharmacies.append({
            "id": str(idx),
            "name": nom,
            "address": emplacement,
            "hours": "AM - PM",
            "isOpen": True,
            "phone": telephone,
            "latitude": latitude if latitude else 8.621697000000001,
            "longitude": longitude if longitude else 0.8296844999999848
        })
        with open('pharmacies.json', 'w', encoding='utf-8') as f:
            json.dump(pharmacies, f, ensure_ascii=False, indent=4)


    return json.dumps(pharmacies, ensure_ascii=False, indent=4)

# Exemple d'utilisation
if __name__ == "__main__":
    data = fetch_pharmacies_data()
    print(data)





def pharmacies_list(request):
    file_path = os.path.join(settings.BASE_DIR, 'pharmacies.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)