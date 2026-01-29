import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pipeline import graphs, get_cleaned_data

df, df_filtered, mode_counts, stats, df_classic, top_10_wins, bottom_10_wins, df_champions, df_duration, df_match_agg = get_cleaned_data()

fig1, fig2, fig3, fig4, fig5, fig6, fig_agg = graphs(stats, mode_counts, top_10_wins, bottom_10_wins, df_champions, df_duration, df_match_agg, df_classic)


st.header('Champions statistics')

st.write("""I ett spel som Leauge Of Legends så finns det ett stort urval av champions en spelare kan välja på.
Det som kan vara svårt för ett spel är hur dessa champions förhåller sig i styrka till varandra.
Som vi kan se i de två graferna under så skiljer sig procenten av antal vinster ganska stort mellan den som har högst och den som har lägst.""")

st.write("""Frågan vi ställer oss i denna del av analysen är alltså, hur balanserat är spelet när det kommer till deras champions?""")

st.pyplot(fig3)

st.write("""Vid en första titt på datan hade man troligen konstaterat att detta spelet inte är så balanserat.
Är det ok att en champion har cirka 63% win rate medans en annan har cirka 37 %?
Troligtvis hade de som spelar detta spelet klagat något enormt om detta var fallet.

Men om vi tar en titt på win rate i förhållande till antal matcher en champion spelat, hur föhåller det sig då?
Ta en kik på tabellen nedan för att se den stora spridningen som finns i datasetet.""")

# I hide index to solve issue with name being double displayed as df_champion has been merged on "champion".
# Since it has been merged the names of champion is in index
st.dataframe(df_champions, hide_index=True,column_config={
        "Wins": "Antal Vinster",
        "Win Rate": st.column_config.NumberColumn(
            "Vinstprocent",
            format="%.2f %%"
        ),
        "Total Games": "Spelade Matcher"
    })

st.write("""Vi har alltså konstaterat att det finns en stor spridning i spelade matcher och i win rate på champions
och ställer oss då frågan, hur hänger dessa ihop och någon slutsats vi kan dra av detta?""")

st.write("""I scatterplotten under ser vi på y axeln en champions win rate och på x axeln ser vi antal spelade matcher.
        Varje cirkel representerar en champion.
        Från detta kan vi se att de flesta cirklarna finns i början av grafen och det har relativt stor spridning i win rate %.
        Ju längre ut på grafen vi kommer (alltså fler matcher spelade) ser vi ett mönster av att dessa börjat samlas kring cirka 50 %.
        Ett antagande som skulle kunna göras av detta är att ju fler spelade matcher en champion har desto större chans är det att deras 
        win rate ligger runt 50 %.
        Med andra ord skulle man kunna göra ett antagande att spelets champions verkar vara relativt balanserade.""")

show_trend = st.checkbox("Visa trendlinje och konfidensintervall")

if show_trend:
    st.write("""För att verkligen bekräfta vårt antagande har vi här lagt till en regressionslinje (den röda trendlinjen).
         Som vi ser ligger linjen nästan helt horisontellt, strax över 50-procentstrecket.
        Detta ger oss ett statistiskt kvitto på vår analys: trots den enorma spridningen vi ser vid låga volymer, så rör sig det stora genomsnittet stadigt mot mitten.
        Den svaga lutningen och det rosa skuggade området (konfidensintervallet) visar att ju mer data vi samlar in, desto tydligare blir det att balansen i spelet är stabil.""")

    st.info(""" Notera att konfidensintervallet blir något bredare längst ut till höger i grafen. 
        Detta beror troligtvis på att vi har färre champions med så höga matchantal, vilket skapar en naturlig statistisk osäkerhet i ytterkanterna av vårt dataset. 
        Det är i det täta klustret i mitten som vi ser den mest tillförlitliga bekräftelsen på spelets balans""")

    st.pyplot(fig5)

else:

    st.pyplot(fig4)

st.divider()

st.header("Slutsats")
st.write(""" En slutsats man kan dra av detta och på nästan all data att det är alltid viktigt att ställa datan emot varandra.
Det räcker inte att blint lite på det första bästa man ser. I detta fall hade det då konstaterats att spelet verkar vara obalanserat.
Även om det troligtvis är långt ifrån perfekt balanserat kan vi däremot se att trendlinjen pekar på något som vi inte kunde se om vi bara tittade på högst och lägst win rate.
""")


