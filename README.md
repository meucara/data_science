# data_science
**Projektet**

Detta projekt är skapat för att utforska och visualisera mönster i League Of Legends-matcher spelade på servrarna EU North & East (EUNE) under 2025.

Datan är hämtad från: https://www.kaggle.com/datasets/jakubkrasuski/league-of-legends-match-dataset-2025/data

Målet är att analysera, visualisera och applicera ML för att skapa förståelse.

**Struktur**

Följande ordning av filer är även rekommendation för läsaren att gå igenom.

*pipeline.py – hanterar inläsning av data, data cleaning, nya beräkningar samt skapande av figurer som anropas till streamlitsidorna (dessa ligger i pages) för att hålla dessa renare.\n
*ml_data.py – hanterar allt som handlar om ML, hämtar rätt data från pipeline, skapar ML logik inkluderat med train,val,test och gridsearch. Returnerar data och figurer som anropas till rätt streamlitsida (ml.py i pages)\n
*navigator.py – innehåller sidostruktur för hemsida och är även denna som körs i streamlit som hämtar allt från sidorna i pages.\n
*league_data_fast.csv – CSV fil med rådata som hämtas in i pipeline.py.*

pages:

Beräkningar och figurer sköts ej i dessa sidor för att det ska hållas rena, dessa hämtas som funktioner från pipeline.py och ml_data.py istället. Funktionerna körs i början av varje kod för att tydliggöras.

*streamlit.py – introduktionssida med information om projekt och syfte.
data_cleaning.py – sida där val av städning förklaras och varför.
game.py – sida som analyserar data som handlar om matcher i spelet.
champion.py – sida som analyserar data som handlar specifikt om champions i spelet.
ml.py – sida for att analysera och visualisera resultat från ML.
requirements.txt – innehåller vilka paket som använts och vad som krävs för att köra sidan.* 
