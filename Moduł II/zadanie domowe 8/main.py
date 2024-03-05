from models import Quote, Author
from seed import seed_mongo_db
import connect


def show_quotes_of_name(value: str):
    author_value = Author.objects(fullname=value).first()
    if author_value:
        quotes = Quote.objects(author=author_value)
        if quotes:
            print(f"\nQuotes with name: {value}")
            for quote in quotes:
                print(f"Quote: {quote.quote}")
        else:
            print(f"Sorry, there are no quotes by {value}.")
    else:
        print(f"Sorry, there are no authors with the name {value}.")


if __name__ == "__main__":
    choice = input("Do you want to fill mongo database with data? ")
    if choice in ["y", "Y", "Yes", "yes"]:
        seed_mongo_db()
    while True:
        query = input("Enter command (name: <author>, exit): ")
        if query.lower() == "exit":
            break
        elif query.startswith("name:"):
            author_name = query.split(":")[1].strip()
            show_quotes_of_name(author_name)
        else:
            print("Invalid command format. Please try again.")
