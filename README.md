# Web Scraping Tool
## Overview:
This project is designed to scrape faculty directory information from various college and department websites to eliminate 100% of manual image population for RatePsiProfessor. The script extracts names and profile images for professors and other faculty members, formats the names, and compiles the data into a CSV file.

## Features:
* Scrapes data from 37 different websites
* Extracts names and professor images
* Formats names, accounting for hyphenated last names and those with multiple parts (e.g., double or compound last names)
* Handles single-page and multi-page sites
* Compiles data into CSV file

## Required Libraries:
* pandas
* requests
* beautifulsoup4
* time
* random
* re

### Install missing libraries with pip:
```
pip install beautifulsoup4 pandas requests (..etc.)
```

## Project Structure:
```
Web-Scraping-Tool/
|-- main.py
|-- colleges/
|   |-- __init__.py
|   |-- artsAndSciences.py
|   |-- communicationAndInformationSciences.py
|   |-- communityHealthSciences.py
|   |-- culverhouseBusiness.py
|   |-- education.py
|   |-- engineering.py
|   |-- humanEnvironmentalSciences.py
|   |-- lawSchool.py
|   |-- nursing.py
|   |-- socialWork.py
|-- output/
|   |-- combined_data.csv
```

## Key Functions:
### formatNames(name):
* Cleans and formats names by:
  - Removing prefixes or suffixes such as "Dr. " or ", Ph.D."
  - Converts hyphens from href links to spaces
  - Capitalizes names

### createNameList(name):
* Handles multiple last names by splitting into individual names then creating various combinations
* Returns list of possible name variations to pair with same image

### Data Collection Options:
Single CSV File:
* Run main.py to aggregate data from all college-specific scripts into a single CSV file, containing over 4,200 lines of data (including all possible name combinations)

Individual CSV Files:
* Run each college-specific script individually to generate a CSV file containing data for that specific college. To do this, uncomment the relevant line of code at the bottom of the script

### Data Handling:
* Data is stored in a pandas DataFrame
* Extracted data includes:
  - Name: Full formatted name of faculty member
  - Image: URL to professor image

### Multi-Page Handling:
* For directories with multiple pages, the script iterates through all pages by either detecting a "next" button or using a user-specified number of pages
