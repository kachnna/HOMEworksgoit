from models import Quote, Author
from seed import seed_mongo_db
import connect


def show_quotes_of(value):
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


def show_quotes_by_tag(value):
    quotes = Quote.objects(tags=value)
    if quotes:
        print(f"\nQuotes with tag: {value}")
        for quote in quotes:
            print(f"Quote: {quote.quote}")
    else:
        print(f"Sorry, there are no quotes with the tag {value}.")


def show_quotes_by_tags(values):
    quotes = Quote.objects(tags__in=values)
    if quotes:
        print(f"\nQuotes with tags: {', '.join(values)}")
        for quote in quotes:
            print(f"Quote: {quote.quote}")
    else:
        print(f"Sorry, there are no quotes with the tags {', '.join(values)}.")


OPERATIONS_MAP = {
    "name": show_quotes_of,
    "tag": show_quotes_by_tag,
    "tags": show_quotes_by_tags
}

if __name__ == "__main__":
    # choice = input("Do you want to fill mongo database with data? ")
    # if choice in ["y", "Y", "Yes", "yes"]:
    #     # seed_mongo_db()
    print("""
          Enter command name, tag or tags.
          name: Steve Martin — znajdź i zwróć listę wszystkich cytatów autora Steve Martin;
          tag:life — znajdź i zwróć listę cytatów dla tagu life;
          tags:life,live — znajdź i zwróć listę cytatów, które zawierają tagi life lub live (bez spacji między tagami life, live);
          exit — zamknij skrypt;"""
          )
    while True:
        user_input = input("\nEnter command: ")
        if user_input.lower() == "exit":
            break
        input_splitted = user_input.split(":")
        command = input_splitted[0].lower().strip()
        if command in OPERATIONS_MAP:
            if len(input_splitted) > 1:
                value = input_splitted[1].strip()
                if len(value) == 0:
                    print("You have not provided any value. Please, try again.")
                else:
                    OPERATIONS_MAP[command](value)
            else:
                print(
                    f"No value provided for command: {command}. Please, try again.")
        else:
            print("Invalid command format. Please try again.")
