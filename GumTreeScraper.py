from typing import List
import time

import requests
from numpy import typing as npt
from selenium import webdriver
from Scraper import CarScraper
from Car import Car
import re
import numpy as np
import cv2


class GumTreeScraper(CarScraper):

    def __init__(self, driver: webdriver, postcode: str, radius: int, price_from: int, price_to: int):
        super().__init__()
        self.radius = radius
        self.driver = driver
        self.postcode = postcode
        self.price_from = price_from
        self.price_to = price_to
        self._cars: List[Car] = []
        self.url = (f"https://www.gumtree.com/search?search_category=cars&search_location"
                    f"={postcode}&max_price={price_to}&min_price={price_from}&search_distance={radius}&distance={radius}")

    @property
    def cars(self):
        return self._cars

    def scrape(self):
        content = self.get_page_content()
        number_of_cars = int(content.find("h1", attrs={"class": "css-19squc8"}).text.split()[0].replace(",", ""))
        if number_of_cars == 0:
            print("No results found.")
        page_number = 1
        car_number = 1

        while car_number < 20:
            try:
                self.url = f"{self.url}&page={page_number}"
            except Exception as err:
                print("Finished Scraping Gumtree")
                break
            time.sleep(5)
            content = self.get_page_content()
            articles = content.find_all("article", attrs={"data-q": "search-result"})
            for article in articles:
                print(f"Scraping car {car_number} of {number_of_cars}...")
                car_year = article.find("span", {"data-q": "motors-year"}).text
                car_mileage = article.find("span", {"data-q": "motors-mileage"}).text
                car_images = self.get_image_sources(article)
                car_numberplate = self.get_numberplate(car_images)
                car_price = article.find("div", {"data-testid": "price"}).text
                car_name = article.find("div", {"data-q": "tile-title"}).text
                car_url = article.find("a", {"data-q": "search-result-anchor"}).get("href")
                self._cars.append(
                    Car(name=car_name, price=int(car_price.replace("£", "").replace(",", "")), url=car_url,
                        year=re.sub(r"\s(\(\d\d reg\))", "", car_year),
                        mileage=car_mileage.replace(",", "").replace(" miles", ""),
                        owners=0, potential_numberplate=car_numberplate))
                car_number += 1
            page_number += 1
        print("Finished Scraping")

    def get_image_sources(self, page_element) -> List[npt.NDArray]:
        images = []
        source = page_element.find("img").get("data-src")
        try:
            image_data = requests.get(source).content
            jpg_as_np = np.frombuffer(image_data, dtype=np.uint8)
            img = cv2.imdecode(jpg_as_np, flags=1)
            if img.shape[0] < 195 or img.shape[1] < 260:
                return images
            else:
                images.append(img)
        except requests.exceptions.RequestException as err:
            print(err)
        return images
