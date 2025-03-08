import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import calendar
sns.set(style='dark')

def rentals_total(df):
    total_all = df['cnt'].sum()
    return total_all

def day_category(df):
    df['Category'] = df.apply(lambda x: 
                                  'Working Day' if x['workingday'] == 1 else 
                                  'Holiday' if x['holiday'] == 1 else 
                                  'Non-Working Non-Holiday', axis=1)
    category_stats = df.groupby('Category')['cnt'].agg(['max', 'min', 'mean']).reset_index()
    return category_stats

def peak_hours(df):
    hourly_rentals = df.groupby("hr")["cnt"].sum().reset_index()

    q75 = hourly_rentals["cnt"].quantile(0.75) 
    q25 = hourly_rentals["cnt"].quantile(0.25) 

    hourly_rentals["Category"] = hourly_rentals["cnt"].apply(
        lambda x: "Peak Hour" if x >= q75 else ("Off-Peak Hour" if x <= q25 else "Normal Hour")
    )

    hourly_rentals = hourly_rentals.sort_values(by="cnt", ascending=False)
    return hourly_rentals

def by_season(df):
    season_conditions = {
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    }

    season_avg_rentals = df.groupby('season')['cnt'].mean().reset_index()
    season_avg_rentals['season_desc'] = season_avg_rentals['season'].map(season_conditions)
    return season_avg_rentals

def by_weather(df):
    def categorize_windspeed(wind):
        if wind < 0.25:
            return 'Low'
        elif wind < 0.40:
            return 'Medium'
        else:
            return 'High'

    hour_df['windspeed_category'] = hour_df['windspeed'].apply(categorize_windspeed)
    windspeed_stats = hour_df.groupby('windspeed_category')['cnt'].agg(['mean', 'max', 'min', 'std'])
    windspeed_stats = windspeed_stats.sort_values(by='mean', ascending=False)
    return windspeed_stats

#by Time Category
def by_timecategory(df):
    
    batas = [0, 5, 11, 15, 19, 23]  
    labels = ['Dini Hari', 'Pagi', 'Siang', 'Sore', 'Malam']

    hour_df['time_bin'] = pd.cut(hour_df['hr'], bins=batas, labels=labels, include_lowest=True)
    time_category = hour_df.groupby('time_bin')['cnt'].sum().reset_index()
    time_category = time_category.sort_values(by='cnt', ascending=False)

    return time_category




# Load Data
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

# Convert 'dteday' to datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/wahyunirosyidah/submission/main/dashboard/image.png")
    st.title("Everywhere, We Gowes!")
    
    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal
filtered_day_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]
filtered_hour_df = hour_df.merge(filtered_day_df[['dteday', 'instant']], on='instant')

# Fungsi untuk menghitung total rentals
def rentals_total(df):
    return df['cnt'].sum()

# Total Rentals
st.header('Bike Rentals Dashboard :bike:')
total_all = rentals_total(filtered_day_df)
st.metric("Total Bike Rentals", value=total_all)

# Peak vs. Off-Peak Hours
def peak_hours(df):
    hourly_rentals = df.groupby("hr")["cnt"].sum().reset_index()
    q75 = hourly_rentals["cnt"].quantile(0.75)
    q25 = hourly_rentals["cnt"].quantile(0.25)
    
    hourly_rentals["Category"] = hourly_rentals["cnt"].apply(
        lambda x: "Peak Hour" if x >= q75 else ("Off-Peak Hour" if x <= q25 else "Normal Hour")
    )
    return hourly_rentals

st.subheader('Peak vs. Off-Peak Hours')
hourly_rentals = peak_hours(filtered_hour_df)
plt.figure(figsize=(12, 6))
sns.barplot(x="hr", y="cnt", hue="Category", data=hourly_rentals, 
            palette={"Peak Hour": "blue", "Off-Peak Hour": "red", "Normal Hour": "gray"})
plt.xlabel("Hour")
plt.ylabel("Number of Rentals")
plt.xticks(range(0, 24))
plt.legend(title="Category")
st.pyplot(plt)


# st.header('Bike Rentals Dashboard :bike:')

# #Total Bike Rentals
# total = rentals_total(day_df)
# total_all = total
# st.metric("Total Bike Rentals", value=total_all)

