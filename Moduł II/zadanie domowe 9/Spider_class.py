import scrapy


csv_path_authors = "result/authors.csv"
csv_path_quotes = "result/quotes.csv"

json_file_path_authors = "./authors.json"
json_file_path_quotes = "./quotes.json"


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": csv_path_authors
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
        "FEED_URI": csv_path_quotes
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
