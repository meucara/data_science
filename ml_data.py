import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


@st.cache_data
def prepare_ml_data(df_classic):
    """Preparing team statistics and counting diff with focus on team 1."""
    df_classic = df_classic.fillna(0)
    # Some columns contains
    numerical_columns = df_classic.select_dtypes(include=['number']).columns.tolist()


    aggregation_rules = {
        'game_start_utc': 'first',
        'game_minutes': 'first',
        'win': 'first',
#---------------OBJECTIVES----------------------
        'baron_kills': 'sum',
        'dragon_kills': 'sum',
#--------------GAME STATS----------------------
        'gold_earned': 'sum',
        'kills': 'sum',
        'deaths': 'sum',
        'assists': 'sum',
        'total_damage_dealt': 'sum',
        'damage_dealt_to_turrets': 'sum',
        'total_damage_dealt_to_champions': 'sum',
        'damage_dealt_to_objectives': 'sum',
        'total_damage_taken': 'sum',

#--------------------PLAYER STATS------------------
        'summoner_level': 'mean',
        'champion_mastery_level': 'mean',
#---------------------WARDS---------------------
        'vision_score': 'sum',
        'wards_placed': 'sum',
        'time_ccing_others': 'mean',
        'vision_wards_bought_in_game': 'sum',
        'wards_killed': 'sum',


    }
    # Dataset has multiple columns starting with final, using list comprehension to loop through and using mean on all of them
    # Appends it to the dictionary aggregation rules
    final_stats = [col for col in numerical_columns if col.startswith('final_')]
    for col in final_stats:
        aggregation_rules[col] = 'mean'

    # Group the new data in two rows per game (one for each team)
    team_df = df_classic.groupby(['game_id', 'team_id']).agg(aggregation_rules).reset_index()

    # Grouping the game by the team ID.
    team1 = team_df[team_df['team_id'] == 100].add_prefix('t1_')
    team2 = team_df[team_df['team_id'] == 200].add_prefix('t2_')

    # Merging the two rows together with the game id
    merged_df = pd.merge(
        team1,
        team2,
        left_on='t1_game_id',
        right_on='t2_game_id',
        how='inner'
    )


    stats_to_diff = [col.replace('t1_', '') for col in team1.columns
                     if col not in ['t1_game_id', 't1_team_id', 't1_win', 't1_game_start_utc']]

    for stat in stats_to_diff:
        merged_df[f'{stat}_diff'] = merged_df[f't1_{stat}'] - merged_df[f't2_{stat}']

    # Decided to only get the diff columns with list comprehension.
    # Since there are only two teams the goal is to only look at team 1. Did they win and what was the difference in between the two teams
    X_columns = [col for col in merged_df.columns if col.endswith('_diff')]
    X = merged_df[X_columns]
    y = merged_df['t1_win']

    # Added a test to see that all was merged correctly
    test_passed = (merged_df['t1_game_id'] == merged_df['t2_game_id']).all()
    num_matches = len(merged_df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, test_passed, num_matches


# Cache is used to not rerun the grid search everytime
# False on show spinner because I don't want the run_grid_search to be shown but rather a customized message.
@st.cache_resource(show_spinner=False)
def run_grid_search(X_train, y_train, features_names):
    """Run GridSearch and save it in cache so it doesn't need to re-run everytime."""
    param_grid = {
        'max_depth': [10, 12, 15],
        'min_samples_split': [4, 5, 6],
        'n_estimators': [100, 150]
    }
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    return grid_search


def get_ml_results(df_classic, selected_features=None):
    """
    selected_features: If None, use all.
    Otherwise, use selected features (can be found in ml.py.)
    """
    X_train_full, X_test, y_train_full, y_test, test_passed, num_matches = prepare_ml_data(df_classic)

    # If selected features -> use only
    if selected_features:

        features_to_use = [f"{f}_diff" for f in selected_features if f"{f}_diff" in X_train_full.columns]
        X_train_full = X_train_full[features_to_use]
        X_test = X_test[features_to_use]

    # Split for validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full, y_train_full, test_size=0.25, random_state=42
    )

    # Träna modellen - feature_names ser till att cachen vet vilken modell som är vilken
    grid_search = run_grid_search(X_train, y_train, X_train.columns.tolist())
    best_rf = grid_search.best_estimator_

    # Accuracy
    val_acc = accuracy_score(y_val, best_rf.predict(X_val))
    test_acc = accuracy_score(y_test, best_rf.predict(X_test))

    importances = pd.DataFrame({
        'feature': X_train.columns,
        'importance': best_rf.feature_importances_ * 100
    }).sort_values(by='importance', ascending=False)



    results = {
        'val_acc': val_acc,
        'test_acc': test_acc,
        'best_params': grid_search.best_params_,
        'importances': importances,
        'data_check': test_passed,
        'num_matches': num_matches
    }

    # Figure for ml
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=importances.head(10), x='feature', y='importance', ax=ax, palette='viridis')

    for container in ax.containers:
        ax.bar_label(container, padding=5, fmt='%.2f%%')

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()

    return fig, results