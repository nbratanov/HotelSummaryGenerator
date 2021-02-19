import mysql.connector as mysql
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor


class DatabaseConnector:
    database: MySQLConnection
    cursor: MySQLCursor

    def __init__(self):
        self.database = mysql.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="hotel_reviews"
        )
        self.cursor = self.database.cursor()

    def add_review(self, review):
        query = "INSERT IGNORE INTO reviews (id, text, hotel_id, city_location, hotel_publish_date, rating, language," \
                " original_language, translation_type, reviewer_stay_date, trip_type, like_count) VALUES (%s, %s, %s," \
                " %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            review.id, review.text, review.hotel_id, review.city_location, review.hotel_publish_date, review.rating,
            review.language, review.original_language, review.translation_type, review.reviewer_stay_date,
            review.trip_type,
            review.like_count)
        self.cursor.execute(query, values)
        self.database.commit()

    def add_hotel(self, hotel):
        query = "INSERT IGNORE INTO hotels (id, name, country, city, rating, amenities) VALUES " \
                "(%s, %s, %s, %s, %s, %s)"
        values = (hotel.id, hotel.name, hotel.country, hotel.city, hotel.rating, hotel.amenities)
        self.cursor.execute(query, values)
        self.database.commit()

    def get_hotel_id_by_name(self, name):
        query = f"SELECT id FROM hotels WHERE name = {name}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        return result

    def get_review_by_hotel_id(self, hotel_id):
        query = f"SELECT text FROM reviews WHERE hotel_id = {hotel_id}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        reviews = list()
        for review in result:
            reviews.append(review)

        return reviews

    def store_generated_summaries(self, hotel_summary):
        query = "INSERT IGNORE INTO hotel_summaries (hotel_id, frequency_summary, tf_idf_summary, frequent_phrases) " \
                "VALUES (%s, %s, %s, %s) "
        values = (hotel_summary.hotel_id, hotel_summary.frequency_summary, hotel_summary.tf_idf_summary,
                  hotel_summary.frequent_phrases)
        self.cursor.execute(query, values)
        self.database.commit()

    def get_all_reviews(self):
        query = f"SELECT text FROM reviews"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        reviews = list()
        for review in result:
            reviews.append(review)

        return reviews

    def get_hotels_information(self):
        query = f"SELECT * FROM hotels as hs LEFT JOIN hotel_summaries as h ON hs.id = h.hotel_id"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        hotel_summaries = list()
        for hotel_summary in result:
            hotel_summaries.append(hotel_summary)

        return hotel_summaries

    def get_hotel_summary_by_id(self):
        query = f"SELECT * FROM hotel_summaries"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        hotel_summaries = list()
        for hotel_summary in result:
            hotel_summaries.append(hotel_summary)

        return hotel_summaries
