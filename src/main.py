from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from futbolenlatv.spiders.spider import FutbolSpider

load_dotenv()

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(FutbolSpider)
    process.start()
