import json
from datetime import datetime
from connect import client


def read_json_data(file_path):
    with open(file_path, "r", encoding="UTF-8") as fh:
        readable_data = json.load(fh)
    return readable_data


def save_data_to_mongodb(authors, quotes, db):
    database = db["database"]
    authors_collection = database["authors"]
    quotes_collection = database["quotes"]

    for author in authors:
        born_date = datetime.strptime(author["born_date"], "%B %d, %Y")
        author_record = {
            "fullname": author["fullname"],
            "born_date": born_date,
            "born_location": author["born_location"],
            "description": author["description"]
        }
        author_id = authors_collection.insert_one(author_record).inserted_id

        author_quotes = [
            quote for quote in quotes if quote["author"] == author["fullname"]]
        for quote in author_quotes:
            tags = [{"name": tag} for tag in quote["tags"]]
            quote_record = {
                "author_id": author_id,
                "author": quote["author"],
                "quote": quote["quote"],
                "tags": tags
            }
            quotes_collection.insert_one(quote_record)


def seed_mongo_db():
    authors_file_path = "./authors.json"
    quotes_file_path = "./quotes.json"

    authors_data = read_json_data(authors_file_path)
    quotes_data = read_json_data(quotes_file_path)

    save_data_to_mongodb(authors_data, quotes_data, client)
