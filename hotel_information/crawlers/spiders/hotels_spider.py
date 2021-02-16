import scrapy
import json
from google_trans_new import google_translator

from common.domain.review import Review
from common.domain.hotel import Hotel

from database.database_connector import DatabaseConnector


class HotelsComCrawler(scrapy.Spider):
    name = "hotelscom"
    start_urls = ["https://www.hotels.com/ho"]
    BASE_URL = "https://www.hotels.com/ho"
    amenities: str
    database = DatabaseConnector()
    translator = google_translator()

    def start_requests(self):
        initial_hotel_id = 356070
        last_hotel_id = 356072
        for hotel_id in range(initial_hotel_id, last_hotel_id):
            yield scrapy.Request(self.BASE_URL + str(hotel_id), self.parse)

    def parse(self, response, **kwargs):
        if response.request.url != "https://www.hotels.com/":
            number_of_pages = self.get_number_of_pages(response)
            self.amenities = self.get_hotel_amenities(response)

            for reviews_page_number in range(number_of_pages):
                review_pages_request_url = response.request.url + '-tr-p' + str(reviews_page_number) + '/?ajax=true&reviewTab=brand-reviews&ajax=true'
                yield scrapy.Request(review_pages_request_url, self.parse_reviews)

    def parse_reviews(self, response):
        json_response = json.loads(response.body)

        json_body = self.get_json_body(json_response)
        hotel = self.store_hotel(json_body, self.amenities)

        review_groups = self.get_review_item_groups(json_body)
        self.store_reviews(review_groups, hotel.id, hotel.city)

    def get_number_of_pages(self, response):
        pages = str(response.xpath('//a[@class="more-reviews"]//text()').get())
        pages = pages.replace('From ', '')
        pages = pages.replace(' reviews', '')

        return int((int(pages) / 50) + 1)

    def get_json_body(self, json_object):
        json_data = json_object["data"]
        json_body = object()
        if json_data:
            json_body = json_data["body"]

        return json_body

    def get_hotel_name(self, json_body):
        hotel_name = ""
        if json_body["propertyDescription"] is not None and json_body["propertyDescription"]["name"] is not None:
            hotel_name = json_body["propertyDescription"]["name"]

        return hotel_name

    def get_review_item_groups(self, json_body):
        review_item_groups = []
        if json_body:
            review_content = json_body["reviewContent"]
            if review_content is not None and review_content["reviews"] is not None and review_content["reviews"]["hermes"] is not None:
                review_groups = review_content["reviews"]["hermes"]["groups"]
                if len(review_groups) > 0:
                    for i in range(len(review_groups)):
                        current_review_group = review_groups[i]
                        review_item_groups.append(current_review_group["items"])

        return review_item_groups

    def store_reviews(self, review_groups, hotel_id, city_location):
        for review in review_groups[0]:
            review_id = review["itineraryId"]
            text = review["description"]
            rating = review["rating"]
            language = review["reviewer"]["locale"]
            reviewer_stay_date = review["reviewDate"]
            trip_type = review["tripType"]

            review_result = Review(review_id, text, hotel_id, city_location, "null", rating, language, "null",
                                   "null", reviewer_stay_date, trip_type, 0)

            if text is not None and review_result.should_translate_for_hotels() is True:
                review_result.text = self.translator.translate(text)

            self.database.add_review(review_result)

    def store_hotel(self, json_body, amenities):
        hotel_id = json_body["pdpHeader"]["hotelId"]
        name = self.get_hotel_name(json_body)
        country = json_body["propertyDescription"]["address"]["countryName"]
        city = json_body["propertyDescription"]["address"]["locality"]
        rating = json_body["reviewContent"]["overall"]["rating"]

        hotel = Hotel(hotel_id, name, country, city, rating, amenities)
        self.database.add_hotel(hotel)

        return hotel

    def get_hotel_amenities(self, response):
        hotel_amenities_list = response.xpath('//div[@class="fact-sheet-table-cell"]//ul//li//text()').getall()
        amenities = ""
        for amenity in hotel_amenities_list:
            amenities += amenity + ", "
        amenities = amenities[:len(amenities) - 2]

        return amenities
