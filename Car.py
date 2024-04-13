from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class Car:
    def __repr__(self):
        return (f"{{Name: {self.listing_name}, NumberPlate: {self.potential_numberplate}, Price: £{self.price}, "
                f"Year: {self.year}, Mileage: {self.mileage}}}")
    listing_name: str
    car_name: str
    url: str
    price: int
    year: int
    potential_numberplate: List[str]
    mileage: int
    owners: int

