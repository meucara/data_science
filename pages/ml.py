import streamlit as st
from pipeline import get_cleaned_data
from ml_data import get_ml_results


# Hämta data
df, _, _, _, df_classic, *_ = get_cleaned_data()

# Definiera vad som räknas som läckage
STRATEGIC_FEATURES = [
    'champion_mastery_level',
    'wards_placed',
    'time_ccing_others',
    'wards_killed',
    'vision_wards_bought_in_game',
    'summoner_level'
]

OBJECTIVE_FEATURES = [
        'baron_kills',
        'dragon_kills'
]

MODEL_DESCRIPTIONS = {
    "All data (Läckage)": """
        **Analys:** Denna modell har en extremt hög precision eftersom den ser 'facit'. 
        Här ser vi tydligt att guldövertag och skada på torn vid dominerar helt, 
        vilket bekräftar teorin om dataläckage.
    """,
    "Macro och summoner skicklighet": """
        **Analys:** Här ser på skillnaden mellan macro (förmåga att spela på hela planen och inte bli fast där man är) kontra speltid. 
        Notera hur stor vikt modellen lägger vid vision score och CC-tid jämfört med summoner level. En kort analys av detta indikerar lite på att det inte räcker att spela mycket och bemästra en champion.
        Utan det är viktigt att lära sig spela tillsammns och bidra till kontroll av banan.
    """,
    "Objectives importance": """
        **Analys:** Resultatet visar att modellen värderar drakar högre än Barons i detta dataset. 
        Detta kan bero på att drakar tas mer frekvent och ger en kumulativ fördel över tid, vilket gör dem till en stabilare indikator på vilket lag som har kontroll över matchen.
        Det kan inte sägas att drakar leder till vinst kanske men det visar på att det är en viktig faktor (se den höga accuracyn) att prioritera och att det möjligen är bättre att ta drake framför baron om det uppstår ett val.
    """
}


st.title("🤖 ML Modell-analys")

st.info("Du finner modellerna längst ner på sidan efter en kort introduktion om denna del av analysen.")

st.write("""
Denna del av analysen använder maskininlärning för att identifiera vilka faktorer "features" som har störst påverkan på utgången av en match. Genom att analysera historisk data kan modellen lära sig mönster som skiljer vinnande lag från förlorande.

Modellen bygger på följande arbetsflöde:

RandomForestClassifier: Vald för att den hanterar klassificeringsproblem väl och ger tydlig insikt i Feature Importance.

Train/Val/Test: Datan delas upp i tre delar. Modellen tränas på träningssetet, finjusteras mot valideringssetet och utvärderas slutligen mot ett helt dolt testset för att säkerställa att den inte bara "lär sig utantill" (overfitting).

GridSearch: En automatiserad sökning genomförs för att hitta de optimala hyperparametrarna (t.ex. trädens djup och antal), vilket maximerar modellens precision .""")

st.divider()

st.write("""
Problematik: Dataläckage (Data Leakage)

I "All data" inkluderas variabler som total skada på torn eller guldövertag som är från sista sekunden. Detta skapar "läckage" eftersom dessa värden i praktiken är resultatet av vinsten snarare än strategin som ledde dit. 
Om motståndarens Nexus är nere kommer din "skada på torn" vara maximal – modellen behöver då inte vara "smart" för att gissa vinnaren, den behöver bara läsa av slutstatistiken.

För att få en mer intressant analys finns läget "Macro och summoner skicklighet". Här har vi filtrerat bort den mest uppenbara slutstatistiken och fokuserar istället på:

* Vision Control: Hur bra laget placerar och förstör wards.

* Erfarenhet: Spelarnas summoner level och champion mastery.

* Lagspel: CC-tid (Crowd Control) och assistans.

En sista analys (Objective importance) görs även på objectives "Baron" och "Dragon".
Dessa två är en ständig diskussion inom Leauge Of Legends världen vilken som är viktigast. I matcher är det heta diskussioner om vilken som bör prioriteras högst.
Vissa säger att Dragon inte är viktig och att det är lika bra att lämna den för det andra laget för att fokusera på annat.
I denna modell testas alltså dessa två features mot varandra för att se vilken av dessa som modellen anser väga tyngst.
""")
st.divider()
mode = st.radio("**Välj typer av feature importance**:",
                ["All data (Läckage)", "Macro och summoner skicklighet", "Objectives importance"])

# Using ml_results and st.session to get around problem of repressing button everytime to show the figures.
# When flipping through the different models it will be the last figure shown because of st.session but with added "Latest run".
# This makes sure the person knows it's the previous one.
if 'ml_results' not in st.session_state:
    st.session_state.ml_results = None


if st.button("🚀 Starta träning"):
    if mode == "Macro och summoner skicklighet":
        features = STRATEGIC_FEATURES
        msg = "Tränar modell på ej läckande data..."
    elif mode == "Objectives importance":
        features = OBJECTIVE_FEATURES
        msg = "Kollar på Dragon vs Baron..."
    else:
        features = None
        msg = "Tränar modell på fullständig data och söker efter feature importance..."

    with st.spinner(msg):
        fig, results = get_ml_results(df_classic, selected_features=features)

        # Saves the fig for the session.
        st.session_state.ml_results = {
            'fig': fig,
            'results': results,
            'mode': mode  # Spara vilket läge som kördes
        }

# Here follows the session logic to show the figure if in session
if st.session_state.ml_results is not None:
    res_data = st.session_state.ml_results
    results = res_data['results']

    if results.get('data_check'):
        st.success(f"✅ Dataintegritet bekräftad: {results['num_matches']} matcher par ihop korrekt via Game ID.")
    else:
        st.error("❌ VARNING: Datafel upptäckt! Match-ID:n på raderna stämmer inte överens.")


    st.subheader(f"Senaste körning: {res_data['mode']}")
    st.metric("Test Accuracy", f"{res_data['results']['test_acc']:.1%}")
    # HÄR LÄGGER VI TILL TEXTEN
    # Vi hämtar beskrivningen baserat på det 'mode' som sparades i session_state
    description = MODEL_DESCRIPTIONS.get(res_data['mode'], "")
    st.info(description)

    st.pyplot(res_data['fig'])

