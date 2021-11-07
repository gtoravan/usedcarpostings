
import requests
from bs4 import BeautifulSoup
import geopy
from geopy.geocoders import Nominatim
import csv

import json

#removed geocoder files

default_limit = 20

def scrape(URL):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="vehicle-cards-container")

    traverse_urls = []

    posting_list = []

    # print(results.prettify())

    car_elements = results.find_all("div", class_="vehicle-card")
    for car_element in car_elements:
        title_element = car_element.find("h2", class_="title")
        company_element = car_element.find("span", class_="primary-price")
        location_element = car_element.find("div", class_="dealer-name")
        car_link = car_element.find("a", {"class": "vehicle-card-link js-gallery-click-link"}).attrs['href']
        #
        # print(title_element.text)
        # print(company_element.text)
        # print(location_element.text)
        # print(car_link)
        traverse_urls.append("https://www.cars.com/" + str(car_link))
        # print()

    for i in traverse_urls:
        rec = scrapeForEach(i)
        if len(rec) != 0:
            posting_list.append(rec)

    return posting_list

def scrapeForEach(URL):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    temp_list = []

    title_element = soup.find("h1", class_="listing-title")
    price_element = soup.find("span", class_="primary-price")
    dealer_element = soup.find("h3", class_="sds-heading--5 heading seller-name")
    location_element = soup.find("div", class_="dealer-address")
    location_element = location_element.text
    # print(location_element)

    geolocator = Nominatim(user_agent="maps")
    location = geolocator.geocode(str(location_element))
    if location != None:
        temp_list = [title_element.text, price_element.text, dealer_element.text, location.latitude,
                     location.longitude]

    return temp_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    master_list = []
    for i in range(1,default_limit+1):
        print(i)
        URL = "https://www.cars.com/shopping/results/?page=" + str(i) + "&page_size=100&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=&maximum_distance=all&mileage_max=&seller_type[]=dealership&sort=best_match_desc&stock_type=all&year_max=&year_min=&zip=14265"
        master_list = master_list + (scrape(URL))

    print(master_list)

    #CSVVVVVVVVVVVVVVV

    with open('data.csv', mode='w') as csv_file:
        fieldnames = ['title', 'price', 'dealer_name', 'lat', 'long']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for i in master_list:
            price = i[1].rstrip("$").replace(",", "")
            writer.writerow({'title': i[0], 'price': price, 'dealer_name': i[2], 'lat': i[3], 'long': i[4]})