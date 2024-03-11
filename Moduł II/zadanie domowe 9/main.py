from seed import seed_mongo_db
from commands import show_quotes_by_tag, show_quotes_by_tags, show_quotes_of
import connect
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy


csv_file_path_authors = "spyder_results/authors.csv"
csv_file_path_quotes = "spyder_results/quotes.csv"

json_file_path_authors = "./authors.json"
json_file_path_quotes = "./quotes.json"


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": csv_file_path_authors
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']
    authors_links = set()

    def parse(self, response):
        author = response.xpath("/html//div[@class='author-details']")
        if author:
            yield {
                "fullname": author.xpath("h3[@class='author-title']/text()").get(),
                "born_date": author.xpath("p/span[@class='author-born-date']/text()").get(default=''),
                "born_location": author.xpath("p/span[@class='author-born-location']/text()").get(default=''),
                "description": author.xpath("div[@class='author-description']/text()").get(default=''),
            }
        for author_link in response.xpath("/html//div[@class='quote']/span/a/@href").extract():
            self.authors_links.add(author_link)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
        for author_link in self.authors_links:
            yield scrapy.Request(url=self.start_urls[0] + author_link)


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": csv_file_path_quotes
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


OPERATIONS_MAP = {
    "name": show_quotes_of,
    "tag": show_quotes_by_tag,
    "tags": show_quotes_by_tags
}


def main():
    choice = input(
        "Do you want to fill the MongoDB database with data? (Y/N) ")
    if choice.lower().strip() in ["y", "yes"]:
        process = CrawlerProcess(get_project_settings())
        process.crawl('quotes_spider')
        process.start()
        seed_mongo_db()

    print("""
          Enter command name, tag, or tags.
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
        else:
            print("Invalid command format. Please try again.")


if __name__ == "__main__":
    main()
