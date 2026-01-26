import streamlit as st

# Defining the pages
intro_page = st.Page("pages/streamlit.py", title="Project info", icon="🏠")
data_cleaning_page = st.Page("pages/data_cleaning.py", title="Data Cleaning", icon="🧹")
games_page = st.Page("pages/games.py", title="Game Statistics", icon="🎮")
champion_page = st.Page("pages/champions.py", title="Champion Statistics", icon="👤")
ml_page = st.Page("pages/ml.py", title="Feature Importance", icon="🧠")
# Creating the menu
pg = st.navigation([intro_page, data_cleaning_page, games_page, champion_page, ml_page])

# Run this file
pg.run()