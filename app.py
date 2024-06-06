import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import helper
import preprocessor
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff

df = pd.read_csv('resources/athlete_events.csv')
region_df = pd.read_csv('resources/noc_regions.csv')

df = preprocessor.preprocess(df, region_df)
st.sidebar.title('Olympics Analysis')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlethe-wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    country, years = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select year', years)
    selected_country = st.sidebar.selectbox('Select country', country)
    medal_tally = helper.fetch_medal_tally(selected_year, selected_country, df)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Meal tally in ' + str(selected_year) + " Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + 'Overall performance')
    else:
        st.title(selected_country + " perfromance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

elif user_menu == 'Overall Analysis':
    st.title("Top Statistics")
    editions = df['Year'].unique().shape[0] - 1  #1906 is not considered by uno
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['ID'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    nations_over_time = helper.data_over_time(df, col="region")
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, col="Event")
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, col="Name")
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No of Events over time(Every Sport)")
    x = df.drop_duplicates(['Year','Sport','Event'])
    fig, ax = plt.subplots(figsize=(30, 30))
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title('Most successful Athlete')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport',sport_list)
    x = helper.most_successful_sport_wise(df, selected_sport)
    st.table(x)
elif user_menu == 'Country-wise Analysis':
    st.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0,'Overall')
    selected_country = st.selectbox('Select a country', country_list)
    country_df = helper.year_wise_medal(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.title('Medals over the years')
    st.plotly_chart(fig)

    st.title(selected_country+ " excels in the following sports")
    pt = helper.country_wise_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(30,30))
    ax = sns.heatmap(pt,annot = True)
    st.pyplot(fig)

    st.title('Top 10 athletes of '+selected_country)
    top_10_df = helper.most_successful_country_wise(df,selected_country)
    st.table(top_10_df)
elif user_menu == 'Athlethe-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)
    x = []
    names = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        sport_df = athlete_df[athlete_df['Sport']==sport]
        x.append(sport_df[sport_df['Medal'] == 'Gold']['Age'].dropna())
        names.append(sport)

    fig = ff.create_distplot(x, names, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    st.title('Weight vs Height')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a sport', sport_list)

    x = helper.weight_vs_height(athlete_df,selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(athlete_df,x=x['Weight'],y=x['Height'],hue = x['Medal'], style=x['Sex'], s=100)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    x = helper.men_vs_women(athlete_df)
    fig = px.line(x, 'Year',['Male','Female'] )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


