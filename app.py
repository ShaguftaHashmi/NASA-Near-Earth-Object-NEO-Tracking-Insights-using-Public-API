import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="NASA Asteroid Tracker",
    page_icon="🚀",
    layout="wide"
)

# -------------------- DATABASE CONNECTION --------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="nasa_asteroids"
)

cursor = conn.cursor()


# -------------------- FUNCTION TO RUN QUERY --------------------
def run_query(query):
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    return pd.DataFrame(rows, columns=columns)


# -------------------- METRICS --------------------
cursor.execute("SELECT COUNT(*) FROM asteroids")
total_asteroids = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM close_approach")
total_approaches = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM asteroids
WHERE is_potentially_hazardous_asteroid = TRUE
""")
hazardous_count = cursor.fetchone()[0]

cursor.execute("""
SELECT MAX(relative_velocity_kmph)
FROM close_approach
""")
max_speed = round(cursor.fetchone()[0], 2)


# -------------------- TITLE --------------------
st.markdown(
    """
    <h1 style='text-align:center;color:#2E86C1;'>
    🚀 NASA Asteroid Tracker 🌠
    </h1>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------- METRIC CARDS --------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("☄️ Asteroids", total_asteroids)
c2.metric("🌍 Approaches", total_approaches)
c3.metric("⚠️ Hazardous", hazardous_count)
c4.metric("💨 Fastest (km/h)", f"{max_speed:,.2f}")

st.divider()

# -------------------- SIDEBAR --------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🔍 Filter Criteria",
        "📊 SQL Queries",
        "🙏 Thank You"
    ]
)
if page == "🏠 Home":

    st.title("🚀 NASA Near Earth Object (NEO) Tracker")

    st.image(
        "https://www.nasa.gov/wp-content/uploads/2023/03/stsci-01ga76rm0c11depzt8x1p0t1qq.png",
        use_container_width=True
    )

    st.markdown("""
    ### 🌍 Project Overview

    This dashboard analyzes NASA's Near-Earth Object (NEO) data.

    ### Features

    - ☄️ Asteroid Filtering
    - 📊 SQL Analytics
    - 📈 Interactive Charts
    - 💾 Download Results
    - 🛰️ NASA NeoWs Dataset
    """)

# =====================================================
# FILTER PAGE
# =====================================================

elif page == "🔍 Filter Criteria":

    col1, col2, col3 = st.columns(3)

    # Column 1
    with col1:

        magnitude = st.slider(
            "Min Magnitude",
            10.0,
            35.0,
            (13.8, 32.6)
        )

        min_diameter = st.slider(
            "Min Estimated Diameter (km)",
            0.0,
            5.0,
            (0.0, 5.0)
        )

        max_diameter = st.slider(
            "Max Estimated Diameter (km)",
            0.0,
            10.5,
            (0.0, 10.5)
        )

    # Column 2
    with col2:

        velocity = st.slider(
            "Relative Velocity (km/h)",
            0,
            180000,
            (1000, 180000)
        )

        astronomical = st.slider(
            "Astronomical Unit",
            0.0,
            0.5,
            (0.0, 0.5)
        )

        hazardous = st.selectbox(
            "Potentially Hazardous",
            ["All", "Yes", "No"]
        )

    # Column 3
    with col3:

        start_date = st.date_input(
            "Start Date",
            date(2024, 1, 1)
        )

        end_date = st.date_input(
            "End Date",
            date(2025, 4, 13)
        )

    if st.button("🔍 Filter"):

        st.info("Dynamic SQL filter will be added in Part 2.")

        query = """
        SELECT
            a.id,
            a.name,
            a.absolute_magnitude_h,
            a.estimated_diameter_min_km,
            a.estimated_diameter_max_km,
            a.is_potentially_hazardous_asteroid,
            c.close_approach_date,
            c.relative_velocity_kmph,
            c.astronomical,
            c.miss_distance_km
        FROM asteroids a
        JOIN close_approach c
        ON a.id = c.neo_reference_id
        LIMIT 100;
        """

        df = run_query(query)

        st.subheader("Filtered Asteroids")

        st.dataframe(
            df,
            use_container_width=True
        )


# =====================================================
# QUERY PAGE
# =====================================================

