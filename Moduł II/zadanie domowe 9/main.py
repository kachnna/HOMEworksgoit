from seed import seed_mongo_db
from commands import show_quotes_by_tag, show_quotes_by_tags, show_quotes_of, author_info, show_all_authors
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Spider_class import AuthorsSpider, QuotesSpider
from convertor import make_authors_json, make_quotes_json
from file_paths import csv_path_authors, csv_path_quotes, json_path_authors, json_path_quotes
import connect


OPERATIONS_MAP = {
    "author": author_info,
    "name": show_quotes_of,
    "tag": show_quotes_by_tag,
    "tags": show_quotes_by_tags
}


def main():
    choice = input(
        "Do you want to fill the MongoDB database with data? (Y/N) ")
    if choice.lower().strip() in ["y", "yes"]:
        process = CrawlerProcess(get_project_settings())
        process.crawl(AuthorsSpider)
        process.crawl(QuotesSpider)
        process.start()
        make_authors_json(csv_path_authors, json_path_authors)
        make_quotes_json(csv_path_quotes, json_path_quotes)
        seed_mongo_db()

    print("""
          Enter command show all authors, author, name, tag, or tags.
          show all authors - show all authors in database
          author: Steve Martin - information about author
          name: Steve Martin — find and return a list of all quotes by author Steve Martin;
          tag: life — find and return a list of quotes for the tag 'life';
          tags: life,live — find and return a list of quotes that contain tags 'life' or 'live' (without spaces between tags);
          exit — exit the script;"""
          )

    while True:
        user_input = input("\nEnter command\n ")
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
        elif command == "show all authors":
            show_all_authors()
        else:
            print("Invalid command format. Please try again.")


if __name__ == "__main__":
    main()
