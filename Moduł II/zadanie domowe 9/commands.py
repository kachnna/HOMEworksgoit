from models import Quote, Author

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
