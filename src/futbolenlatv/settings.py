# Scrapy settings for futbolenlatv project
BOT_NAME = 'futbolenlatv'

SPIDER_MODULES = ['futbolenlatv.spiders']
NEWSPIDER_MODULE = 'futbolenlatv.spiders'

# Robot rules
ROBOTSTXT_OBEY = True

# Item pipelines
ITEM_PIPELINES = {
    'futbolenlatv.pipelines.FutbolPipeline': 300,
}

# Logging settings
LOG_LEVEL = 'ERROR'
