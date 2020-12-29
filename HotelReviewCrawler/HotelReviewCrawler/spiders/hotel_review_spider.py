import json

import scrapy
from scrapy import Request
from . import reviews_model

BASE_URL = "https://www.tripadvisor.com"

class HotelReviewSpider(scrapy.Spider):
    name = "tripadvisor"

    # start_urls = [
    #     "https://www.tripadvisor.com/Hotel_Review-g488299-d202929-Reviews-Caesar_Augustus_Hotel"
    #     "-Anacapri_Island_of_Capri_Province_of_Naples_Campania.html",
    #     "https://www.tripadvisor.com/Hotel_Review-g187791-d205044-Reviews-Hotel_Artemide-Rome_Lazio.html"
    # ]
    start_urls = [
        "https://www.tripadvisor.com/Hotel_Review-g488299-d202929-Reviews-or15-Caesar_Augustus_Hotel-Anacapri_Island_of_Capri_Province_of_Naples_Campania.html"
    ]

    def parse(self, response, **kwargs):
        page = response.url.split('/')[-1]
        filename = "hotel-reviews.csv"

        review_schema = self.parse_reviews(response)

        with open(filename, 'a') as f:
            for review in review_schema['reviews']:
                f.write(review['text'] + "\n")

        next_page_link = response.xpath('//a[@class="ui_button nav next primary "]').attrib['href']
        if next_page_link is not None:
            yield Request(BASE_URL + next_page_link, callback=self.parse)

    def parse_reviews(self, response):
        """
        old version
        reviews = response.xpath('//q[@class="IRsGHoPm"]//span').getall()
        reviews = list(map(lambda r: r.replace('<span>', '').replace('</span>', ''), reviews))

        """

        review_id = response.xpath('//div[@class="oETBfkHU"]').attrib['data-reviewid']
        print(review_id)

        first_review = f'//script[contains(., "{review_id}")]'
        print(type(first_review))
        regex = r'"reviews":(.*)},"reviewAggregations":'
        print("\n" + first_review)
        prefix = '{ "reviews": '
        suffix = "}"

        reviews = prefix + response.xpath(first_review).re_first(r'"reviews":(.*)},"reviewAggregations":') + suffix

        # review_schema = reviews_model.Reviews.Schema().load(json.loads(reviews))
        review_schema = json.loads(reviews)

        return review_schema
