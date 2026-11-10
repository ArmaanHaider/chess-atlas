import sqlite3
import pandas as pd
import streamlit as st

#Creating dashboard using streamlit
st.set_page_config(page_title="Chess Tournaments Dashboard", layout="wide")
st.title("Chess Tournaments Dashboard")

df=pd.read_sql("SELECT * FROM tournaments", con=sqlite3.connect("chess_tournaments.db")) # reading data from database
col1, col2 = st.columns(2) # dividing dashboard into 2 equally spaced columns
col1.metric("Total Tournaments", len(df)) #Finding total number of tournaments in database
col2.metric("cities",df["city"].nunique()) #Finding total unique cities in database 
st.divider() #Adds horizontal line

search = st.text_input("Search for a tournament by name") #search for tournaments by name
df_copy = df.copy() #creating a copy of the dataframe to avoid changing the original dataframe
if search:
    results = []
    for index, row in df_copy.iterrows():
        if search.lower() in row["name"].lower():
            results.append(row) #searching for tournaments that match the search query and appending them to a list

    df_copy = pd.DataFrame(results) #creating a new dataframe with the search results
