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
        author_id = authors_collection.insert_one({
            "fullname": author["fullname"],
            "born_date": born_date,
            "born_location": author["born_location"],
            "description": author["description"]
        }).inserted_id
        for quote in quotes:
            if quote["author"] == author["fullname"]:
                tags = [{"name": tag} for tag in quote["tags"]]
                quotes_collection.insert_one({
                    "author_id": author_id,
                    "quote": quote["quote"],
                    "tags": tags
                })


def seed_mongo_db():
    authors_file_path = "./task1/authors.json"
    quotes_file_path = "./task1/quotes.json"

    authors_data = read_json_data(authors_file_path)
    quotes_data = read_json_data(quotes_file_path)

    save_data_to_mongodb(authors_data, quotes_data, client)
