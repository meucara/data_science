import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

"""This page retrieves data, cleans what is necessary for the analysis and handles the graphs as a function to be able to
call in the streamlit pages files to keep it cleaner"""



def get_cleaned_data():
    """This function is called get cleaned data as the first stage
    was an excel file with a CSV in it. To be able to run it faster the CSV file was saved in project and this function
    retrieves the file"""
    df = pd.read_csv('league_data_fast.csv')


    def classify_game(duration):
        """Used to find duration of game as the analysis will only be interesting to focus on games that
        were considered 'Full Game' (meaning it was probably not containing someone leaving directly or early in game)"""
        if duration <= 210:
            return 'Remake'
        elif duration <= 900:
            return 'Early Surrender'
        else:
            return 'Full Game'

#-----------------------CHECKING GAME TYPE---------------------------------
    # Using the function and creating a new column for the game_type
    df['game_type'] = df['game_duration'].apply(classify_game)

    df['game_minutes'] = df['game_duration'] / 60

    # New DF with only unique games. Original DF contains 10 rows for each game(for every player in game).
    df_unique = df.drop_duplicates(subset='game_id')
    stats = df_unique['game_type'].value_counts().reset_index()
    stats.columns = ['Matchtyp', 'Antal']

    stats['Total'] = stats['Antal'].agg(lambda x: sum(x))

# -----------------------FILTERING AWAY "BAD DATA"---------------------------------
    df_filtered_time = df[df['game_duration'] > 900]

# ----------------------------CHECKING GAME MODE -------------------------------
    # Used to showcase the different game modes and how many belongs in every category to show why this is needed to be dropped.
    df_unique_matches = df_filtered_time.drop_duplicates(subset='game_id')

    mode_counts = df_unique_matches['game_mode'].value_counts().reset_index()
    mode_counts.columns = ['Game Mode', 'Antal']
    mode_counts['Total'] = mode_counts['Antal'].agg(lambda x: sum(x))

#----------------------------A DF WITH ALL THE CLEANING (ONLY FULL GAME AND CLASSIC GAME MODE-------------------------
    df_classic = df_filtered_time[df_filtered_time['game_mode'] == 'CLASSIC'].copy()

#-----------------------------CHAMPION STATISTICS--------------------------------------
    # Data used for the champions.py map and in the graphs below to showcase champion statistics
    df_winners = df_classic[df_classic['win'] == True]

    champion_wins = df_winners['champion_name'].value_counts().reset_index()
    champion_wins.columns = ['Champion', 'Wins']

    total_played = df_classic['champion_name'].value_counts().reset_index()
    total_played.columns = ['Champion', 'Total Games']

    champion_stats = pd.merge(champion_wins, total_played, on='Champion')
    champion_stats['Win Rate'] = (champion_stats['Wins'] / champion_stats['Total Games'] * 100).round(2)

    champion_stats['Name_with_Count'] = (
            champion_stats['Champion'] +
            " (" + champion_stats['Total Games'].astype(str) + ")"
    )

    top_10_wins = champion_stats.sort_values(by='Win Rate', ascending=False).head(10)
    bottom_10_wins = champion_stats.sort_values(by='Win Rate', ascending=False).tail(10)

    df_champion_drop = champion_stats.drop(columns=['Name_with_Count'])

    df_champions = df_champion_drop[['Champion', 'Wins', 'Win Rate', 'Total Games']].copy()


    df_champions = df_champions.sort_values(by='Total Games', ascending=False)

    df_duration = df_classic.groupby(['game_id'])[['game_duration', 'game_minutes']].first().reset_index()

    df_match_agg = df_classic.groupby('game_id').agg({
        'kills': 'sum',
        'summoner_level': 'mean',
        'game_minutes': 'mean'
    }).reset_index()


    df_match_agg.columns = ['game_id', 'total_match_kills', 'avg_summoner_level', 'game_minutes']

    # Bins is taken here from the median of the summoner lvl of the players in the data.
    # The summoner level per person ranges from 0 - 2000 +.
    # For the analysis the importance was to find a balance in the groups and a way of highlighting the high level ones.
    # The developers Riot probably have some sort of matchmaking system to not get to high differences and this categories
    # tries to still find the highest ones.
    bins = [0, 300,700, 3000]
    labels = ['Low Level (0-385)', 'Mid level (386-700)', 'High Level (701+)']
    df_match_agg['level_group'] = pd.cut(df_match_agg['avg_summoner_level'], bins=bins, labels=labels)





    return df, df_filtered_time, mode_counts, stats, df_classic, top_10_wins, bottom_10_wins, df_champions, df_duration, df_match_agg


