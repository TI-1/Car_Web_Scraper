import time
import numpy as np
import cv2
from Scraper import CarScraper
from typing import List, Dict
from selenium import webdriver
from bs4 import BeautifulSoup

from Car import Car
import re
import requests


class AutoTraderScraper(CarScraper):
    def __init__(self, driver: webdriver, postcode: str, radius: int, year_from: int, year_to: int, price_from: int,
                 price_to: int, car_list: List[Dict[str, str]]):
        super().__init__()
        self.driver = driver
        self.postcode = postcode
        self.radius = radius
        self.year_from = year_from
        self.year_to = year_to
        self.price_from = price_from
        self.price_to = price_to
        self.car_list = car_list
        self._cars: List[Car] = []
        self.url = (f"https://www.autotrader.co.uk/car-search?advertising-location=at_cars&exclude-writeoff"
                    f"-categories=on&moreOptions=visible&postcode={self.postcode}&price-to={self.price_to}&radius="
                    f"{self.radius}&sort=relevance&year-from={self.year_from}")

    def scrape(self):
        content = self.get_page_content()
        number_of_pages = int(content.find("p", attrs={"data-testid": "pagination-show"}).text.split()[-1])
        if number_of_pages == 0:
            print("No results found.")

        for page_number in range(1, number_of_pages + 1):
            self.url = f"{self.url}&page={page_number}"
            time.sleep(5)
            content = self.get_page_content()

            articles = content.find_all("section", attrs={"data-testid": "trader-seller-listing"})

            print(f"Scraping page {page_number} of {number_of_pages}...")

            for article in articles:
                car_year, car_mileage, car_owners = "", "", ""
                car_images = self.get_image_sources(article)
                car_numberplate = self.get_numberplate(car_images)
                car_price = re.search("[£]\d+(\,\d{3})?", article.text).group(0)
                car_name = article.find("a", {"href": re.compile(r'/car-details/')}).find("h3").text
                car_url = article.find("a", {"href": re.compile(r'/car-details/')}).get("href")
                spec_list = article.find("ul", attrs={"data-testid": "search-listing-specs"})
                for spec in spec_list:
                    if "reg" in spec.text:
                        car_year = spec.text
                    if "miles" in spec.text:
                        car_mileage = spec.text
                    if "owner" in spec.text:
                        car_owners = spec.text[0]
                self._cars.append(
                    Car(name=car_name, price=int(car_price.replace("£", "").replace(",", "")), url=car_url,
                        year=re.sub(r"\s(\(\d\d reg\))", "", car_year),
                        mileage=car_mileage.replace(",", "").replace(" miles", ""),
                        owners=car_owners, potential_numberplate=car_numberplate))
        print("finished scraping autotrader")

    def get_image_sources(self, page_element):
        images = []
        srcsets = [source_tag.get('srcset') for picture_tag in page_element.find_all('picture')
                   for source_tag in picture_tag.find_all('source') if source_tag.get('srcset')]
        for source in srcsets:
            try:
                image_data = requests.get(source).content
                jpg_as_np = np.frombuffer(image_data, dtype=np.uint8)
                img = cv2.imdecode(jpg_as_np, flags=1)
                if img.shape[0] < 195 or img.shape[1] < 260:
                    continue
                else:
                    images.append(img)
            except requests.exceptions.RequestException as err:
                continue
        return images

    def cars(self):
        return self._cars
