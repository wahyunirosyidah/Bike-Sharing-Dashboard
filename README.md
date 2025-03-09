# Bike Sharing Dashboard 🚲

## 🚴 Project Overview

This project provides a Bike Sharing Dashboard that visualizes and analyzes bike rental patterns based on various factors such as time, season, working days, and weather conditions. The dashboard is built using Streamlit, Pandas, Seaborn, and Matplotlib.

## Features
- Total Rentals Analysis: Displays the total number of bike rentals within a selected time range.
- Peak vs. Off-Peak Hours: Categorizes hours into Peak, Off-Peak, and Normal based on rental frequency.
- Working Day & Holiday Analysis: Analyzes bike rentals on working days, holidays, and non-working non-holidays.
- Rentals by Windspeed: Groups rentals based on different windspeed levels.
- Rentals by Time Category: Classifies bike rentals into Late Night, Morning, Afternoon, Evening, and Night categories.
- Seasonal Trends: Displays average bike rentals across different seasons.

## Dataset
The project uses the Bike Sharing Dataset, which contains:
- Hourly Data (hour.csv)
- Daily Data (day.csv)

## Installation & Setup

1️⃣ Clone the Repository
```
git clone https://github.com/username/bike-sharing-dashboard.git
cd bike-sharing-dashboard
```
2️⃣ Install Dependencies
```
pip install pandas matplotlib seaborn streamlit
```
3️⃣ Run the Dashboard
```
streamlit run dashboard/dashboard.py
```
## Dashboard Deploy
[Dashboard](https://wahyunirosyidah-bike-sharing-dashboard.streamlit.app/)

## Technologies Used
- Python 
- Pandas 
- Matplotlib 
- Seaborn 
- Streamlit 
- Jupyter Notebook 

## Results & Insights
- Bike rentals are highest during Peak Hours (evening and morning rush hours).
- The highest rental counts occur in Fall and Summer, while Winter has the lowest.
- Windspeed affects rentals, with low windspeed conditions leading to higher rentals.
- Rentals are higher on working days compared to holidays.
  
![image](https://github.com/user-attachments/assets/d9b47ead-6a9e-4d76-a88b-0c716fc3068e)
![image](https://github.com/user-attachments/assets/77a7883e-6a24-4bee-860a-6e1931c86868)
![image](https://github.com/user-attachments/assets/175c86b5-a5a4-43b9-a929-893a7e588424)
![image](https://github.com/user-attachments/assets/e81a2ba1-6696-44f8-bdef-dbbf00c77aaf)
![image](https://github.com/user-attachments/assets/eb550603-a6a8-4e4e-be3b-2fa4b3d58840)


