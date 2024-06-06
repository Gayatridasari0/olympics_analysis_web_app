import numpy as np


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['NOC', 'Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
        'Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return country, years


def fetch_medal_tally(year, country, df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_tally
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_tally[medal_tally['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_tally[medal_tally['Year'] == year]
    else:
        temp_df = medal_tally[(medal_tally['Year'] == year) & (medal_tally['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


def data_over_time(df, col):
    data_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    data_over_time.sort_index()
    data_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return data_over_time


def most_successful_sport_wise(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Sport', 'region', 'count']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x


def most_successful_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    if (country != 'Overall'):
        temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Sport', 'count']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x


def year_wise_medal(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]
    final_df = temp_df.groupby(temp_df['Year']).count()['Medal'].reset_index()
    return final_df


def country_wise_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
                            inplace=True)
    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    new_df = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return new_df


def weight_vs_height(df, sport):
    df['Medal'].fillna('No Medal', inplace=True)
    temp_df = df
    if (sport != 'Overall'):
        temp_df = df[df['Sport'] == sport]
    return temp_df


def men_vs_women(df):
    df = df.drop_duplicates(subset=['Name', 'region'])
    men = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year',how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final
