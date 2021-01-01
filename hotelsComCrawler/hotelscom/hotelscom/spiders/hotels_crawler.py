import scrapy
import json
from google_trans_new import google_translator


class Crawler(scrapy.Spider):
    name = "crawler"
    start_urls = ["https://www.hotels.com/ho"]

    def start_requests(self):
        base_url = "https://www.hotels.com/ho"
        initial_hotel_id = 268916
        last_hotel_id = 268917
        for hotel_id in range(initial_hotel_id, last_hotel_id):
            yield scrapy.Request(base_url + str(hotel_id), self.parse)

    def parse(self, response):
        if response.request.url != "https://www.hotels.com/":
            for reviews_page_number in range(1, 60):
                reviewPagesRequestUrl = response.request.url + '-tr-p' + str(reviews_page_number) + '/?ajax=true&reviewTab=brand-reviews&ajax=true'
                yield scrapy.Request(reviewPagesRequestUrl, self.parse_reviews)

    def get_json_body(self, json_object):
        json_data = json_object["data"]
        json_body = object()
        if json_data:
            json_body = json_data["body"]

        return json_body

    def get_hotel_name(self, json_object):
        json_body = self.get_json_body(json_object)
        hotel_name = ""
        if json_body["propertyDescription"] is not None and json_body["propertyDescription"]["name"] is not None:
            hotel_name = json_body["propertyDescription"]["name"]

        return hotel_name

    def get_review_item_groups(self, json_object):
        review_item_groups = []
        json_body = self.get_json_body(json_object)
        print(json)
        if json_body:
            review_content = json_body["reviewContent"]
            if review_content is not None and review_content["reviews"] is not None and review_content["reviews"]["hermes"] is not None:
                review_groups = review_content["reviews"]["hermes"]["groups"]
                if len(review_groups) > 0:
                    for i in range(0, len(review_groups)):
                        current_review_group = review_groups[i]
                        review_item_groups.append(current_review_group["items"])

        return review_item_groups

    def parse_reviews(self, response):
        filename = "reviews.txt"
        json_body = json.loads(response.body)
        hotel_name = self.get_hotel_name(json_body)
        review_groups = self.get_review_item_groups(json_body)
        translator = google_translator()

        with open(filename, 'a', encoding="utf-8-sig") as f:
            with open(hotel_name, 'a', encoding="utf-8-sig") as separate_file:
                if hotel_name is not None and len(hotel_name) > 0:
                    for i in range(0, len(review_groups)):
                        for review in review_groups[i]:
                            if review is not None and review["description"] is not None and len(review["description"]) > 0:
                                f.write(hotel_name + ' - ' + translator.translate(review["description"]) + '\n')
                                separate_file.write(translator.translate(review["description"]) + '\n')