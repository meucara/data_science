# data_science
**Projektet**

Detta projekt är skapat för att utforska och visualisera mönster i League Of Legends-matcher spelade på servrarna EU North & East (EUNE) under 2025.

Datan är hämtad från: https://www.kaggle.com/datasets/jakubkrasuski/league-of-legends-match-dataset-2025/data

Målet är att analysera, visualisera och applicera ML för att skapa förståelse.

# Projektstruktur

Det rekommenderas att läsa filerna i den ordning de listas nedan för att bäst förstå dataflödet.


**`navigator.py`**              # Huvudfilen som kör Streamlit och hanterar sidnavigering.

**`pipeline.py`**               # Data processing: Inläsning, städning, beräkningar och grafer.
`ml_data.py`                # ML-motor: Logik för train/val/test-split samt GridSearch.
league_data_fast.csv      # Rådata från Kaggle som används i projektet.
requirements.txt          # Lista över nödvändiga Python-bibliotek (t.ex. Scikit-learn, Seaborn).

pages/                # (rena sidor som anropar funktioner)
streamlit.py          # Introduktion, syfte och bakgrund till projektet.
data_cleaning.py      # Genomgång av hur datan har tvättats.
game.py               # Analys och visualisering av matchstatistik.
champion.py           # Djupdykning i statistik för specifika champions.
ml.py                 # Visualisering av ML-resultat och Feature Importance.
