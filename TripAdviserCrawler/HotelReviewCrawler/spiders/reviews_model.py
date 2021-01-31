from marshmallow_dataclass import dataclass
from typing import List


@dataclass
class Review:
    id: str
    text: str

    def __init__(self, review_id, text):
        self.id = review_id
        self.text = text


@dataclass
class Reviews:
    reviews: List[Review]

    def __init__(self):
        self.reviews = list()

    def add(self, review):
        self.reviews.append(review)

    def print(self):
        for review in self.reviews:
            print(review.id + ": " + review.text + "\n")



def object_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'User':
        return Review(obj['id'], obj['text'])
    return obj
