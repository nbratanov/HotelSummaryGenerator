import mysql.connector as mysql


class DatabaseUtil:

    """Create reviews database"""
    @staticmethod
    def setup_database():
        db = mysql.connect(
            host="localhost",
            user="root",
            passwd="password"
        )

        cursor = db.cursor()
        cursor.execute("CREATE DATABASE hotel_reviews")

    """Create database tables"""
    @staticmethod
    def setup_tables():
        db = mysql.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="hotel_reviews"
        )

        cursor = db.cursor()
        cursor.execute("CREATE TABLE reviews("
                       "id VARCHAR(255) NOT NULL PRIMARY KEY,"
                       "text VARCHAR(5000),"
                       "hotel_id VARCHAR(255) NOT NULL,"
                       "city_location VARCHAR(50),"
                       "hotel_publish_date DATE,"
                       "rating INT(10),"
                       "language VARCHAR(50),"
                       "original_language VARCHAR(50),"
                       "translation_type VARCHAR(5),"
                       "reviewer_stay_date DATE,"
                       "trip_type VARCHAR(15),"
                       "like_count INT(10)"
                       ")")

        cursor.execute("CREATE TABLE hotels("
                       "id VARCHAR(255) NOT NULL PRIMARY KEY,"
                       "name VARCHAR(255),"
                       "country VARCHAR(50),"
                       "city VARCHAR(50),"
                       "rating INT(10),"
                       "amenities VARCHAR(5000)"
                       ")")

        cursor.execute("CREATE TABLE hotel_summaries("
                       "hotel_id VARCHAR(255) NOT NULL PRIMARY KEY,"
                       "frequency_summary TEXT(15000),"
                       "tf_idf_summary TEXT(15000),"
                       "frequent_phrases VARCHAR(5000)"
                       ")")
