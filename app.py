from flask import Flask, render_template, request
from wr import *
from my import *

# Requirements to run Flask=
app = Flask(__name__)
app.config["SECRET_KEY"] = "randomKEY"

# Routing for main page
@app.route("/", methods=["GET", "POST"])
def index():
    # Load input page for user if website entered through "GET" request.
    if request.method == "GET":
        # Define the minimum date selection for the form
        today = getDay(0)
        min_checkout_date = getDay(1)
        return render_template("index.html", today=today, min_checkout_date=min_checkout_date)

    # If "POST" request is received, do the following
    # Extract information from form to be used as parameters
    check_in_date = request.form["check-in-date"]
    check_out_date = request.form["check-out-date"]
    adults = request.form["adults"]
    children = request.form["children"]
    rooms = request.form["rooms"]

    # Generate the URL of the website using the parameters obtain
    url = getURL(check_in_date, check_out_date, adults, children, rooms)
    # Get the HTML of the wesite using Selenium Webdriver
    html = getHTML(url)
    # Parse the HTML through BeautifulSoup4 and put it into a list
    hotelData = getData(html)
    # Create a JSON file that store the list for future uses
    storeList(hotelData)

    # Return a page where user can see the list of hotels
    return render_template("hotel_info.html", hotelData=hotelData)

# Routing for page where all hotel information is displayed
@app.route("/hotel_info", methods=["GET", "POST"])
def hotel_info():
    # Load the idata from JSON file
    hotelData = getList("hotelData.txt")
    # Load input page for user if website entered through "GET" request from searched page
    if request.method == "GET":
      return render_template("hotel_info.html", hotelData=hotelData)
    
    # Get the type of sorting requested from the form
    sortBy = request.form["sort"]

   # Get the sorted list of data
    sortedData = sortData(sortBy, hotelData)
    return render_template("hotel_info.html", hotelData=sortedData)

@app.route("/input", methods=["GET", "POST"])
def input():
   # Load input page for user if website entered through "GET" request.
   if request.method == "GET":
      return render_template("input.html")

   # If "POST" request is received, do the following
   # Extract information from form to be used as parameters
   hotelName = request.form['name']
   rating = request.form['rating']
   wordRating = request.form['word_rating']
   price = "S$ " + request.form['price']
   location = request.form['location']
   distance = request.form['distance'] + " " + request.form["distance_unit"] + " from centre"
   duration = request.form['duration']

   # Load the list from JSON file
   hotelData = getList("hotelData.txt")
   # Update the list with the new data
   hotelData = newData(hotelData, hotelName, rating, wordRating, price, location, distance, duration)
   # Update the JSON file with the new data
   storeList(hotelData)
   # Return the page where user can see all data
   return render_template("hotel_info.html", hotelData=hotelData)

@app.route("/search", methods=["GET", "POST"])
def search():
   # Load input page for user if website entered through "GET" request.
   if request.method == "GET":
      return render_template("search.html")

   # Load the list from JSON file
   hotelData = getList("hotelData.txt")

   # If "POST" request is received, do the following
   # Extract information from form to be used as parameters
   search_by = request.form["search_by"]
   if search_by == "price":
      minPrice = request.form["min_price"]
      maxPrice = request.form["max_price"]
      searchedData = searchPrice(hotelData, minPrice, maxPrice)
   elif search_by == "ratings":
      minRating = request.form["min_rating"]
      maxRating = request.form["max_rating"]
      searchedData = searchRating(hotelData, minRating, maxRating)

   return render_template("searched.html", searchedData=searchedData)