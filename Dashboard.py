import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

#This will be additional analysis from our work on deepnote. Here, we will load in all the previous CSV's we have used, and will create a dashboard graph to compare the correlation between Expected Wins and Rushing/Passing Attempts

advanced_passing_air_yards_df = pd.read_csv("Passing CSV 1.csv", header=1)
advanced_passing_air_yards_df = advanced_passing_air_yards_df.rename(columns={'Cmp': 'Passing Cmps', 'Att': 'Passing Attempts', 'Yds': 'Passing Yards', 'IAY': 'Intended Air Yards', 'IAY/PA': 'Intended Air Yards Per Attempt', 'CAY': 'Completed Air Yards', 'CAY/Cmp': 'Completed Air Yards Per Cmp', 'CAY/PA': 'Completed Air Yards Per Attempt', 'YAC': 'Passing YAC'})
remove_columns = ['G']
advanced_passing_air_yards_df = advanced_passing_air_yards_df.drop(remove_columns, axis=1)

advanced_passing_accuracy_df = pd.read_csv("Passing CSV 2.csv", header=1)
advanced_passing_accuracy_df = advanced_passing_accuracy_df.rename(columns={'Bats': 'Passes Batted', 'ThAwy': 'Passes Thrown Away', 'BadTh': 'Bad Throws', 'OnTgt': 'Passes On Target'})
remove_columns2 = ['G', 'Cmp', 'Att', 'Yds']
advanced_passing_accuracy_df = advanced_passing_accuracy_df.drop(remove_columns2, axis=1)

advanced_rushing_df = pd.read_csv("Rushing CSV 1.csv", header=0)
remove_columns3 = ['G']
advanced_rushing_df = advanced_rushing_df.rename(columns={'Att': 'Rushing Attempts', 'Yds': 'Rushing Yds', '1D': 'Rushing Yards', 'YBC': 'Rushing YBC', 'YAC': 'Rushing YAC', 'BrkTkl': 'Rushing BrkTkl', 'Att/Br': 'Attempts Per BrkTkl'})
advanced_rushing_df = advanced_rushing_df.drop(remove_columns3, axis=1)

advanced_receiving_df = pd.read_csv("Receiving CSV 1.csv", header=0)
advanced_receiving_df = advanced_receiving_df.rename(columns={'Yds':'Receiving Yards', 'TD':'Receiving TDs', '1D': 'Receiving 1Ds', 'YBC': 'Receiving YBC', 'BrkTkl': 'Receiving BrkTkl', 'Rec/Br': 'Receptions Per BrkTkl'})
remove_columns4 = ['G', 'ADOT', 'Int', 'Rat']
advanced_receiving_df = advanced_receiving_df.drop(remove_columns4, axis=1)

advanced_defense_df = pd.read_csv("Defense CSV 1.csv", header=0)
advanced_defense_df = advanced_defense_df.rename(columns={'Att': 'Opponents Attempts', 'Cmp': 'Opponents Cmps', 'Yds': 'Opponents Yards', 'TD': 'Opponents TDs', 'DADOT': 'Average Depth of Target', 'Air': 'Air Yards Allowed', 'YAC': 'YAC Allowed', 'Bltz': 'Blitzes', 'Bltz%': 'Blitz%', 'Hrry': 'QB Hurries', 'Hrry%': 'QB Hurry %', 'QBKD': 'QB Knockdowns', 'QBKD%': 'QB Knockdown%', 'Sk': 'Sacks', 'Prss': 'QB Pressures', 'Prss%': 'QB Pressure%', 'MTkl': 'Missed Tackles'})
remove_columns5 = ['G']
advanced_defense_df = advanced_defense_df.drop(remove_columns5, axis=1)

afc_csv = pd.read_csv('AFC.csv', header=0)
afc_csv = afc_csv.rename(columns={'W': 'Wins', 'L': 'Losses', 'T': 'Ties', 'W-L%': 'Win %', 'PF': 'Points For', 'PA': 'Points Against', 'PD': 'Point Differential', 'MoV': 'Average Margin of Victory', 'SoS': 'Strength of Schedule', 'SRS': 'Simple Rating System', 'OSRS': 'Offensive Simple Rating System', 'DSRS': 'Defensive Simple rating System'})

nfc_csv = pd.read_csv('NFC.csv', header=0)
nfc_csv = nfc_csv.rename(columns={'W': 'Wins', 'L': 'Losses', 'T': 'Ties', 'W-L%': 'Win %', 'PF': 'Points For', 'PA': 'Points Against', 'PD': 'Point Differential', 'MoV': 'Average Margin of Victory', 'SoS': 'Strength of Schedule', 'SRS': 'Simple Rating System', 'OSRS': 'Offensive Simple Rating System', 'DSRS': 'Defensive Simple rating System'})

#Now, we combine the dataframes into one big dataframe with all the teams and statistics.

both_conferences_df = pd.concat([afc_csv, nfc_csv], ignore_index=True)


advanced_passing_df = pd.merge(advanced_passing_air_yards_df, advanced_passing_accuracy_df, on='Tm')
advanced_passing_and_rushing_df = pd.merge(advanced_passing_df, advanced_rushing_df)
advanced_offensive_df = pd.merge(advanced_passing_and_rushing_df, advanced_receiving_df, on='Tm')
all_advanced_stats_df = pd.merge(advanced_offensive_df, advanced_defense_df, on='Tm')

main_football_df = pd.merge(both_conferences_df, all_advanced_stats_df, on='Tm')
main_football_df = main_football_df.rename(columns={'Bad%': 'Bad Throw %', 'Rushing Yards': 'Rushing Yards Per Game', 'Drop%_y': 'Drop %'})
remove_columns6 = ['Drops']
main_football_df = main_football_df.drop(remove_columns6, axis=1)

#We add in an expected wins column
expected_wins = (main_football_df['Points For']**(2.37) / ((main_football_df['Points For']**2.37) + (main_football_df['Points Against']**2.37)))
expected_wins = expected_wins*16
main_football_df['Expected Wins'] = expected_wins


#Finally, we create a scatterplot that shows the correlation between Expected Wins and Rushing Attempts and the lack of correlation between Pass Attempts and Expected Wins
fig, ax = plt.subplots()
ax.set_title("Correlation between Expecting Wins & Rushing/Passing Attempts?")
ax.set_ylabel("Number of Rushing/Passing Attempts")
ax.set_xlabel("Number of Expected Wins")
ax.scatter(main_football_df['Expected Wins'], main_football_df['Passing Attempts'], color='red', label='Passing Attempts')
ax.scatter(main_football_df['Expected Wins'], main_football_df['Rushing Attempts'], color='blue', label='Rushing Attempts')
ax.legend(loc="upper right")
st.pyplot(fig)

