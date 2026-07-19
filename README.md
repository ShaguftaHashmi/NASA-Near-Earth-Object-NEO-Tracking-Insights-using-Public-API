# NASA-Near-Earth-Object-NEO-Tracking-Insights-using-Public-API

## 📌 Project Overview

The **NASA Near-Earth Object (NEO) Tracker** is a data analytics dashboard developed using **Python, MySQL, and Streamlit**. The application fetches asteroid data from NASA's NeoWs API, stores it in a MySQL database, performs SQL-based analysis, and provides an interactive dashboard for filtering and visualizing asteroid information.

---

## 🎯 Objectives

- Fetch Near-Earth Object (NEO) data from NASA's API.
- Store asteroid and close approach information in a MySQL database.
- Perform SQL analysis on asteroid data.
- Build an interactive Streamlit dashboard.
- Enable filtering and visualization of asteroid information.

---

## 🛠️ Tech Stack

- Python
- Streamlit
- MySQL
- MySQL Connector (mysql.connector)
- Pandas
- NASA NeoWs API

---

## 📂 Project Structure

```
NASA_Asteroid_Tracker/
│
├── app.py                 # Streamlit Dashboard
├── fetch_data.py          # Fetch data from NASA API
├── database.py            # MySQL connection
├── create_tables.py       # Create MySQL tables
├── insert_data.py         # Insert API data into MySQL
├── requirements.txt
├── README.md
```

---

## 🗄️ Database Schema

### Table 1: asteroids

| Column |
|----------|
| id |
| name |
| absolute_magnitude_h |
| estimated_diameter_min_km |
| estimated_diameter_max_km |
| is_potentially_hazardous_asteroid |

---

### Table 2: close_approach

| Column |
|----------|
| neo_reference_id |
| close_approach_date |
| relative_velocity_kmph |
| astronomical |
| miss_distance_km |
| miss_distance_lunar |
| orbiting_body |

---

## 📊 Dashboard Features

### 🏠 Home

- Project Overview
- Dashboard Summary
- Navigation Menu

---

### 🔍 Filter Criteria

Users can filter asteroid data based on:

- Absolute Magnitude
- Estimated Diameter
- Relative Velocity
- Astronomical Unit (AU)
- Close Approach Date
- Hazardous / Non-Hazardous Asteroids

---

### 📈 SQL Queries

The dashboard includes the following SQL analyses:

1. Count how many times each asteroid has approached Earth.
2. Average velocity of each asteroid.
3. Top 10 fastest asteroids.
4. Hazardous asteroids approaching Earth more than three times.
5. Month with the highest asteroid approaches.
6. Fastest asteroid approach ever recorded.
7. Largest asteroids by estimated diameter.
8. Asteroids whose closest approach is getting nearer over time.
9. Closest approach distance for every asteroid.
10. Asteroids travelling faster than 50,000 km/h.
11. Number of approaches per month.
12. Brightest asteroid.
13. Hazardous vs Non-Hazardous asteroid count.
14. Asteroids passing closer than the Moon.
15. Asteroids passing within 0.05 AU.

---

## 📊 Dashboard Components

- KPI Cards
- SQL Query Execution
- Interactive Filters
- Download Results as CSV
- Bar Charts
- Line Charts
- Area Charts
- Interactive Data Tables

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/NASA-Asteroid-Tracker.git
```

### Navigate to Project

```bash
cd NASA-Asteroid-Tracker
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configure MySQL

Create a MySQL database.

```sql
CREATE DATABASE nasa_asteroids;
```

Update your MySQL credentials inside `app.py` or `database.py`.

```python
host="localhost"
user="root"
password="your_password"
database="nasa_asteroids"
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The dashboard will be available at:

```
http://localhost:8501
```

---

## 📸 Dashboard Preview

The dashboard includes:

- 📊 KPI Cards
- 🔍 Dynamic Filters
- 📈 SQL Analysis
- 📉 Interactive Charts
- 💾 CSV Download
- 🙏 Thank You Page

---

## 📌 Key Learnings

- Working with REST APIs
- JSON Data Processing
- MySQL Database Design
- SQL Queries and Joins
- Data Analysis using Pandas
- Interactive Dashboard Development using Streamlit

---

## 🔮 Future Enhancements

- Live NASA API integration
- Interactive map of asteroid approaches
- Machine Learning-based asteroid risk prediction
- User authentication
- Dashboard deployment on Streamlit Community Cloud

---

## 👩‍💻 Author

**Shagufta Hashmi**

---

## 🙏 Acknowledgements

- NASA NeoWs API
- Streamlit
- MySQL
- Python Community

---

## 📄 License

This project is developed for educational and learning purposes.
