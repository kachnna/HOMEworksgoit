from models import Quote, Author
from connect import client


def show_all_authors():
    authors = Author.objects()
    print("-------------ALL AUTHORS IN DATABASE--------------")
    if authors:
        seen_names = set()
        for author in authors:
            if author.fullname not in seen_names:
                print(f"{author.fullname}")
                seen_names.add(author.fullname)
    else:
        print("Sorry, there are no authors.")


def author_info(value):
    try:
        author_value = Author.objects(fullname=value.strip()).first()
        if author_value:
            print("Author:", author_value.fullname)
            print("Born Date:", author_value.born_date)
            print("Born Location:", author_value.born_location)
            print("Description:", author_value.description)
        else:
            print(
                f"Sorry, there are no authors with the name {value.strip()}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def show_quotes_of(value):
    try:
        author_value = Author.objects(fullname=value).first()
        if author_value:
            quotes = Quote.objects()
            if quotes:
                print(f"\nQuotes by author: {author_value.fullname}")
                for quote in quotes:
                    print(f"Quote: {quote.quote}")
            else:
                print(
                    f"Sorry, there are no quotes by {author_value.fullname}.")
        else:
            print(
                f"Sorry, there are no authors with the name {value.strip()}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def show_quotes_by_tag(value):
    try:
        unique_quotes = set()
        quotes = Quote.objects(tags__name=value)

        if quotes:
            print(f"\nQuotes with tag: {value}")
            for quote in quotes:
                unique_quotes.add(quote.quote)

            for quote in unique_quotes:
                print(f"Quote: {quote}")
        else:
            print(f"Sorry, there are no quotes with the tag {value}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def show_quotes_by_tags(values):
    try:
        tags = values.split(',')
        unique_quotes = set()
        quotes = Quote.objects(tags__name__in=tags)

        if quotes:
            print(f"\nQuotes with tags: {', '.join(tags)}")
            print("-"*20)
            for quote in quotes:
                unique_quotes.add(quote.quote)

            for quote in unique_quotes:
                print(f"Quote: {quote}")
        else:
            print(
                f"Sorry, there are no quotes with the tags {', '.join(tags)}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
