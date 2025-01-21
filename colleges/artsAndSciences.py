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

    # Arts and Sciences departments without multiple pages
    department_links_single = {
        "https://ams.ua.edu/directory/": "col",
        "https://anthropology.ua.edu/directory/": "col-10 col-md-12",
        "https://art.ua.edu/people/": "col",
        "https://bsc.ua.edu/directory/": "col",
        "https://blount.as.ua.edu/hoi-polloi-people/faculty-staff/": "col",
        "https://chemistry.ua.edu/faculty-and-staff/": "col",
        "https://cd.ua.edu/people/": "col-10 col-md-12",
        "https://cj.ua.edu/contact-us/faculty-staff/": "col-10 col-md-12",
        "https://english.ua.edu/faculty-and-staff-directory/": "col",
        "https://grs.ua.edu/directory/": "col",
        "https://geography.ua.edu/directory/": "col-12",
        "https://history.ua.edu/contact-us/faculty-and-staff-directory/": "col",
        "https://mlc.ua.edu/directory/": "col-10 col-md-12",
        "https://newcollege.ua.edu/directory/": "col-lg-3",
        "https://philosophy.ua.edu/people/": "col",
        "https://physics.ua.edu/department-directory/": "col-10 col-md-12",
        "https://psc.ua.edu/contact/directory/": "col",
        "https://psychology.ua.edu/faculty-and-staff-directory/": "col-10 col-md-12",
        "https://religion.ua.edu/directory/": "col",
        "https://music.ua.edu/faculty-staff/": "col-12",
        "https://theatre.ua.edu/contact/directory/": "col-lg-3"
    }

    # Arts and Sciences departments with multi-page directories
    department_links_multiple = {
        "https://geo.ua.edu/contact-us/directory/?sf_paged=": {"class_name": "col-lg-3", "page_count": 2},
        "https://math.ua.edu/faculty-staff/?sf_paged=": {"class_name": "col-lg-3", "page_count": 5}
    }

    column_titles = ['Name', 'Image']
    df = pd.DataFrame(columns=column_titles)

    for url, class_name in department_links_single.items():
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # Find all professor profiles depending on website structure
        professor_columns = soup.find_all("div", class_ = class_name) 

        # Loop through each article found
        for article in professor_columns:
            # Extract the name from the href or text
            name_tag = article.find('a', href=True) # Adjust as needed
            if name_tag:
                name_parts = name_tag['href'].split('/')  
                length_of_url = len(name_parts)
                unformatted_name = name_parts[length_of_url - 2]

                name = formatName(unformatted_name)

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
                            name = names.title()
                            df = pd.concat([df, pd.DataFrame({'Name': [name], 'Image': [img_src]})], ignore_index=True)

                    else:
                        df = pd.concat([df, pd.DataFrame({'Name': [name], 'Image': [img_src]})], ignore_index=True)
        
        # print("Completed " + url + ", moving to next site")
        time.sleep(random.randint(2,10))

    # Begins scraping directories with multiple pages
    for base_url, details in department_links_multiple.items():
        page_count = details["page_count"]
        class_name = details["class_name"]
        page_number = 1

        while page_number <= page_count:
            url = base_url + str(page_number)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            
            professor_columns = soup.find_all("div", class_ = class_name)

            for article in professor_columns:
                # Extract the name from the href or text
                name_tag = article.find('a', href=True) # Adjust as needed
                if name_tag:
                    name_parts = name_tag['href'].split('/')  
                    length_of_url = len(name_parts)
                    unformatted_name = name_parts[length_of_url - 2]

                    name = formatName(unformatted_name)

                    # Extract the image source
                    img_tag = article.find('img', src=True) 
                    img_src = img_tag['src'] if img_tag else None

                    # Add to the DataFrame
                    if img_src:
                        check_for_double_lastname = name.split(' ')
                        if len(check_for_double_lastname) > 2:
                            name_list = createNameList(check_for_double_lastname)
                            for names in name_list:
                                name = names.title()
                                df = pd.concat([df, pd.DataFrame({'Name': [name], 'Image': [img_src]})], ignore_index=True)

                        else:
                            df = pd.concat([df, pd.DataFrame({'Name': [name], 'Image': [img_src]})], ignore_index=True)
        
            # print("Completed " + url + ", moving to next page")
            time.sleep(random.randint(2,10))

            page_number += 1

        # print("Completed " + url + ", moving to next url")
        time.sleep(random.randint(2,10))

    # Return df if using with main.py
    return df
    
    # Save to CSV if using individually
    # df.to_csv('arts_and_sciences_professors.csv', index=False)
