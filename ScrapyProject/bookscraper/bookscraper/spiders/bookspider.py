import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    '''
    A web scraper spider that scrapes book data from "books.toscrape.com". custom_settings is used to define item pipelines and feed export settings.
    The spider starts at the main page, follows links to individual book pages, and extracts details such as title, price, stock availability, rating, description, UPC, category, and URL.
    The extracted data is processed through the BookscraperPipeline for cleaning and transformation before being saved to a JSON file named 'booksdata.json'.
    The spider also handles pagination by following the "next" page links to scrape all available books on the site.
    '''
    
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'bookscraper.pipelines.BookscraperPipeline': 300,
    #     },
    #     'FEEDS': {
    #         'booksdata.json': {'format': 'json', 'overwrite': True},
    #     }
    # }

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            book_url = book.css("h3 a::attr(href)").get()
            yield response.follow(book_url, self.parse_book)

        
        next_page = response.css("li.next a::attr(href)").get()

        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        title = response.css("div.product_main h1::text").get()
        price = response.css("p.price_color::text").get()
        stock = response.css("p.instock.availability::text")
        rating = response.css("p.star-rating").attrib["class"].split()[-1]
        description = response.css("#product_description ~ p::text").get()
        upc = response.css("th:contains('UPC') + td::text").get()
        category = response.css("ul.breadcrumb li:nth-child(3) a::text").get()

        bookItem = BookItem()

        bookItem['title'] = title
        bookItem['price'] = price
        bookItem['stock'] = stock
        bookItem['rating'] = rating
        bookItem['description'] = description
        bookItem['upc'] = upc
        bookItem['category'] = category
        bookItem['url'] = response.url

        yield bookItem