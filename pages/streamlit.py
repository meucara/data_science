import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pipeline import graphs, get_cleaned_data

st.title("League of Legends: Dataanalys & Machine Learning")

st.markdown("""
### Välkommen till analysen av EUNE-metan 2025
Denna applikation är skapad för att utforska och visualisera mönster i League of Legends-matcher spelade på servrarna **EU North & East (EUNE)** under **2025**. 

#### Om datan
Datasetet innehåller detaljerad statistik från tusentals matcher, inklusive:
* **Matchdynamik:** Längd, vinstresultat och matchtyper (Remakes, Surrenders, Full Games).
* **Prestationsmått:** Kills, deaths, assists, skada på champions och objektive-kontroll.
* **Karaktärsdata:** Champion Mastery och tekniska stats (Ability Haste, Health, etc.) vid matchens slut.

#### Syfte och metod
Tanken med projektet är tredelad:
1. **Explorativ Analys:** Att gräva i datan för att se hur moderna matcher faktiskt ser ut i den nuvarande säsongen.
2. **Visualisering:** Skapa tydliga grafer som lyfter fram intressanta samband som annars är svåra att se i rådata.
3. **Machine Learning:** Genom att använda modeller som **XGBoost** och **Random Forest** identifierar vi "Feature Importance" – det vill säga vilka variabler som statistiskt sett väger tyngst för att avgöra om ett lag vinner eller förlorar.

*Använd menyn till vänster (eller flikarna nedan) för att navigera mellan den visuella analysen och insikterna från våra ML-modeller.*
""")

st.divider()



