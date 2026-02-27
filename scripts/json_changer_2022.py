import json

# ---- Load original JSON ----
with open("2022_election_downloaded.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ---- Correct region mapping (maz -> region name) ----
region_names = {
    "01": "Budapest",
    "02": "Baranya",
    "03": "Bács-Kiskun",
    "04": "Békés",
    "05": "Borsod-Abaúj-Zemplén",
    "06": "Csongrád-Csanád",
    "07": "Fejér",
    "08": "Győr-Moson-Sopron",
    "09": "Hajdú-Bihar",
    "10": "Heves",
    "11": "Jász-Nagykun-Szolnok",
    "12": "Komárom-Esztergom",
    "13": "Nógrád",
    "14": "Pest",
    "15": "Somogy",
    "16": "Szabolcs-Szatmár-Bereg",
    "17": "Tolna",
    "18": "Vas",
    "19": "Veszprém",
    "20": "Zala"
}

features = []

# ---- IMPORTANT FIX: iterate over data["list"] ----
for item in data.get("list", []):

    if not isinstance(item, dict):
        continue

    maz = item.get("maz")
    evk = item.get("evk")

    if not maz or maz not in region_names:
        print("Unknown or missing maz code:", maz)
        continue

    if not evk:
        print("Missing evk for maz:", maz)
        continue

    evk_formatted = str(evk).zfill(2)
    district_name = f"{region_names[maz]} {evk_formatted}"

    poly_str = item.get("poligon")
    if not poly_str:
        print("Missing polygon for:", district_name)
        continue

    coords = []

    for point in poly_str.split(","):
        try:
            lat_str, lon_str = point.strip().split()
            lat = float(lat_str)
            lon = float(lon_str)

            # GeoJSON uses [longitude, latitude]
            coords.append([lon, lat])

        except ValueError:
            print("Skipping malformed point in:", district_name)
            continue

    # Need at least 3 points for a polygon
    if len(coords) < 3:
        print("Invalid polygon (too few points):", district_name)
        continue

    # Ensure polygon is closed
    if coords[0] != coords[-1]:
        coords.append(coords[0])

    feature = {
        "type": "Feature",
        "properties": {
            "name": district_name
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [coords]
        }
    }

    features.append(feature)

# ---- Create GeoJSON ----
geojson = {
    "type": "FeatureCollection",
    "features": features
}

# ---- Save output ----
with open("hungary_voting_districts_2022.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2, ensure_ascii=False)

print(f"✅ Saved hungary_voting_districts_2022.geojson with {len(features)} districts")