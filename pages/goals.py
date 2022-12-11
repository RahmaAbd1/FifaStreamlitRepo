import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np 
from collections import Counter


st.set_page_config(layout="wide")


goals = pd.read_csv("goals.csv")

st.markdown("# Goals 🥅 ")
st.write(" Goals can sometimes be ambigious. To better determine what is or is not considered a goal, FIFA follows the [Laws of the Game](https://www.theifab.com/laws-of-the-game-documents/?language=all&year=2022%2F23), the rules of football that are annualy authorized by the International Football Association Board (IFAB). The IFAB states that goal is scored when the entire ball passes the goal line between the goalpost, and into the goalpost at the end of the pitch.")
st.write("***")



st.subheader(" Analysis of Goals over Time")

st.write("""Brazil, Italy, and Germany have won the world cup the most times. The amount of goals they have scored at each tournament can be analyzed.
- A gap in obervations over time during the 1940's was due to the World Cup tournaments being canceled due to WWI & II.
- Brazil & Germany are the top two countries in number of goals scored, with the German team growing better over time since 1990. """)

#Converting Date
goals['match_date'] = pd.to_datetime(goals['match_date'])
goals['Year'] = goals['match_date'].dt.year

#Combining West Germany with Germany
goals['team_name'].replace({'West Germany':'Germany'}, inplace=True)

#Observing only top three countries
team_name = ["Brazil", "Italy", "Germany"]
df_list = goals[goals.team_name.isin(team_name)]



#Grouping by year
df4 = df_list.groupby(['Year', "team_name"])['key_id'].count().reset_index()

team_name = ["Brazil", "Italy", "Germany"]
df_list2 = goals[goals.team_name.isin(team_name)]

col1, col2 = st.columns(2)
with col1:
    three = px.histogram(
        df_list2,
        x='match_date',
        title="Country Stages",
        color="team_name",
        log_x=False,
        log_y=False,
        #symbol='title',
        #markers=True,
        #width=800, 
        height=500,
        hover_name="team_name",
        hover_data=['team_name'])
    three.update_layout(barmode='group')
    st.plotly_chart(three)

with col2:
    #Plotting Scatterplot
    fig = px.line(df4, x="Year", y="key_id", title = "Number of Goals for the Top 3 Countries over the Years", height = 500, width=800,
    labels={
      "key_id": "Number of Goals", "team_name": "Team/Country",
           },
    color = "team_name"
    )
    st.plotly_chart(fig)


st.write("***")

st.subheader("When Do Goals Typically Occur?")
col3, col4 = st.columns(2)


with col3:
    st.write(""" A game of soccer is split into two halves of 45 minutes each with a halftime break at the end of the first 45 minute period. Extra time consists of two 15-minute periods added onto a game when the score is tied after the alloted 90 minutes of gametime. Stoppage time is also sometimes added to each extra time half based on time lost from substitutions, injuries, and other delays.
    - As expected, since this is the largest section of a game, the first and second half of the game is when a goal is typically scored.
    - Extra time & stoppage time may be a short amount of time, but a goal is sometimes scored. Since the first world cup, 64 goals during stoppage time at the end of the second half was scored. This is the last chance before the game ends to score a goal! """)

with col4: 
    bubbledf = goals.groupby(["match_period"])['goal_id'].count().reset_index()

    gb = px.bar(
        bubbledf,
        x='match_period',
        y ="goal_id",
        #title="Country Stages",
        log_x=False,
        log_y=False,
        #symbol='title',
        #markers=True,
        #width=800, 
        height=600,
        text = "goal_id",
        labels={
            "match_period": "Match Period", "goal_id": "Number of Goals"
               },
     hover_name="match_period",
     hover_data=['match_period', "goal_id"]
    )
    
    gb.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(gb)

st.write("***")


st.subheader ("Which players scored the most goals overall?")

col5, col6 = st.columns(2)

goals['given_name'].replace({'not applicable':'-'}, inplace=True)

goals['full_name'] = np.where(goals[['given_name', 'family_name']].eq('').any(axis=1),
                           goals['player_id'],
                           goals[['given_name', 'family_name']].apply(' '.join, axis=1))

counts = Counter(goals["full_name"])

goalnum = pd.DataFrame.from_records(counts.most_common(), columns=['full_name','counts'])


goalnumdf = goalnum.nlargest(10,'counts')

with col5:
    st.write(""" Since the first tournament in 1930, 1,298 footballers have scored goals in the World Cup final tournaments,[3] of whom just 98 have scored five or more.
    - Miroslav Klose (Germany) played in 24 matches in 4 tournaments, and scored 16 goals total.
    - Ronaldo (Brazil) played in 19 matches in 3 tournaments, and scored 16 goals total.
    - Gerd Müller (Germany) played in 13 matches in 2 tournaments, and scored 14 goals total. """)


with col6:
    num = px.bar(
        goalnumdf,
        x='full_name',
        y="counts",
        #title="Country Stages",
        log_x=False,
        log_y=False,
        #symbol='title',
        #markers=True,
        #width=800, 
        height=500,
        text = "counts",
        hover_name="full_name",
        hover_data=['counts']
    )
    
    num.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})

    st.plotly_chart(num)
