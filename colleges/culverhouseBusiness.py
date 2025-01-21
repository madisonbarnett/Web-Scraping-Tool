from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random

def formatName(name):
    if "dr-" in name:
        name = name.removeprefix("dr-")
    formatted_name = name.replace('-', ' ')
    return formatted_name.title()

# Handles hyphenated names / multiple names
def createNameList(name):
    name_list = [name[0] + ' ' + name[1], name[0] + ' ' +  name[2], name[1] + ' ' +  name[2], name[0] + ' ' + name[1] + '-' + name[2], name[0] + ' ' + name[1] + ' ' + name[2]]
    return name_list

def collect_data():

    base_url = "https://culverhouse.ua.edu/directory/?sf_paged="
    page_number = 1

    column_titles = ['Name', 'Image']
    df = pd.DataFrame(columns=column_titles)

    while True:
        current_url = base_url + str(page_number)
        page = requests.get(current_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find all professor profiles depending on website structure
        professor_articles = soup.find_all('article') 

        # Loop through each article tag
        for article in professor_articles:
            # Extract the name from the href or text
            name_tag = article.find('a', href=True) # Adjust as needed
            if name_tag:
                name_parts = name_tag['href'].split('/')
                unformatted_name = name_parts[4]

                name = formatName(unformatted_name)

                # Extract the image source
                img_tag = article.find('img', src=True)  
                img_src = img_tag['src'] if img_tag else None

                # Add to the DataFrame
                if img_src:
                    check_for_double_lastname = unformatted_name.split('-')
                    if len(check_for_double_lastname) > 2:
                        name_list = createNameList(check_for_double_lastname)
                        # Add multiple name variations to dataframe with same image
                        for names in name_list:
                            name = formatName(names)
                            df = pd.concat([df, pd.DataFrame({'Name': [name], 'Image': [img_src]})], ignore_index=True)

                    else:
                        df = pd.concat([df, pd.DataFrame({'Name': [name], 'Image': [img_src]})], ignore_index=True)

        next_button = soup.find("a", class_="page-numbers next")
        if next_button:
            print("next button exists for page ", page_number)
            page_number += 1
        
        else:
            break
        
        time.sleep(random.randint(2,10))

    # Return df is using with main.py
    return df

    # Save to CSV if using individually
    # df.to_csv('business_professors.csv', index=False)