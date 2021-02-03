import json
import re

import scrapy
from scrapy import Request

from common.domain.review import Review
from common.domain.reviews import Reviews
from google_trans_new import google_translator


BASE_URL = "https://www.tripadvisor.com"

class HotelReviewSpider(scrapy.Spider):
    name = "tripadvisor"

    # start_urls = [
    #     "https://www.tripadvisor.com/Hotel_Review-g488299-d202929-Reviews-Caesar_Augustus_Hotel"
    #     "-Anacapri_Island_of_Capri_Province_of_Naples_Campania.html",
    #     "https://www.tripadvisor.com/Hotel_Review-g187791-d205044-Reviews-Hotel_Artemide-Rome_Lazio.html"
    # ]
    start_urls = [
        "https://www.tripadvisor.com/Hotel_Review-d"
    ]

    def start_requests(self):
        base_url = "https://www.tripadvisor.com/Hotel_Review-d"
        # base_url = "https://www.tripadvisor.com/Hotel_Review-g293974-d1674691-Reviews-or790-Hotel_Amira_Istanbul-Istanbul.html#REVIEWS"
        initial_hotel_id = 1674691
        last_hotel_id = 1674692
        for hotel_id in range(initial_hotel_id, last_hotel_id):
            yield Request(base_url + str(hotel_id), self.parse)


    def parse(self, response, **kwargs):
        page = response.url.split('/')[-1]  #not used?
        filename = "/Users/bratanovn/Uni-Projects/TripAdvisorCrawler/data/hotel-reviews.csv"
        translator = google_translator()

        reviews = self.parse_reviews(response)
        hotel_name = self.get_hotel_name(response).lower()
        single_filename = "/Users/bratanovn/Uni-Projects/TripAdvisorCrawler/data/" + hotel_name + '.txt'

        with open(filename, 'a', encoding="utf-8-sig") as f:
            with open(single_filename, 'a', encoding="utf-8-sig") as single_file:
                for review in reviews.reviews:
                    if review is not None and review.text is not None and len(review.text) > 0:
                        translated_review = translator.translate(review.text) + "\n"
                        f.write(hotel_name + " - " + review.text + "\n")
                        single_file.write(translated_review)

        next_page_link = response.xpath('//a[@class="ui_button nav next primary "]').attrib['href']
        if next_page_link is not None:
            yield Request(BASE_URL + next_page_link, callback=self.parse)

    def get_hotel_name(self, response):
        return response.xpath('//h1[@id="HEADING"]//text()').get()

    def parse_reviews(self, response):
        """
        old version
        reviews = response.xpath('//q[@class="IRsGHoPm"]//span').getall()
        reviews = list(map(lambda r: r.replace('<span>', '').replace('</span>', ''), reviews))

        """

        review_id = response.xpath('//div[@class="oETBfkHU"]').attrib['data-reviewid']
        print(review_id)

        first_review = f'//script[contains(., "{review_id}")]'
        regex = r'"reviews":(.*)},"reviewAggregations":'
        print("\n" + first_review)
        prefix = '{ "reviews": '
        suffix = "}"

        reviews = prefix + response.xpath(first_review).re_first(r'"reviews":(.*)},"reviewAggregations":') + suffix

        try:
            review_ids = re.findall(r'"id":([0-9]+?),', reviews)
            review_texts = re.findall('"text":"(.+?)",', reviews)
        except AttributeError:
            raise AttributeError("No text or id field in reviews")

        reviews = Reviews()
        for i in range(5):
            review = Review(review_ids[i], review_texts[i])
            reviews.add(review)

        reviews.print()

        return reviews
