from marshmallow_dataclass import dataclass


@dataclass
class HotelSummary:
    hotel_id: str
    frequency_summary: str
    tf_idf_summary: str
    frequent_phrases: str

    def __init__(self, hotel_id, frequency_summary, tf_idf_summary, frequent_phrases):
        self.hotel_id = hotel_id
        self.frequency_summary = frequency_summary
        self.tf_idf_summary = tf_idf_summary
        self.frequent_phrases = frequent_phrases
