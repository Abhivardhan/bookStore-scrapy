import scrapy

class BookStoreSpider(scrapy.Spider):
    name = "bookstore_spider"

    def start_requests(self):
        url = "http://books.toscrape.com/"

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        articles = response.css("article.product_pod")
        for article in articles:
            image = article.css("div.image_container a img::attr(src)").get()
            title = article.css("div.image_container a img::attr(alt)").get()
            price = article.css("div.product_price p.price_color::text").get()

            yield { 
                'image_url': image,
                "book_title": title,
                'product_price': price
            }


        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
