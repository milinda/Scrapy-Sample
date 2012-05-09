from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http.request import Request
import urlparse
from bscraper.items import BlogPost

class Tim(CrawlSpider):
    name = 'Tim'
    allowed_domains = ['radar.oreilly.com']
    start_urls = ['http://radar.oreilly.com/tim/']

    def handle_blog(self, response):
        hxs = HtmlXPathSelector(response)
        item = BlogPost()

        item['title'] = hxs.select("//div[@class='post_block']/div/h2[@id='title']/a/text()").extract()
        item['link'] = hxs.select("//div[@class='post_block']/div/h2[@id='title']/a/@href").extract()
        item['content'] = hxs.select("//div[@class='post_block']/div/div[@class='entry-body']/p/text()").extract()

        yield item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        prev = hxs.select("//div[@class='content-nav']/a[@rel='next']/@href").extract()
        prev_page_link = urlparse.urljoin("http://radar.oreilly.com/tim/", prev[0])
        yield Request(prev_page_link, self.parse)
        posts = hxs.select("//div[@class='entry-list']/div[@class='entry']")
        for post in posts:
            post_link = post.select("h2[@class='title']/a/@href").extract()
            yield Request(post_link[0], self.handle_blog)
