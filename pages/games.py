import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pipeline import graphs, get_cleaned_data

df, df_filtered, mode_counts, stats, df_classic, top_10_wins, bottom_10_wins, df_champions, df_duration, df_match_agg = get_cleaned_data()

fig1, fig2, fig3, fig4, fig5, fig6, fig_agg = graphs(stats, mode_counts, top_10_wins, bottom_10_wins, df_champions, df_duration, df_match_agg, df_classic)

st.header("Game statistics")

st.write("""Som visat i data cleaning så fokuserar analysen av datan i detta projekt enbart på det utvalda kriterierna:
* **Classic mode (5v5)**
* **Matcher som inte have störningar så som spelare som lämnat**""")

st.write("""Under finner du en graf som visar fördelningen av antalet matcher och hur många minuter de varar.
Som kan tydas av grafen så är det vanligaste snittet cirka 30 minuter.""")

st.pyplot(fig6)

st.write("""Det finns flera variabler som kan avgöra hur länge en match varar men en hypotes som antogs för denna analys var att:
* Ju lägre level en spelare har (alltså hur mycket tid de spenderat i spelet) ju längre.

Anledning till denna hypotes skulle vara att de höglvlade spelarna dels:
* Kan kontrollera matchen om de får ledningen och avsluta snabbare genom att fatta rätt beslut.
* Motståndarlaget som ligger under kan tydligt se att det inte finns någon väg tillbaka in i matchen och ger upp.

För att analysera detta har det använts en boxplot där det har grupperats på medelvärdet av spelarnas "Summoner level" per match.""")

st.pyplot(fig_agg)
with st.expander("Vad betyder boxens storlek? (Lär dig mer om IQR)"):
    st.write("""
    **Interkvartilavståndet (IQR)** är höjden på boxen i grafen och representerar de mellersta 50 % av alla matcher i dens grupp.
    * **Stor box:** Stor spridning i matchlängd (mer oförutsägbart).
    * **Liten box:** Matcherna är mer konsekventa och samlade kring medianen.
    * **Cirklarna:** Kallas för 'outliers' (extremvärden) och är matcher som varar ovanligt länge/kort jämfört med det normala för den gruppen.
    """)

st.write("""Analys av matchlängd baserat på erfarenhetsnivå:
* Genom att dela upp datan i tre grupper framträder en tydlig trend där de mest erfarna spelarna (High Level 701+) har den lägsta medianmatchlängden. Detta tyder på att hypotesen verkar stämma och att "veteraner" har en högre förmåga att avsluta snabbare.

* Stabilitet vs. Kaos: Gruppen Low Level (0-385) uppvisar en större box, vilket indikerar en högre varians och mer oförutsägbara matchförlopp. I kontrast är High Level-boxen mer kompakt, vilket visar på en mer standardiserad och stabil spelstil.

* Matchmakingens utjämningseffekt: Den generellt låga variansen mellan gruppernas medianer kan förklaras av Riots matchmaking-algoritmer. Genom att blanda spelare med olika "Summoner Levels" för att balansera lagens totala styrka skapas en utjämning i datan som troligtvis döljer de mest extrema skillnaderna.

* Trots erfarenhetsnivå finns det i alla kategorier matcher som sträcker sig över 50 minuter (se cirklarna, dessa är anomalier i varje grupp). Detta visar att vissa matcher, oberoende av spelarnas skicklighet och summoner level inte kan direkt avgöra att en match kommer avslutas snabbt.
""")


st.divider()

st.header("Slutsats")
st.write("""
Sammanfattningsvis ger datan stöd för hypotesen att högre erfarenhet leder till mer effektiva och kortare matcher, men analysen belyser också en komplexiteten:

* Bekräftad trend trots utjämning: Även om skillnaderna i minuter är små, ser vi en konsekvent minskning av både matchtid och varians i takt med att spelarnas genomsnittliga nivå ökar. Detta tyder på att erfarenhet faktiskt bidrar till en mer "stabila" matcher.

* Matchmakingens roll: Att resultaten inte är mer extrema är sannolikt ett tecken på att Riots matchmaking fungerar som den ska. Systemet strävar efter jämna matcher genom att balansera lagens sammansättning, vilket skapar en naturlig statistisk utjämning.

* Level vs. Rank: En viktig insikt från analysen är att "Summoner Level" endast mäter nedlagd tid, inte nödvändigtvis skicklighet. En intressant vidareutveckling hade varit att analysera matcherna baserat på Rank (t.ex. Silver vs. Diamond).

* Problematiken med "Smurfing": Genom att titta på rank istället för level skulle man kunna isolera effekten av skicklighet från erfarenhet. En skicklig spelare på ett nytt konto ("smurf") har en låg level men är troligtvis mycket bättre än de andra i matchen, vilket kan förvränga data som enbart baseras på summoner level.
""")

