import json

# Input and output file paths
input_file = "hungary_voting_districts_2022.geojson"   # your original 2022 file
output_file = "2022_election_with_year.json"  # new file with year added

# Load the original GeoJSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Add "year": 2022 to each feature's properties
for feature in data.get("features", []):
    feature.setdefault("properties", {})  # make sure "properties" exists
    feature["properties"]["year"] = 2022

# Save the modified GeoJSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added 'year': 2022 to all features. Saved as {output_file}")
