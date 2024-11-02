import scrapy


class FutbolItem(scrapy.Item):
    date = scrapy.Field()  # Date of the match
    hour = scrapy.Field()  # Hour of the match
    datetime = scrapy.Field()  # Date and hour of the match in datetime format
    local = scrapy.Field()  # Local team
    visitor = scrapy.Field()  # Visitor team
    competition = scrapy.Field()  # Competition name
    channels = scrapy.Field()  # Channels that broadcast the match
