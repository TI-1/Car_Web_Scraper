from abc import ABC, abstractmethod


class CarScraper(ABC):

    @abstractmethod
    def get_cars(self):
        pass

    @abstractmethod
    def scrape(self):
        pass