# # Konversi kolom tanggal
# day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# # Sidebar - Filter Rentang Waktu
# min_date = day_df["dteday"].min()
# max_date = day_df["dteday"].max()


# # Sidebar
# with st.sidebar:
#     st.image("https://raw.githubusercontent.com/wahyunirosyidah/submission/main/dashboard/image.png")
#     st.title("Everywhere, We Gowes!")
#     start_date, end_date = st.date_input(
#         label='Rentang Waktu',
#         min_value=min_date,
#         max_value=max_date,
#         value=[min_date, max_date]
#     )
    
#     st.caption('Copyright © Wahyuni Fajrin Rosyidah 2025')

# # Filter Data
# filtered_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]


# #Peak Hours vs Off-Peak Hours
# hourly_rentals = peak_hours(hour_df)
# st.subheader('Peak vs. Off-Peak Hours')
# plt.figure(figsize=(12, 6))
# sns.barplot(x="hr", y="cnt", hue="Category", data=hourly_rentals, palette={"Peak Hour": "blue", "Off-Peak Hour": "red", "Normal Hour": "gray"})
# plt.xlabel("Hour")
# plt.ylabel("Number of Rentals")
# plt.xticks(range(0, 24))
# plt.legend(title="Category")
# st.pyplot(plt)


# # By Season
# season_avg_rentals=by_season(hour_df)
# st.subheader('Average Rentals by Season')
# plt.figure(figsize=(12, 7))
# max_value = season_avg_rentals['cnt'].max()
# colors = ['blue' if x == max_value else 'gray' for x in season_avg_rentals['cnt']]

# plt.bar(season_avg_rentals['season_desc'], 
#         season_avg_rentals['cnt'], 
#         color=colors)

# plt.title('Average Rentals by Season', fontsize=14)
# plt.xlabel('Season', fontsize=12)
# plt.ylabel('Average Rentals (Unit)', fontsize=12)
# st.pyplot(plt)


# #Working Day, Holiday, Non-Working Non-Holiday
# category_stats = day_category(day_df)
# st.subheader('Working Day, Holiday, Non-Working Non-Holiday')
# fig, ax = plt.subplots(1, 3, figsize=(15, 5))
# metrics = ['max', 'min', 'mean']
# titles = ['Maximum Rentals', 'Minimum Rentals', 'Average Rentals']
# for i, metric in enumerate(metrics):
#     max_category = category_stats.loc[category_stats[metric].idxmax(), 'Category']
#     colors = ['gray' if cat != max_category else 'blue' for cat in category_stats['Category']]
#     sns.barplot(data=category_stats, x='Category', y=metric, ax=ax[i], palette=colors)
#     ax[i].set_title(titles[i])
#     ax[i].set_ylabel('Number of Rentals (Unit)')
#     ax[i].set_xlabel('')
#     ax[i].tick_params(axis='x', rotation=45)
    
# plt.tight_layout()
# st.pyplot(plt)

# #by Windspeed
# weather_category=by_weather(hour_df)
# st.subheader('Average Rentals by Windspeed')
# plt.figure(figsize=(10, 5))
# max_category = weather_category['mean'].idxmax()
# colors = ["blue" if cat == max_category else "gray" for cat in weather_category.index]
# sns.barplot(x=weather_category.index, y=weather_category['mean'], palette=colors)
# plt.xlabel("Windspeed Category", fontsize=12)
# plt.ylabel("Average Rentals (Unit)", fontsize=12)
# st.pyplot(plt)

# #by time category
# time_category=by_timecategory(hour_df)
# st.subheader('Bike Rentals by Time Category')
# plt.figure(figsize=(10, 6))

# max_index = time_category['cnt'].idxmax()  

# colors = ['blue' if i == max_index else 'gray' for i in range(len(time_category))]

# bar_plot = sns.barplot(x='time_bin', 
#                        y='cnt', 
#                        data=time_category, 
#                        palette=colors)

# plt.title('Bike Rentals by Time Category')
# plt.xlabel('Time Category')
# plt.ylabel('Number of Rentals (Unit)')

# plt.ticklabel_format(style='plain', axis='y')

# st.pyplot(plt)