import streamlit as st


st.title("League of Legends: Dataanalys & Machine Learning")

st.markdown("""
### Välkommen till en analys av EUNE-match data från 2025
Denna applikation är skapad för att utforska och visualisera mönster i League of Legends-matcher spelade på servrarna **EU North & East (EUNE)** under **2025**. 

Datan är hämtad från: https://www.kaggle.com/datasets/jakubkrasuski/league-of-legends-match-dataset-2025/data

#### Om datan
Datasetet innehåller detaljerad statistik från tusentals matcher, inklusive:
* **Matchdynamik:** Längd, vinstresultat och matchtyper.
* **Prestationsmått:** Kills, deaths, assists, skada på champions och objectives.
* **Karaktärsdata:** Champion Mastery och tekniska stats (Ability Haste, Health, etc.) vid matchens slut.

#### Syfte och metod
Tanken med projektet är tredelad:
1. **Explorativ Analys:** Att gräva i datan för att se , till exempel, vinstprocenten bland champions och en matchs längd i förhållande till hur mycket tid som spelarna lagt på spelet.
2. **Visualisering:** Skapa tydliga grafer som lyfter fram intressanta samband som annars är svåra att se i rådata.
3. **Machine Learning:** Genom att använda **Random Forest** identifierars "Feature Importance" – det vill säga vilka variabler som statistiskt sett väger tyngst för att avgöra om ett lag vinner eller förlorar.

*Använd menyn till vänster för att navigera mellan data städning, champion analys, game analys och insikterna från ML "Feature importance".*
""")

st.divider()



