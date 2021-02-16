from marshmallow_dataclass import dataclass


@dataclass
class Hotel:
    id: str
    name: str
    country: str
    city: str
    rating: int
    amenities: str

    def __init__(self, hotel_id, name, country, city, rating, amenities):
        self.id = hotel_id
        self.name = name
        self.country = country
        self.city = city
        self.rating = rating
        self.amenities = amenities

    def print(self):
        print(f"id: {self.id}, name: {self.name}, country: {self.country}, city: {self.city}, rating: {self.rating},"
              f" amenities: {self.amenities}")
