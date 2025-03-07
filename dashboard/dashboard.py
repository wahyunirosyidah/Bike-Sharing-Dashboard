import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import calendar
sns.set(style='dark')

def rentals_total(df):
    total_all = df['cnt'].sum()
    return total_all

def by_membership(df):
    total_casual = df['casual'].sum()
    total_registered = df['registered'].sum()
    return total_casual, total_registered

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


# Load Data
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

st.header('Bike Rentals Dashboard :bike:')

#Total Bike Rentals
total = rentals_total(day_df)
total_all = total
st.metric("Total Bike Rentals", value=total_all)

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/wahyunirosyidah/submission/main/dashboard/image.png")
    st.title("Everywhere, We Gowes!")

    st.caption('Copyright © Wahyuni Fajrin Rosyidah 2025')

#Peak Hours vs Off-Peak Hours
hourly_rentals = peak_hours(hour_df)
st.subheader('Peak vs. Off-Peak Hours')
plt.figure(figsize=(12, 6))
sns.barplot(x="hr", y="cnt", hue="Category", data=hourly_rentals, palette={"Peak Hour": "blue", "Off-Peak Hour": "red", "Normal Hour": "gray"})
plt.xlabel("Hour")
plt.ylabel("Number of Rentals")
plt.xticks(range(0, 24))
plt.legend(title="Category")
st.pyplot(plt)


# By Season
season_avg_rentals=by_season(hour_df)
st.subheader('Average Rentals by Season')
plt.figure(figsize=(12, 7))
plt.bar(season_avg_rentals['season_desc'], 
        season_avg_rentals['cnt'], 
        color=['blue'])

plt.xlabel('Season', fontsize=12)
plt.ylabel('Average Rentals (Unit)', fontsize=12)

plt.show()
st.pyplot(plt)


#Working Day, Holiday, Non-Working Non-Holiday
category_stats = day_category(day_df)
st.subheader('Working Day, Holiday, Non-Working Non-Holiday')
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
metrics = ['max', 'min', 'mean']
titles = ['Maximum Rentals', 'Minimum Rentals', 'Average Rentals']

for i, metric in enumerate(metrics):
    sns.barplot(data=category_stats, x='Category', y=metric, ax=ax[i], hue='Category', palette=['blue', 'gray', 'red'])
    ax[i].set_title(titles[i], fontsize=18)
    ax[i].set_ylabel('Number of Rentals (Unit)')
    ax[i].set_xlabel('')
    ax[i].tick_params(axis='x', rotation=45)
    
plt.tight_layout()
st.pyplot(plt)

#By Membership
total_casual, total_registered = by_membership(day_df)
st.subheader('User Category by Membership')
plt.figure(figsize=(7, 7))
plt.pie([total_casual, total_registered], 
        labels=['Casual Users', 'Registered Users'], 
        autopct='%1.1f%%', 
        colors=['red', 'blue'], 
        startangle=90, 
        explode=(0.05, 0),
        textprops={'fontsize': 14}  
)

plt.title("Casual vs. Registered Users", fontsize=16)
st.pyplot(plt)