elif page == "📊 SQL Queries":

    st.subheader("SQL Queries")

    st.info("All 15 project queries will be added in Part 3.")
    
    st.subheader("📊 SQL Analysis")

    queries = {

    "1. Count how many times each asteroid has approached Earth":
    """
    SELECT
    a.name,
    COUNT(*) AS Total_Approaches
    FROM asteroids a
    JOIN close_approach c
    ON a.id=c.neo_reference_id
    GROUP BY a.id,a.name
    ORDER BY Total_Approaches DESC;
    """,

    "2. Average velocity of each asteroid":
    """
    SELECT
    a.name,
    ROUND(AVG(c.relative_velocity_kmph),2) AS Average_Velocity
    FROM asteroids a
    JOIN close_approach c
    ON a.id=c.neo_reference_id
    GROUP BY a.id,a.name
    ORDER BY Average_Velocity DESC;
    """,

    "3. Top 10 Fastest Asteroids":
    """
    SELECT
    a.name,
    MAX(c.relative_velocity_kmph) AS Maximum_Velocity
    FROM asteroids a
    JOIN close_approach c
    ON a.id=c.neo_reference_id
    GROUP BY a.id,a.name
    ORDER BY Maximum_Velocity DESC
    LIMIT 10;
    """,

    "4. Hazardous Asteroids Approached More Than 3 Times":
    """
    SELECT
    a.name,
    COUNT(*) AS Total_Approaches
    FROM asteroids a
    JOIN close_approach c
    ON a.id=c.neo_reference_id
    WHERE a.is_potentially_hazardous_asteroid=True
    GROUP BY a.id,a.name
    HAVING COUNT(*)>3;
    """,

    "5. Month With Most Asteroid Approaches":
    """
    SELECT
    MONTHNAME(close_approach_date) AS Month,
    COUNT(*) AS Total
    FROM close_approach
    GROUP BY MONTH(close_approach_date),MONTHNAME(close_approach_date)
    ORDER BY Total DESC
    LIMIT 1;
    """,

    "6. Fastest Ever Approach Speed":
    """
    SELECT
    a.name,
    c.relative_velocity_kmph
    FROM asteroids a
    JOIN close_approach c
    ON a.id=c.neo_reference_id
    ORDER BY c.relative_velocity_kmph DESC
    LIMIT 1;
    """,

    "7. Largest Asteroids":
    """
    SELECT
    name,
    estimated_diameter_max_km
    FROM asteroids
    ORDER BY estimated_diameter_max_km DESC;
    """,

    "8. Closest Approach Getting Nearer":
    """
    SELECT
    a.name,
    c.close_approach_date,
    c.miss_distance_km
    FROM asteroids a
    JOIN close_approach c
    ON a.id=c.neo_reference_id
    ORDER BY a.name,c.close_approach_date;
    """
    "9. Closest Approach of Every Asteroid"
    """
    SELECT
        a.name,
        c.close_approach_date,
        c.miss_distance_km
    FROM asteroids a
    JOIN close_approach c
    ON a.id = c.neo_reference_id
    WHERE c.miss_distance_km =
    (
    SELECT MIN(c2.miss_distance_km)
    FROM close_approach c2
    WHERE c2.neo_reference_id = a.id
    )
    ORDER BY c.miss_distance_km;
    """,

    "10. Asteroids with Velocity > 50,000 km/h":
    """
    SELECT DISTINCT
        a.name,
        c.relative_velocity_kmph
    FROM asteroids a
    JOIN close_approach c
    ON a.id = c.neo_reference_id
    WHERE c.relative_velocity_kmph > 50000
    ORDER BY c.relative_velocity_kmph DESC;
    """,

    "11. Number of Approaches Per Month":
    """
    SELECT
        MONTHNAME(close_approach_date) AS Month,
        COUNT(*) AS Total_Approaches
    FROM close_approach
    GROUP BY MONTH(close_approach_date),
    MONTHNAME(close_approach_date)
    ORDER BY MONTH(close_approach_date);
    """,

    "12. Brightest Asteroid":
    """
    SELECT
        name,
        absolute_magnitude_h
    FROM asteroids
    ORDER BY absolute_magnitude_h ASC
    LIMIT 1;
    """,

    "13. Hazardous vs Non-Hazardous":
    """
    SELECT
    CASE
    WHEN is_potentially_hazardous_asteroid = TRUE
    THEN 'Hazardous'
    ELSE 'Non-Hazardous'
    END AS Category,
    COUNT(*) AS Total
    FROM asteroids
    GROUP BY is_potentially_hazardous_asteroid;
    """,

    "14. Passed Closer Than Moon (<1 LD)":
    """
    SELECT
        a.name,
        c.close_approach_date,
        c.miss_distance_lunar
    FROM asteroids a
    JOIN close_approach c
    ON a.id = c.neo_reference_id
    WHERE c.miss_distance_lunar < 1
    ORDER BY c.miss_distance_lunar;
    """,

    "15. Came Within 0.05 AU":
    """
    SELECT
        a.name,
        c.close_approach_date,
        c.astronomical
    FROM asteroids a
    JOIN close_approach c
    ON a.id = c.neo_reference_id
    WHERE c.astronomical < 0.05
    ORDER BY c.astronomical;
    """
    }

    selected_query = st.selectbox(
        "Choose SQL Query",
        list(queries.keys())
    )

    if st.button("▶ Run Query"):

        df = run_query(queries[selected_query])

        st.success("Query Executed Successfully")

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download CSV",
            csv,
            "query_result.csv",
            "text/csv"
    )
elif page == "🙏 Thank You":

    st.balloons()

    st.markdown("""
    <div style='text-align:center;padding:40px;'>

    <h1 style='color:#1E88E5;'>
    🚀 Thank You!
    </h1>

    <h3>
    NASA Near-Earth Object (NEO) Tracker
    </h3>

    <br>

    <h4>
    Submitted by
    </h4>

    <h2 style='color:#4CAF50;'>
    Shagufta Hashmi
    </h2>

    <br>

    <h4>
    Technologies Used
    </h4>

    <p style='font-size:18px;'>

    🐍 Python <br>
    🌐 Streamlit <br>
    🛢️ MySQL <br>
    📊 Pandas <br>
    🚀 NASA NeoWs API

    </p>

    <br>

    <h3 style='color:#ff9800;'>
    Thank You for Your Valuable Time 😊
    </h3>

    </div>
    """, unsafe_allow_html=True)
    