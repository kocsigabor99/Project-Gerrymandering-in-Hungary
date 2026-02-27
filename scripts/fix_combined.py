import json
from shapely.geometry import shape, mapping
from shapely.validation import explain_validity

# Path to your file
input_path = r"C:\Users\kocsi\Desktop\ACT PROJ\1 FIND JOB\00 PLANT JOB\SUPPORT MATERIALS\Article 54 VOTING HUNGARY\github data\combined.json"
output_path = r"C:\Users\kocsi\Desktop\ACT PROJ\1 FIND JOB\00 PLANT JOB\SUPPORT MATERIALS\Article 54 VOTING HUNGARY\github data\combined_fixed.json"

# Load GeoJSON
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

invalid_count = 0

for feature in data["features"]:
    geom = shape(feature["geometry"])

    if not geom.is_valid:
        invalid_count += 1
        print("Invalid geometry found:")
        print("Reason:", explain_validity(geom))

        # Fix geometry
        fixed_geom = geom.buffer(0)

        # Replace geometry
        feature["geometry"] = mapping(fixed_geom)

print(f"\nTotal invalid geometries fixed: {invalid_count}")

# Save fixed file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f)

print("Fixed file saved as combined_fixed.json")