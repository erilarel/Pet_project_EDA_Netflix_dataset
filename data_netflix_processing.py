import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('netflix_titles.csv')
df = data.copy()

# Exploratory data analysis

# print(data.head)
# print(data['country'].sample(5))
# print(data.columns)
# print(df.dtypes)
# print(df.shape)
# print(df.info())
# print(df.describe(include='all'))
# print(df.describe(include=['number']))
# print(df.describe(include=['object']))


# Missing

# missing = df.isna().sum()
# print(missing)

# percent_missing = (df.isna().sum() / len(df)) * 100
# print(percent_missing)


# Data cleaning

df['director'] = df['director'].fillna('Unknown')
df.drop(columns=['cast', 'description'], inplace=True)
df = df.drop_duplicates()

# Working

df['date_added'] = df['date_added'].str.strip()
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

# Metrics

total_films = len(df)
movies = (df['type'] == 'Movie').sum()
tv_shows = (df['type'] == 'TV Show').sum()

movies_by_year = df[df['type'] == 'Movie'].groupby('year_added').size()
tv_shows_by_year = df[df['type'] == 'TV Show'].groupby('year_added').size()

year_show = pd.concat([movies_by_year, tv_shows_by_year], axis=1)
year_show.columns = ['Movies', 'TV Shows']
year_show = year_show.fillna(0)
year_show = year_show[year_show.index >= 2015]

countries_count = df['country'].str.split(', ').explode().value_counts().count()
genres_count = df['listed_in'].str.split(', ').explode().value_counts().head(10)

ratings = df['rating'].value_counts().head(10)

content_by_month = df.groupby('month_added').size()
content_by_year = df.groupby('year_added').size()

print(countries_count)
# Visualisation 

plt.figure()
content_by_year.plot()
plt.title('Content added by year')

plt.figure()
countries_count.plot(kind='bar')
plt.title('Top countries')

plt.figure()
genres_count.plot(kind='bar')
plt.title('Top genres')

plt.figure()
ratings.plot(kind='bar')
plt.title('Ratings distribution')

plt.figure()
year_show.plot(kind='bar')
plt.title('Movies vs TV Shows by Year')
plt.xlabel('Year')
plt.ylabel('Number of titles')


# Saving

df.to_csv('netflix_cleaned.csv', index=False)