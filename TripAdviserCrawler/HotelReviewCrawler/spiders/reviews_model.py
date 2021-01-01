from marshmallow_dataclass import dataclass
from typing import List


@dataclass
class Review:
    id: str
    text: str


@dataclass
class Reviews:
    reviews: List[Review]

    def print(self):
        for review in self.reviews:
            print(review.id + ": " + review.text + "\n")
