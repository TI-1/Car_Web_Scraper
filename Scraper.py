import re
from abc import ABC, abstractmethod


class CarScraper(ABC):
    @property
    @abstractmethod
    def cars(self):
        pass

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def numberplate_detector(self, image):
        pass

    @abstractmethod
    def get_numberplate(self, article):
        pass

    @staticmethod
    def is_valid_uk_number_plate(plate):
        pattern = r'^[A-Z]{2}\d{2}\s?[A-Z]{3}$'
        return bool(re.match(pattern, plate.upper()))
