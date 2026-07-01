
#!/usr/bin/env python3
# graphhopper_chile_argentina.py
# Calcula distancia entre ciudades de Chile y Argentina

import requests
import urllib.parse

API_KEY = "06762a27-b690-4cb0-a1f7-63765032470a"
GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

def geocoding(location):
    url = GEOCODE_URL + urllib.parse.urlencode({
        "q": location,
        "limit": "1",
        "key": API_KEY
    })
    resp = requests.get(url)
    data = resp.json()
    if resp.status_code == 200 and data.get("hits"):
        hit = data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit.get("name", location)
        country = hit.get("country", "")
        state = hit.get("state", "")
        full = f"{name}, {state}, {country}" if state and country else f"{name}, {country}" if country else name
        return True, lat, lng, full
    return False, None, None, location

def get_route(olat, olng, dlat, dlng, vehicle):
    url = (ROUTE_URL + 
           urllib.parse.urlencode({"key": API_KEY, "vehicle": vehicle}) +
           f"&point={olat}%2C{olng}&point={dlat}%2C{dlng}")
    resp = requests.get(url)
    return resp.status_code, resp.json()

def format_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

print("\n" + "="*50)
print("   CALCULADORA CHILE -> ARGENTINA")
print("="*50)

while True:
    print("\nModos: car, bike, foot  |  's' para salir")
    vehicle = input("Seleccione modo de transporte: ").lower()
    if vehicle == 's':
        print("Hasta luego!")
        break
    if vehicle not in ["car", "bike", "foot"]:
        print("Modo no valido. Usando 'car'.")
        vehicle = "car"
    
    origen = input("Ciudad de Origen (Chile): ")
    if origen.lower() == 's':
        break
    destino = input("Ciudad de Destino (Argentina): ")
    if destino.lower() == 's':
        break
    
    ok_o, lat_o, lng_o, name_o = geocoding(origen)
    if not ok_o:
        print(f"Error: No se encontró '{origen}'")
        continue
    ok_d, lat_d, lng_d, name_d = geocoding(destino)
    if not ok_d:
        print(f"Error: No se encontró '{destino}'")
        continue
    
    status, data = get_route(lat_o, lng_o, lat_d, lng_d, vehicle)
    if status != 200:
        print(f"Error en ruta: {data.get('message', 'Desconocido')}")
        continue
    
    path = data["paths"][0]
    dist_m = path["distance"]
    time_ms = path["time"]
    km = dist_m / 1000
    miles = km / 1.60934
    seg = time_ms / 1000
    
    print("\n" + "="*50)
    print(f"Origen: {name_o} -> Destino: {name_d}  |  Modo: {vehicle}")
    print(f"Distancia: {km:.1f} km / {miles:.1f} miles")
    print(f"Duracion: {format_time(seg)}")
    print("="*50)
    print("\nInstrucciones del viaje:")
    for i, step in enumerate(path.get("instructions", []), 1):
        text = step.get("text", "")
        dist = step.get("distance", 0) / 1000
        print(f"{i:2d}. {text} ({dist:.2f} km)")
    print("\n" + "="*50)
