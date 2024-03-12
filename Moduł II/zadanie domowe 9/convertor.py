import csv
import json


def make_authors_json(csvPath, jsonPath):
    authors = []
    with open(csvPath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            author_data = {
                "fullname": row["fullname"],
                "born_date": row["born_date"],
                "born_location": row["born_location"],
                "description": row["description"].strip()
            }
            authors.append(author_data)
    with open(jsonPath, 'w', encoding='utf-8') as json_file:
        json.dump(authors, json_file, ensure_ascii=False, indent=4)


def make_quotes_json(csvPath, jsonPath):
    quotes = []
    with open(csvPath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            quote_data = {
                "tags": [tag.strip() for tag in row["keywords"].split(",")],
                "author": row["author"],
                "quote": row["quote"]
            }
            quotes.append(quote_data)
    with open(jsonPath, 'w', encoding='utf-8') as json_file:
        json.dump(quotes, json_file, ensure_ascii=False, indent=4)
