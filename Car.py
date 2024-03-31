from dataclasses import dataclass


@dataclass(slots=True)
class Car:
    Name: str
    url: str
    price: int
    year: int
    numberplate: str
    mileage: int
    owners: int
