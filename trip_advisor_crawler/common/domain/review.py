from marshmallow_dataclass import dataclass
from datetime import date


@dataclass
class Review:
    id: str
    text: str
    hotel_id: str
    city_location: str
    hotel_publish_date: date
    rating: int
    language: str
    translation_type: str
    original_language: str
    reviewer_stay_date: date
    trip_type: str
    like_count: int

    def __init__(self, review_id, text, hotel_id, city_location, hotel_publish_date, rating, language, translation_type,
                 original_language, reviewer_stay_date, trip_type, like_count):
        self.id = review_id
        self.text = text
        self.hotel_id = hotel_id
        self.city_location = city_location
        self.hotel_publish_date = hotel_publish_date
        self.rating = rating
        self.language = language
        self.original_language = original_language
        self.translation_type = translation_type
        self.reviewer_stay_date = reviewer_stay_date
        self.trip_type = trip_type
        self.like_count = like_count

    def should_translate(self):
        return self.language != "en"
