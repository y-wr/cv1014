import datetime


# Return the current day and any day added
def getDay(day):
    return (datetime.date.today() + datetime.timedelta(day)).strftime("%Y-%m-%d")

# Return the URL for the website after adding in the parameter
def getURL(check_in_date, check_out_date, adults, children, rooms):
    return f"https://www.booking.com/searchresults.en-gb.html?ss=Singapore&ssne=Singapore&ssne_untouched=Singapore&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaMkBiAEBmAEJuAEHyAEN2AEB6AEBiAIBqAIDuAKLiYahBsACAdICJGZkMjU1YjNmLTk4OTYtNDEwOS1hYTU0LWI1NWEyZThjOTBmN9gCBeACAQ&sid=a0cb1b22dffb48f2af8ff75bc510a6e3&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-73635&dest_type=city&checkin={check_in_date}&checkout={check_out_date}&group_adults={adults}&no_rooms={rooms}&group_children={children}&sb_travel_purpose=leisure"

# Reutrns the distance of the hotel (for sorting purposes)
def getDistance(hotel):
    # Get the distance element in the dictionary
    distance = hotel.get("distance")
    # Get the numeric distance and the associated unit
    numeric, units = float(distance.split()[0]), distance.split()[1]
    # Account for distance in metres
    if units == "m":
        numeric /= 1000
    return numeric

# Gives a sorted list of the data according to the various sorting parameters
def sortData(sortBy, hotelData):
    if sortBy == "price":
        sortedData = sorted(hotelData, key=lambda x: int(x["price"].replace(",", "").split()[1]))
    elif sortBy == "rating":
        sortedData = sorted(hotelData, key=lambda x: float(x["rating"]))
    elif sortBy == "distance":
        sortedData = sorted(hotelData, key=getDistance)
    return sortedData

# Update the list with the new added data
def newData(hotelData, hotelName, rating, wordRating, price, location, distance, duration):
    dict = {
            "name": hotelName,
            "rating": rating,
            "wordRating":wordRating,
            "price":price,
            "location":location,
            "distance":distance,
            "duration":duration
        }
    
    hotelData.append(dict)
    return hotelData

