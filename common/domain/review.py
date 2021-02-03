from marshmallow_dataclass import dataclass
from datetime import date


@dataclass
class Review:
    id: str
    text: str
    geo: str
    published_date: date
    rating: int
    location: str
    language: str
    original_language: str
    translation_type: str
    stay_date: date
    trip_type: str
    like_count: int

    def __init__(self, review_id, text, geo, published_date, rating, location, language, original_language,
                 translation_type, stay_date, trip_type, like_count):
        self.id = review_id
        self.text = text
        self.geo = geo
        self.published_date = published_date
        self.rating = rating
        self.location = location
        self.language = language
        self.original_language = original_language
        self.translation_type = translation_type
        self.stay_date = stay_date
        self.trip_type = trip_type
        self.like_count = like_count

