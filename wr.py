from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from my import sortData
import json


# Use Selenium to obtain HTML of page
def getHTML(url):
    # Initiate the web driver
    driver = webdriver.Chrome("/Users/yeowenrong/CV1014/Project/chromedriver")
    driver.get(url)

    # Wait for HTML of the webpage to full load before getting HTML
    wait = WebDriverWait(driver, timeout=10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "html")))
    
    # Get the HTML from the page
    html = driver.page_source
   
    # Quit driver
    driver.quit()
    return html

# Obtain data from HTML
def getData(html):
    # Search for all relevant elements using CSS selectors
    soup = BeautifulSoup(html, "html.parser")
    hotels = soup.find_all("div", {"data-testid": "title", "class": "fcab3ed991 a23c043802"})
    no_ratings = soup.find_all("div", {"class": "b5cd09854e d10a6220b4"})
    word_ratings = soup.find_all("div", {"class": "b5cd09854e f0d4d6a2f5 e46e88563a"})
    price = soup.find_all("span", {"class": "fcab3ed991 fbd1d3018c e729ed5ab6"})
    location = soup.find_all("span", {"data-testid": "address", "class": "f4bd0794db b4273d69aa"})
    distance = soup.find_all("span", {"data-testid": "distance"})
    duration = soup.find_all("div", {"data-testid": "price-for-x-nights", "class": "d8eab2cf7f c90c0a70d3"})
    
    # Store the relevant elements of a hotel in a dictionary and append it to a list
    store = list()
    for i in range(len(hotels)):
        dict = {
            "name": hotels[i].text,
            "rating": no_ratings[i].text,
            "wordRating":word_ratings[i].text,
            "price":price[i].text,
            "location":location[i].text,
            "distance":distance[i].text,
            "duration":duration[i].text
        }
        store.append(dict)

    # Return the list generated
    return store

# Write the data into a JSON file
def storeList(hotelData):
    # Convert list into a JSON 
    json_str = json.dumps(hotelData)
    # Write JSON string to a file.
    with open('hotelData.txt', 'w') as f:
        f.write(json_str)

# Read JSON file that is saved
def getList(hotelData):
    # Read JSON string from file
    with open(hotelData, 'r') as f:
        json_str = f.read()
    # Convert JSON string to a list
    hotels = json.loads(json_str)
    return hotels

def searchRating(hotelData, minRating, maxRating):
    searchedData = []
    for hotel in hotelData:
        if float(minRating) <= float(hotel["rating"]) <= float(maxRating):
            searchedData.append(hotel)
    return sortData("rating", searchedData)

def searchPrice(hotelData, minPrice, maxPrice):
    searchedData = []
    for hotel in hotelData:
        if float(minPrice) <= float(hotel["price"].replace(",", "").split()[1]) <= float(maxPrice):
            searchedData.append(hotel)
    return sortData("price", searchedData)