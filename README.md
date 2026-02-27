# Project-Gerrymandering-in-Hungary
Gerrymandering in Hungary between 2014 and 2026
🗳️ Választási GeoJSON Feldolgozó Pipeline

Ez a repository a magyar országgyűlési választókerületek adatainak feldolgozására szolgáló scripteket tartalmazza.
A folyamat minden választási évben (4 évente) ismétlődik, majd az évek összevonásra kerülnek egy közös fájlba.

📂 Fájlok
json_changer_<ÉV>.py

Feladata az eredeti, letöltött JSON fájl GeoJSON formátummá alakítása.

Műveletek:

Régiókódok (maz) átalakítása megyei nevekké

Koordináták konvertálása GeoJSON formátumba ([longitude, latitude])

Hibás adatok kiszűrése

Polygonok lezárása

Kimenet:

hungary_voting_districts_<ÉV>.geojson

Minden választási évhez külön script tartozik.

add_year_<ÉV>.py

Hozzáad egy "year" mezőt minden választókerülethez.

Bemenet:

<ÉV>_election.json

Kimenet:

<ÉV>_election_with_year.json

Ez szükséges az évek későbbi összevonásához és szűréséhez.

combine_geojson_mapshaper_finals.py

Az összes év feldolgozott GeoJSON fájlját egyetlen FeatureCollection-be egyesíti.

Kimenet:

combined.json
🔄 Feldolgozási lépések (évenként)

json_changer_<ÉV>.py

add_year_<ÉV>.py

(opcionális tisztítás Mapshaperrel)

Miután minden év elkészült:
4. combine_geojson_mapshaper_finals.py

📊 Végső eredmény

A combined.json fájl tartalmazza az összes választási év összes választókerületét, így alkalmas:

Évek szerinti szűrésre

Idősoros térképes vizualizációra

GIS elemzésre

fix_combined.py (Shapely alapú javítás)
Cél

A combined.json fájlban található érvénytelen (invalid) polygon geometriák automatikus ellenőrzése és javítása.

Ez különösen fontos térképes megjelenítés vagy GIS elemzés előtt, mert hibás geometriák:

renderelési hibát okozhatnak

elemzési problémákat eredményezhetnek

nem kompatibilisek bizonyos GIS szoftverekkel

Működés

A script:

Betölti a combined.json fájlt

Minden feature geometriáját ellenőrzi (geom.is_valid)

Ha hibás geometriát talál:

kiírja a hiba okát (explain_validity)

javítja a geometriát a buffer(0) módszerrel

Elmenti a javított állományt:

combined_fixed.json
Használt könyvtár

shapely – geometriai műveletekhez és validációhoz

Telepítés:

pip install shapely
Mikor kell futtatni?

A teljes feldolgozási folyamat végén:

Éves fájlok előállítása

Évek összevonása (combine_geojson_mapshaper_finals.py)

Geometriák javítása ezzel a scripttel

Végső eredmény

A combined_fixed.json:

topológiailag érvényes polygonokat tartalmaz

stabilan használható GIS eszközökben

alkalmas publikációs vagy vizualizációs célokra
