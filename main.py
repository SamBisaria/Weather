import requests

def createURL(endpoint, options):
  base = "https://api.weather.gov/"
  base = base + endpoint + "/"
  for option in options:
      base =  base + option + "/"
  return base

def getlatlong(streetaddress, city, state, zip):
  address = streetaddress + "%2C " + city + "%2C " + state + " " + zip
  address = address.replace(" ", "+")
  censusurl = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address="+ address + "&benchmark=2020&format=json"
  response = requests.get(censusurl)
  data = response.json()
  matches = data["result"]["addressMatches"]
  coordinates = matches[0]["coordinates"]
  return coordinates["x"], coordinates["y"]

def getforecasturl(latitude, longitude):
  url = createURL("points", [str(latitude) + "," + str(longitude)])
  r = requests.get(url,headers = {"User-Agent":"364254h4h45y3q3ywg8ywr9ygb98"})

  data = r.json()
  #print (data["properties"])
  return data["properties"]["forecast"]

def forecast(url):
  r = requests.get(url,headers = {"User-Agent":"364254h4h45y3q3ywg8ywr9ygb98"})
  data = r.json()
  results = []
  for period in data["properties"]["periods"]:
    results.append({
      "name": period["name"],
      "temperature": period["temperature"],
      "windspeed": period["windSpeed"],
      "winddirection": period["windDirection"],
      "detailedforecast": period["detailedForecast"],
    })
  return results

def main():
  Address = input("Enter your street address: ")
  City = input("Enter your city: ")
  State = input("Enter your state(as an abbreviation): ")
  Zip = input("Enter your ZIP code: ")
  longitude, latitude = getlatlong(Address , City, State, Zip)

  forecasturl = getforecasturl(latitude, longitude)
  results = forecast(forecasturl)
  print()
  for result in results:
    print (result["name"] + ": ")
    print ("\tTemperature: " + str(result["temperature"]))
    print ("\tWind Speed: " + str(result["windspeed"]))
    print ("\tWind Direction: " + result["winddirection"])
    print ("\tDetailed Forecast: " + result["detailedforecast"])
    print()


main()