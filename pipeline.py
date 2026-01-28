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

    # Decided to create for minutes instead as it is easier for viewers to read.
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

#----------------------------A DF WITH ALL THE CLEANING (ONLY FULL GAME AND CLASSIC GAME MODE)-------------------------
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

    # Decided to create a descriptive label for by combining the champion name
    # with the sample size (total games). This allows the viewer to immediately gives both me and the viewer
    # good information on the win rate % and the spread of the top 10 and bottom 10.
    champion_stats['Name_with_Count'] = (
            champion_stats['Champion'] +
            " (" + champion_stats['Total Games'].astype(str) + ")"
    )

    top_10_wins = champion_stats.sort_values(by='Win Rate', ascending=False).head(10)
    bottom_10_wins = champion_stats.sort_values(by='Win Rate', ascending=False).tail(10)

    # Decided to add a dataframe later to further inspect the sample size and therefore
    # dropping the column Name_with_Count as it's already easy to view in a dataframe
    df_champion_drop = champion_stats.drop(columns=['Name_with_Count'])

    df_champions = df_champion_drop[['Champion', 'Wins', 'Win Rate', 'Total Games']].copy()

    df_champions = df_champions.sort_values(by='Total Games', ascending=False)

#-----------------------------------------GAME STATISTICS---------------------------------------------------

    df_duration = df_classic.groupby(['game_id'])[['game_duration', 'game_minutes']].first().reset_index()

    df_match_agg = df_classic.groupby('game_id').agg({
        'kills': 'sum',
        'summoner_level': 'mean',
        'game_minutes': 'mean'
    }).reset_index()


    df_match_agg.columns = ['game_id', 'total_match_kills', 'avg_summoner_level', 'game_minutes']

    # Decided to bin 'summoner_level' to analyze if player experience correlates with match duration.
    # The bins are strategically chosen to separate new/casual players from 'high-level'
    # veterans, aiming for balanced group sizes based on the dataset distribution.
    bins = [0, 300,700, 3000]
    labels = ['Low Level (0-300)', 'Mid level (301-700)', 'High Level (701+)']
    df_match_agg['level_group'] = pd.cut(df_match_agg['avg_summoner_level'], bins=bins, labels=labels)


    return df, df_filtered_time, mode_counts, stats, df_classic, top_10_wins, bottom_10_wins, df_champions, df_duration, df_match_agg


def graphs(stats, mode_counts, top_10_wins, bottom_10_wins, df_champions, df_duration, df_match_agg, df_classic):

#----------------------DATA CLEANING GRAPHS-------------------------------
    fig1, ax1 = plt.subplots(figsize=(8, 4))

    # Simple barplot to show how many games in the dataset exists in each group were focus will be on the matchtyp "Full Game"
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

    # Method for showing the actual data on top of the bars (number of games in each group)
    for i, count in enumerate(stats['Antal']):
        plt.text(i, count + 0.1, str(count), ha='center')

    fig2, ax2 = plt.subplots(figsize=(8, 4))

    # Same logic as the above mentioned one to show the different modes the data set contains
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

    # Using two barplots with two different ax to be shown next to eachother. This to show a first
    # view of how the win percentage is for the champs without taking other parameters into consideration.
    sns.barplot(
        data=top_10_wins,
        hue="Champion",
        x='Win Rate',
        y='Name_with_Count',
        ax=ax_top,
        palette='viridis',
        legend=False)
    ax_top.set_xlabel('Win Rate (%)')
    ax_top.set_ylabel('Champion + games played')
    ax_top.set_title('Tio bästa champions (2025)', fontsize=16)

    sns.barplot(
            data=bottom_10_wins,
            hue="Champion",
            x='Win Rate',
            y='Name_with_Count',
            ax=ax_bot,
            palette='magma',
            legend=False)


    ax_bot.set_ylabel('Champion + games played')
    ax_bot.set_title('Tio sämsta champions (2025)', fontsize=16)
    ax_bot.set_xlabel('Win Rate (%)')

    # Throughout many of the graphs this method is chosen to be able to display the actual percentage to help
    # the viewer see more clearly
    for ax in [ax_top, ax_bot]:
        # Add percentage labels to the end of each bar for immediate readability
        for container in ax.containers:
            ax.bar_label(container, padding=5, fmt='%.1f%%')

        # Expand the X-axis slightly to ensure the bar labels don't get cut off
        current_max = max(top_10_wins['Win Rate'].max(), bottom_10_wins['Win Rate'].max())
        ax.set_xlim(0, current_max + 15)


    plt.tight_layout()

    # Decision made to use scatterplot to see the distribution of the champions and ther played games vs winrate.
    # Helps the analysis to see patterns.
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

    # Using a regplot to visualize the correlation (trendline) between a champion's
    # popularity and their win rate. The idea is to help make it even clearer after seeing the scatterplot
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

    # A histogram is used to visualize the
    # distribution of match lengths. This helps identify the most common game
    # duration and the spread of the data (variance).
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

    # A boxplot is chosen to compare match duration across player level groups.
    # This visualization is superior to a simple bar chart because it displays
    # the median, spread (IQR), and outliers, revealing if more experienced
    # players tend to finish matches faster or more consistently.
    sns.boxplot(
        data=df_match_agg,
        x='level_group',
        y='game_minutes',
        palette='viridis',
        ax=ax_agg)
    ax_agg.set_title('Längden av en match baserat på spelarnas genomsnittliga level')
    ax_agg.set_xlabel('Level gruppering')
    ax_agg.set_ylabel('Minuter (Duration)')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig_agg


