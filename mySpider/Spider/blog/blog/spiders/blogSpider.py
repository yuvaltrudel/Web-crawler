import scrapy
from scrapy.http import FormRequest


class BlogSpider(scrapy.Spider):
    name = 'blog'
    start_urls = [
        'http://3.120.144.6:2233/'
    ]

    def __init__(self):
        self.links = []

    # login to the blog website with my user
    def parse(self, response):
        return FormRequest.from_response(response, formdata={
            'l_email': 'yuval12@walla.com',
            'l_password': 'Aa123456'

        }, callback=self.start_scraping)

    # get all the links in the website and the number of pic on each link
    def start_scraping(self, response):
        # get the link and add it to the list (recursive)
        self.links.append(response.url)
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.start_scraping)
        # get the mun of images on each link
        image = response.css('img::attr(class)').extract()
        link = self.links[-1]
        if not image:
            num = 0
        else:
            num = len(image)

        yield {
            'link': link,
            'number of images': num
        }
