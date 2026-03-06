import json
import pandas as pd

# -------- FILE PATHS --------

geojson_file = r"C:\Users\kocsi\Desktop\ACT PROJ\1 FIND JOB\00 PLANT JOB\SUPPORT MATERIALS\Article 54 VOTING HUNGARY\github data\Final output\combined_fixed_name_seperated.json"

excel_file = r"C:\Users\kocsi\Desktop\ACT PROJ\1 FIND JOB\00 PLANT JOB\SUPPORT MATERIALS\Article 54 VOTING HUNGARY\github data\Final output\Egyéni_szavazás_szkjkv_2022_copied.xlsx"

output_file = r"C:\Users\kocsi\Desktop\ACT PROJ\1 FIND JOB\00 PLANT JOB\SUPPORT MATERIALS\Article 54 VOTING HUNGARY\github data\Final output\combined_fixed_name_seperated_2022_szkjkv_added.json"


# -------- LOAD EXCEL --------

df = pd.read_excel(excel_file, dtype=str)

# Ensure numeric votes
df["SZAVAZAT"] = pd.to_numeric(df["SZAVAZAT"], errors="coerce")


# -------- SPLIT ROW TYPES --------

totals = df[df["SZAVAZÓKÖR_AZON"].str.endswith("F", na=False)].copy()
candidates = df[df["SZAVAZÓKÖR_AZON"].str.endswith("T", na=False)].copy()


# -------- FIX NUMERIC TOTAL COLUMNS --------

numeric_cols = [
    "VÁLASZTÓPOLGÁR",
    "MEGJELENTEK",
    "URNÁBAN_LEVŐ",
    "ÉRVÉNYTELEN",
    "ÉRVÉNYES"
]

for col in numeric_cols:
    totals[col] = pd.to_numeric(totals[col], errors="coerce")


# -------- DISTRICT TOTALS (SUM POLLING STATIONS) --------

district_totals = (
    totals
    .groupby(["MEGYEKÓD", "OEVK"])[numeric_cols]
    .sum()
    .reset_index()
)

district_totals["MEGYEKÓD"] = district_totals["MEGYEKÓD"].astype(str).str.zfill(2)
district_totals["OEVK"] = district_totals["OEVK"].astype(str).str.zfill(2)


# -------- FIX CANDIDATE DISTRICT INFO --------

district_map = totals[["JKV_AZONOSÍTÓ", "MEGYEKÓD", "OEVK"]].drop_duplicates()

candidates = candidates.merge(
    district_map,
    on="JKV_AZONOSÍTÓ",
    how="left",
    suffixes=("", "_from_totals")
)

if "MEGYEKÓD_from_totals" in candidates.columns:
    candidates["MEGYEKÓD"] = candidates["MEGYEKÓD_from_totals"]

if "OEVK_from_totals" in candidates.columns:
    candidates["OEVK"] = candidates["OEVK_from_totals"]

candidates["MEGYEKÓD"] = candidates["MEGYEKÓD"].astype(str).str.zfill(2)
candidates["OEVK"] = candidates["OEVK"].astype(str).str.zfill(2)


# -------- AGGREGATE CANDIDATE VOTES --------

candidate_totals = (
    candidates
    .groupby(["MEGYEKÓD", "OEVK", "JELÖLT", "SZERVEZET"])["SZAVAZAT"]
    .sum()
    .reset_index()
)


# -------- LOAD GEOJSON --------

with open(geojson_file, "r", encoding="utf-8") as f:
    geo = json.load(f)


# -------- MERGE DATA INTO GEOJSON --------

for feature in geo["features"]:

    props = feature["properties"]

    megye = str(props.get("MEGYEKÓD")).zfill(2)
    oevk = str(props.get("OEVK")).zfill(2)

    # ---- district totals ----

    match = district_totals[
        (district_totals["MEGYEKÓD"] == megye) &
        (district_totals["OEVK"] == oevk)
    ]

    if not match.empty:

        row = match.iloc[0]

        props["VÁLASZTÓPOLGÁR"] = int(row["VÁLASZTÓPOLGÁR"])
        props["MEGJELENTEK"] = int(row["MEGJELENTEK"])
        props["URNÁBAN_LEVŐ"] = int(row["URNÁBAN_LEVŐ"])
        props["ÉRVÉNYTELEN"] = int(row["ÉRVÉNYTELEN"])
        props["ÉRVÉNYES"] = int(row["ÉRVÉNYES"])


    # ---- candidate results (FLAT STRUCTURE) ----

    cand = candidate_totals[
        (candidate_totals["MEGYEKÓD"] == megye) &
        (candidate_totals["OEVK"] == oevk)
    ]

    cand = cand.sort_values("SZAVAZAT", ascending=False).reset_index(drop=True)

    for i, r in cand.iterrows():

        idx = i + 1

        props[f"cand_{idx}_name"] = r["JELÖLT"]
        props[f"cand_{idx}_party"] = r["SZERVEZET"]
        props[f"cand_{idx}_votes"] = int(r["SZAVAZAT"])


# -------- SAVE RESULT --------

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(geo, f, ensure_ascii=False, indent=2)

print("Finished building election GeoJSON.")