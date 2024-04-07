from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class Car:
    name: str
    url: str
    price: int
    year: int
    potential_numberplate: List[str]
    mileage: int
    owners: int
