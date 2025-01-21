from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
import re

def formatName(name):
    if "," in name:
        name_parts = name.split(',')
        name = re.sub(r'[^A-Za-z\s]', '', name_parts[0])
    return name.title()

# Handles hyphenated names / multiple names
def createNameList(name):
    name_list = [name[0] + ' ' + name[1], name[0] + ' ' +  name[2], name[1] + ' ' +  name[2], name[0] + ' ' + name[1] + '-' + name[2], name[0] + ' ' + name[1] + ' ' + name[2]]
    return name_list

def collect_data():

    url = "https://socialwork.ua.edu/ssw-directory/faculty-14356/"

    column_titles = ['Name', 'Image']
    df = pd.DataFrame(columns=column_titles)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    ## Find all professor profiles depending on website structure
    professor_articles = soup.find_all('article') 

    # Loop through each article tag
    for article in professor_articles:
        # Extract the name from the href or text
        name_tag = article.find('h3', class_ = "name")  # Adjust as needed
        if name_tag:
            name = name_tag.text.strip()
            name = formatName(name)

            # Extract the image source
            img_tag = article.find('img', src=True)  
            img_src = img_tag['src'] if img_tag else None

            # Add to the DataFrame
            if img_src:
                check_for_double_lastname = name.split(' ')
                if len(check_for_double_lastname) > 2:
                    name_list = createNameList(check_for_double_lastname)
                    # Add multiple name variations to dataframe with same image
                    for names in name_list:
                        df = pd.concat([df, pd.DataFrame({'Name': [names], 'Image': [img_src]})], ignore_index=True)

                else:
                    df = pd.concat([df, pd.DataFrame({'Name': [name], 'Image': [img_src]})], ignore_index=True)

        
    time.sleep(random.randint(2,10))
    # Return df if using with main.py
    return df

    # Save to CSV if using individually
    # df.to_csv('socialWork_professors.csv', index=False)