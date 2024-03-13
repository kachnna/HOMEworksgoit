import json
from models import Author, Quote, Tag
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
        try:
            born_date = datetime.strptime(author["born_date"], "%B %d, %Y")
        except ValueError:
            continue
        author_record = Author(
            fullname=author["fullname"],
            born_date=born_date,
            born_location=author["born_location"],
            description=author["description"]
        )

        author_record.save

    for quote in quotes:
        author_name = quote["author"]
        author = authors_collection.find_one({"fullname": author_name})
        if author:
            tags = [Tag(name=tag_name) for tag_name in quote["tags"]]
            quote_record = Quote(
                author=author_name,
                quote=quote["quote"],
                tags=tags
            )
            quote_record.save


def seed_mongo_db():
    authors_file_path = "./authors.json"
    quotes_file_path = "./quotes.json"

    authors_data = read_json_data(authors_file_path)
    quotes_data = read_json_data(quotes_file_path)

    save_data_to_mongodb(authors_data, quotes_data, client)


if __name__ == "__main__":
    seed_mongo_db()
