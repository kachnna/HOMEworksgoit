import scrapy
from scrapy.crawler import CrawlerProcess

results_authors = []
results_quotes = []


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
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


def data():
    if results_authors or results_quotes:
        return results_authors, results_quotes
    process = CrawlerProcess()
    process.crawl(AuthorsSpider)
    process.crawl(QuotesSpider)
    process.start()
    return results_authors, results_quotes
