import sqlite3
import pandas as pd
import streamlit as st
import calendar
from datetime import date, datetime

#Creating dashboard using streamlit
st.set_page_config(page_title="Chess Tournaments Dashboard", layout="wide")
st.title("Chess Tournaments Dashboard")

df=pd.read_sql("SELECT * FROM tournaments", con=sqlite3.connect("chess_tournaments.db")) # reading data from database

# Load additional tournament details
details = pd.read_csv("tournament_details.csv")

# Load tournament dates and calendar information
calendar_df = pd.read_csv("chess_tournaments.csv")

tab1, tab2 = st.tabs([
    "🔍 Tournament Search",
    "📅 Tournament Calendar"
]) #creating 2 tabs in the dashboard for searching tournaments and viewing the tournament calendar

def tournament_calendar(data):

    data = data.copy()

    # Convert dates into datetime format
    data["start"] = pd.to_datetime(data["start"],errors="coerce")
    data["end"] = pd.to_datetime(data["end"],errors="coerce")

    today = date.today()

    # Get available years
    available_years = sorted(set(data["start"].dt.year.tolist() + [today.year])) #Gets the years which are present in start column along with current year

    # Month and year selection
    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox(
            "Select Month",
            range(1, 13),
            format_func=lambda x: calendar.month_name[x],
            index=today.month - 1,
            key="calendar_month"
        ) # Creates a dropdown for selecting month with current month selected by default

    with col2:
        selected_year = st.selectbox(
            "Select Year",
            available_years,
            index=available_years.index(today.year),
            key="calendar_year"
        ) # Creates a dropdown for selecting year with current year selected by default

    st.markdown(f"### {calendar.month_name[selected_month]} {selected_year}") # Displays the selected month and year as a heading

    # Generate calendar weeks
    month_weeks = calendar.monthcalendar(selected_year,selected_month) # Generates a list of weeks for the selected month and year

    weekdays = ["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"]

    header_cols = st.columns(7)

    for i, day_name in enumerate(weekdays):
        header_cols[i].markdown(f"**{day_name[:3]}**") #Writes first 3 letters of the day name in the header of the calendar in bold

    # Display calendar
    for week in month_weeks:
        day_cols = st.columns(7)
        for i, day in enumerate(week):
            with day_cols[i]:
                if day == 0:
                    st.write("")
                    continue

                current_date = date(selected_year,selected_month,day)

                st.markdown(f"**{day}**")

                # Calculate tournament duration
                data["duration"] = (data["end"] - data["start"]).dt.days

                # Find tournaments happening on this date
                # Tournaments with duration > 5 days are considered to be happening on the start date only as the calendar is cluttered otherwise
                events_today = data[
                    (
                       (data["duration"] > 5) & (data["start"].dt.date == current_date)
                    ) |
                (
                       (data["duration"] <= 5) & (data["start"].dt.date <= current_date) &
                       (data["end"].dt.date >= current_date)
                    )                   
                ]

                # Display tournaments
                for _, event in events_today.iterrows():
                    tournament_name = str(event["name"])
                    
                    st.caption(f"♟ {tournament_name}")      
                    st.caption(f" duration: {event['duration']+1} days")          

                if current_date == today:
                    st.caption("Today")


with tab1:
    col1, col2= st.columns(2) # dividing dashboard into 2 equally spaced columns
    col1.metric("Total Tournaments",len(df)) #Finding total number of tournaments in database
    col2.metric("Cities",df["city"].nunique()) #Finding total unique cities in database
    st.divider() #Adds horizontal line

    st.subheader("Find a Tournament") #Finding a tournament by name or city
    search_name = st.text_input("Enter tournament name")
    col1, col2, col3= st.columns(3) 
    with col1:
        cities = ["All"] + sorted(df["city"].dropna().unique().tolist()) #adding 3 searches for city, province and type
        selected_city = st.selectbox("City", cities)

    with col2:
        provinces = ["All"] + sorted(df["prov"].dropna().unique().tolist())
        selected_province = st.selectbox("Province", provinces)

    with col3:
        types = ["All"] + sorted(df["type"].dropna().unique().tolist())
        selected_type = st.selectbox("Tournament Type", types)

    status_options = ["All", "Upcoming", "Ongoing", "Completed"]
    selected_status = st.selectbox("Tournament Status", status_options) #Date status filter

    filtered_df = df.copy()

    if search_name:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search_name, case=False, na=False)]

    if selected_city != "All":
        filtered_df = filtered_df[filtered_df["city"] == selected_city]

    if selected_province != "All":
        filtered_df = filtered_df[filtered_df["prov"] == selected_province]

    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["type"] == selected_type] #Simultaneously filter with many filters

    #Date status filtering 
    today = pd.Timestamp.today().normalize()

    filtered_df["start"] = pd.to_datetime(filtered_df["start"], errors="coerce")
    filtered_df["end"] = pd.to_datetime(filtered_df["end"], errors="coerce")

    if selected_status == "Upcoming":
        filtered_df = filtered_df[filtered_df["start"] > today]

    elif selected_status == "Ongoing":
        filtered_df = filtered_df[(filtered_df["start"] <= today) &(filtered_df["end"] >= today)]

    elif selected_status == "Completed":
        filtered_df = filtered_df[filtered_df["end"] < today] 

    st.subheader(f"Search Results ({len(filtered_df)} tournaments)")

    # Remove unnecessary columns if they exist
    filtered_df = filtered_df.drop(
        columns=["links", "dates", "oid"],
        errors="ignore"
    )

    # Make tournament links clickable
    st.dataframe(
        filtered_df,
        column_config={
            "url": st.column_config.LinkColumn("Tournament Link",display_text="Open Tournament")
            },
            use_container_width=True
        )

with tab2:
    tournament_calendar(calendar_df)
