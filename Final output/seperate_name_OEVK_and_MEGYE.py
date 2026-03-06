import json

# ---- File paths ----
input_file = r"C:\Users\kocsi\Desktop\ACT PROJ\1 FIND JOB\00 PLANT JOB\SUPPORT MATERIALS\Article 54 VOTING HUNGARY\github data\Final output\combined_fixed.json"
output_file = r"C:\Users\kocsi\Desktop\ACT PROJ\1 FIND JOB\00 PLANT JOB\SUPPORT MATERIALS\Article 54 VOTING HUNGARY\github data\Final output\combined_fixed_name_seperated.json"

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

# Reverse mapping: region name -> code
region_codes = {v: k for k, v in region_names.items()}

# ---- Load file ----
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# ---- Process features ----
for feature in data["features"]:
    props = feature.get("properties", {})
    name = props.get("name", "")

    if name:
        parts = name.rsplit(" ", 1)

        if len(parts) == 2:
            region_name, district_number = parts

            # Add OEVK
            props["OEVK"] = district_number

            # Add MEGYEKÓD
            if region_name in region_codes:
                props["MEGYEKÓD"] = region_codes[region_name]

# ---- Save new file ----
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Finished. File saved as combined_fixed_name_seperated.json")