import json

# Input and output file paths
input_file = "2026_election.json"   # your original 2026 file
output_file = "2026_election_with_year.json"  # new file with year added

# Load the original GeoJSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Add "year": 2026 to each feature's properties
for feature in data.get("features", []):
    feature.setdefault("properties", {})  # make sure "properties" exists
    feature["properties"]["year"] = 2026

# Save the modified GeoJSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added 'year': 2026 to all features. Saved as {output_file}")
