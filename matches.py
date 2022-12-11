import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np 

matches = pd.read_csv('matches.csv')
tnm = pd.read_csv('tournaments.csv')
play = pd.read_csv('players.csv')



stage_categories = ['group stage','second group stage', 'round of 16',
'quarter-finals', 'semi-finals','third-place match', 'final round',
'final']

matches["stage_name"] = pd.Categorical(matches["stage_name"], categories=stage_categories)

matches.sort_values(by="stage_name", inplace=True)

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.markdown("# Matches 🏟 ")
st.sidebar.markdown("# Matches 🏟")



st.markdown(
    "The FIFA World Cup is an international football (or soccer depending on what country) championship competition that occurs every four years since 1930. 21 final tournaments have been held, and 79 teams all over the world have competed. The World Cup is the most widely viewed and followed single sporting event in the world. ")

st.markdown('***')

st.subheader ("Which countries/teams have won the world cup the most?")

col1, col2 = st.columns((1,2))
with col1:
    st.markdown(
        """
        Since 1930, there has been 21 completed tournaments (not including the Qatar 2022 World Cup.) Over these years, there have been certain countries dominating the tournaments. 
        - Brazil has won the world cup five times in 1958, 1962, 1970, 1994, and 2002.
        - Italy has won the world cup four times in 1934, 1938, 1982, and 2006.
        - Germany initially participated in the world cup only as West Germany, with their three victories occuring in 1954, 1974, and 1990. But, after the German reunification in 1990, West Germany was no more, and afterwards participated in the world cup as Germany. Then, in Germany won the world cup in 2014, making this unified Germany's first world cup win. 
        """)

with col2:
    z = px.histogram(
        tnm,
        x='winner',
        log_x=False,
        log_y=False,
        #symbol='title',
        #markers=True,
        #width=900, 
        height=500,
        labels={
         "winner": "Winner of Tournament", "count": "Number of Tournament Wins"
              },
     hover_name="winner",
        hover_data=['host_country', "winner"]
    )
    
    z.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(z)


st.markdown("***")

st.subheader(" How far have countries gotten to winning?")
st.markdown(
"""
Six qualifying tournaments are held to determine which country will participate in the final tournament. The left barcharts the distribution of stages for the away teams, while the right barchart shows the home teams. The charts shows that most countries have only qualified for the groupstage.
- On average, countries play better and advance in stages more often when they are playing as home compared to playing as away.
"""
)


col3, col4 = st.columns((2))

with col3:
    y = px.histogram(
        matches,
        x='home_team_name',
        title="Country (HOME) Stages",
        log_x=False,
        log_y=False,
        #symbol='title',
        #markers=True,
        width=800, 
        height=600,
        color='stage_name',
        hover_name='stage_name',
     hover_data=['home_team_name','stage_name'])
    y.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(y)

with col4:
    x = px.histogram(
        matches,
        x='away_team_name',
        title="Country (AWAY) Stages",
        log_x=False,
        log_y=False,
        #symbol='title',
        #markers=True,
        #width=800, 
        height=600,
        color='stage_name',
        hover_name='stage_name',
     hover_data=['away_team_name','stage_name'])
    x.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(x)

st.markdown('***')

st.subheader("Do teams perform better when playing as home or away?")
st.markdown("""The previous barcharts have shown that most countries play better when playing as home compared to away. Typically, in a regular football match, the home team has home field advantage (playing in their own stadium), while the away team does not. But, in in the case of the world cup tournament, the position is randomly determined.
- Since the first tournament in 1930, while there should not be an advantage with a team playing as home, teams still perform much better when playing as home.
- The line chart also includes any matches that resulted as a "draw", when both teams score the same amount of goals. Over the years, the occurances of draws have increased.   """)






matches["match_date"]= pd.to_datetime(matches["match_date"])
matches['match_date'] = matches['match_date'].dt.year

matches2 = matches.groupby(['match_date', 'result'])['match_id'].count().reset_index(name='counts')

fig = px.line(matches2, x="match_date", y="counts", width = 900, height= 600, labels= {"counts" : "# of Goals", "match_date" : "Year"}, color='result')
st.plotly_chart(fig)

st.markdown('***')


f = play.nlargest(15,'count_tournaments')
f['full_name'] = np.where(f[['given_name', 'family_name']].eq('').any(axis=1),
                           f['player_id'],
                           f[['given_name', 'family_name']].apply(' '.join, axis=1))

st.subheader ("Which players have played at the most tournaments?")

col5, col6 = st.columns(2)

with col5:
    st.markdown(""" As the World Cup only occurs once every four years, not many players get the opportunity to participate many times. However, there are players that have gotten the opportunity to play at the World Cup multiple times.
- While there are many more players that played at 4 different tournaments, only the first 15 observations are shown.    
- Lothar Matthäus (Germay), Rafael Márquez (Mexico), and Antonio Carbajal (Mexico) made it to 5 different World Cup tournaments. Gianluigi Buffon (Italy) also made it to 5 tournaments, but played in the Italian squad for 4 tournaments, as he was benched in the 1998 tournament.
""")

with col6:

    b = px.bar(
        f,
        x='player_id',
        y ="count_tournaments",
        #title="Country Stages",
        log_x=False,
        log_y=False,
        #symbol='title',
        #markers=True,
        #width=800, 
        height=500,
        labels={
        "count_tournaments": "# of Tournaments Attended"
              },
        text = "full_name",
        hover_name="full_name",
        hover_data=['player_id']
    )
    st.plotly_chart(b)

st.markdown('***')

def goals():
    st.markdown("# Page 2 ... ")
    st.sidebar.markdown("# Page 2 ❄️")

def page3():
    st.markdown("# Page 3 ....")
    st.sidebar.markdown("# Page 3 ❄️")
