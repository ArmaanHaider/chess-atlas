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
