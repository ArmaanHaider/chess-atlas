from bs4 import BeautifulSoup
import requests
import dashboard as db
import pandas as pd
    
def get_tournament_cost(soup):

    keywords = ["cost", "entry fee", "registration fee", "price", "fee", "entry fees"]
    text = soup.get_text().lower()  # Get the text content of the page and convert to lowercase
    for keyword in keywords:
        position = text.find(keyword)

        if position != -1: 
            return text[position:position + 200]  # Return the substring containing the keyword and some extra content

    return "Cost information not found"  # Return a message if no keyword is found

def get_tournament_location(soup):

    keywords = ["location", "place", "venue", "address", "tournament venue", "playing venue"]
    text = soup.get_text().lower()  # Get the text content of the page and convert to lowercase
    for keyword in keywords:
        position = text.find(keyword)

        if position != -1: 
            return text[position:position + 100]  # Return the substring containing the keyword and some extra content

    return "Location information not found"  # Return a message if no keyword is found

tournament_data = [] # creating list to append tournament details

for url in db.display_df['url']:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser') #Webscraping each website to get the tournament details like cost.
                
        cost = get_tournament_cost(soup)
        location = get_tournament_location(soup)
                
        tournament_data.append({
            "url": url,     
            "cost": cost,
            "location": location
        })             

        print("Successfully scraped:", url)   

    except Exception as e:
        print("Error scraping:", url, "Error:", e)

df = pd.DataFrame(tournament_data) #creating a dataframe with the tournament details
df.to_csv("tournament_details.csv", index=False) #saving the dataframe to a csv file

print(df.head()) #printing first 5 rows of df

