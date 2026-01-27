import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pipeline import graphs, get_cleaned_data



df, df_filtered, mode_counts, stats, df_classic, top_10_wins, bottom_10_wins, df_champions, df_duration, df_match_agg = get_cleaned_data()

fig1, fig2, fig3, fig4, fig5, fig6, fig_agg = graphs(stats, mode_counts, top_10_wins, bottom_10_wins, df_champions,
                                                     df_duration, df_match_agg, df_classic)

st.header("DATA CLEANING")

st.write("""I denna del så analyseras datan för att städa bort det som inte är relevant för kommande analyser.
Fokus här ligger på att hitta matcher som inte är fullständiga och matcher som inte är av samma typ.""")


st.info("""
**Definitioner för matchlängd:**
* **Full Game:** Över 15 minuter (Matchen spelades troligtvis klart).
* **Early Surrender:** Mellan 3,5 och 15 minuter (Högst troligt att någon lämnat).
* **Remake:** Under 3,5 minuter (Garanterat att någon lämnat).
""")
st.write("""För att få en tydligare bild av matcherna och få mer intressant data att titta på,
 kommer fokus enbart att ligga på "Full Game".""")

st.write("""Under följer data för att visa på hur många matcher datan innehåller och fördelningen av de olika "matchtyperna" 
 """)

st.dataframe(stats, hide_index=True, use_container_width=True)

st.pyplot(fig1)


st.write("I datan finns det även olika typer av modes (typer av spel inom League Of Legends)."
         "Ut av de 3828 games som är kvar efter första städningen med matchens längd görs ännu en städning där analysen sedan fokuserar enbart på Classic mode.")

st.info("""
    **Olika Game Modes:**
    * **CLASSIC** = 5v5 på den vanligaste banan som alla internationella tävlingar körs på.
    * **ARAM** = En bana för att bara "ha roligt".
    * **SWIFTPLAY** = Ett mellanting mellan Aram och Classic där det spelas på CLASSIC bana men allt går mycket fortare.
    """)


st.dataframe(mode_counts, hide_index=True, use_container_width=True)

st.pyplot(fig2)