def graphs(stats, mode_counts, top_10_wins, bottom_10_wins, df_champions, df_duration, df_match_agg, df_classic):

#----------------------DATA CLEANING GRAPHS-------------------------------
    fig1, ax1 = plt.subplots(figsize=(8, 4))

    sns.barplot(
        data=stats,
        x='Matchtyp',
        y='Antal',
        ax=ax1,
        palette='viridis'
    )


    ax1.set_title('Fördelning av matcher', fontsize=16)
    ax1.set_xlabel('Typ av match', fontsize=12)
    ax1.set_ylabel('Antal matcher', fontsize=12)

    for i, count in enumerate(stats['Antal']):
        plt.text(i, count + 0.1, str(count), ha='center')

    fig2, ax2 = plt.subplots(figsize=(8, 4))

    sns.barplot(
        data=mode_counts,
        x='Game Mode',
        y='Antal',
        ax=ax2,
        palette='viridis'
    )


    ax2.set_title('Fördelning av matcher', fontsize=16)
    ax2.set_xlabel('Typ av match', fontsize=12)
    ax2.set_ylabel('Antal matcher', fontsize=12)

    for i, count in enumerate(mode_counts['Antal']):
        plt.text(i, count + 0.1, str(count), ha='center')



#--------------------------CHAMPION GRAPHS----------------------------
    fig3, (ax_top, ax_bot) = plt.subplots(1, 2, figsize=(13, 4))
    sns.barplot(
        data=top_10_wins,
        hue="Champion",
        x='Win Rate',
        y='Name_with_Count',
        ax=ax_top,
        palette='viridis',
        legend=False)
    ax_top.set(xlabel='Win Rate (%)')
    ax_top.set_ylabel('Champion + games played')

    for container in ax_top.containers:
        ax_top.bar_label(container, padding=5, fmt='%.1f%%')

    plt.xlim(0, top_10_wins['Win Rate'].max() + 10)

    ax_top.set_title('Tio bästa champions (2025)', fontsize=16)

    sns.barplot(
            data=bottom_10_wins,
            hue="Champion",
            x='Win Rate',
            y='Name_with_Count',
            ax=ax_bot,
            palette='magma',
            legend=False)

    ax_bot.set(xlabel='Win Rate (%)')
    ax_bot.set_ylabel('Champion + games played')

    ax_bot.set_title('Tio sämsta champions (2025)', fontsize=16)
    ax_bot.set_xlabel('Win Rate (%)')


    for container in ax_bot.containers:
        ax_bot.bar_label(container, padding=5, fmt='%.1f%%')

    plt.tight_layout()


    fig4, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_champions,
        x='Total Games',
        y='Win Rate',
        size='Total Games',
        ax=ax3
    )


    ax3.set_title('Samband mellan antal spelade matcher och vinstprocent')
    ax3.set_xlabel('Totalt antal matcher (Popularitet)')
    ax3.set_ylabel('Vinstprocent (%)')

    fig5, ax4 = plt.subplots(figsize=(10, 6))


    sns.regplot(
        data=df_champions,
        x='Total Games',
        y='Win Rate',
        line_kws={'color':'red'},    # Red line for visuals
        ax=ax4
    )

    ax4.set_title('Trendlinje för Vinstprocent baserat på antal matcher')
    ax4.set_xlabel('Totalt antal matcher (Popularitet)')
    ax4.set_ylabel('Vinstprocent (%)')

#--------------------------------Game statistic graphs----------------------------------------
    fig6, ax5 = plt.subplots(figsize=(10, 6))


    sns.histplot(
        data=df_duration,
        x='game_minutes',
        bins=30,
        kde=True,
        ax=ax5,
        color='skyblue')




    ax5.set_title('Fördelning av matchlängd (Classic 5v5)')
    ax5.set_xlabel('Minuter (Duration)')
    ax5.set_ylabel('Antal matcher')


    fig_agg, ax_agg = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=df_match_agg,
        x='level_group',
        y='game_minutes',
        palette='viridis',
        ax=ax_agg)
    ax_agg.set_title('Längden av en match baserat på spelarnas genomsnittliga level')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig_agg


