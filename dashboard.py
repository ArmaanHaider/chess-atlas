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

search_by = st.selectbox("Search by", ["Name", "City"]) #searching for tournaments by name, city   
search = st.text_input("Search for a tournament by name, city") #Name or city of the tournament to search for
df_copy = df.copy() #creating a copy of the dataframe to avoid changing the original dataframe
if search_by == "Name":
    column = "name"
elif search_by == "City":
    column = "city"
if search:
    results = []
    for index, row in df_copy.iterrows():
        if search.lower() in row.astype(str).str.lower().to_string(): #converts row to a long string to check if the search is present in the row
            results.append(row) #searching for tournaments that match the search query and appending them to a list

    df_copy = pd.DataFrame(results) #creating a new dataframe with the search results

if not df_copy.empty:
    st.subheader("Search Results")
    display_df = df_copy.drop(columns=["links","dates","oid"]) #creating new df which removes unwanted columns
    st.dataframe(display_df, column_config={"url":st.column_config.LinkColumn("url", display_text = "Tournament Link")}) #displaying the search results in a table format and making link clickable